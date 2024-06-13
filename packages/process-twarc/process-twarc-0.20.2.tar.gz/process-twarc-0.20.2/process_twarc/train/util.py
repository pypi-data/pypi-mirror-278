from transformers import (
    AutoTokenizer, 
    TrainerCallback, 
    Trainer, 
    get_constant_schedule_with_warmup, 
    get_linear_schedule_with_warmup, 
    get_cosine_schedule_with_warmup, 
    get_cosine_with_hard_restarts_schedule_with_warmup, 
    DataCollatorWithPadding, 
    DataCollatorForLanguageModeling,
    TrainingArguments, 
    EarlyStoppingCallback, 
    AutoModelForMaskedLM, 
    AutoModelForSequenceClassification,
    AutoModelForMultipleChoice,
    AutoModelForQuestionAnswering,
    TrainerState,
    TrainerControl,
)
# from adapters import AdapterTrainer, AutoAdapterModel
from process_twarc.util import load_dataset, load_dict, make_dir
import inspect
import torch
from torch.optim import AdamW
import wandb
import optuna
from ntpath import basename
import evaluate
import numpy as np
import os
import shutil
from datasets import Dataset, concatenate_datasets
from typing import List, Tuple
import unicodedata
import string
import re
from process_twarc.util import load_dict

import adapters
from adapters import AdapterTrainer, AutoAdapterModel, Fuse
from adapters.heads import PredictionHead, SequenceClassifierOutput
from adapters.configuration.adapter_config import (
    SeqBnConfig,
    DoubleSeqBnConfig,
    ParBnConfig,
    SeqBnInvConfig,
    DoubleSeqBnInvConfig,
    CompacterPlusPlusConfig,
    CompacterConfig,
    PrefixTuningConfig,
    PromptTuningConfig,
    LoRAConfig,
    IA3Config,
    MAMConfig,
    UniPELTConfig
)

from dataclasses import dataclass
from transformers.tokenization_utils_base import PreTrainedTokenizerBase, PaddingStrategy
from typing import Optional, Union
import collections
from tqdm import tqdm
from collections import Counter
import fugashi
import unidic_lite
from transformers import AutoConfig
import re

def login_to_wandb(path_to_keys: str="keys/keys.json"):
    key = load_dict(path_to_keys)["wandb_api_key"]
    wandb.login(key=key)
    return

import torch
from torch import nn
from transformers import AutoModel


class OptunaCallback(TrainerCallback):
    def __init__(self, trial, should_prune):
        self.trial = trial
        self.should_prune = should_prune

    def on_evaluate(self, args, state, control, metrics=None, **kwargs):
        # Collect all loss values
        loss_keys = [key for key in metrics.keys() if "loss" in key]
        if loss_keys:
            # Calculate the average loss from all loss metrics
            total_loss = sum(metrics[key] for key in loss_keys if metrics[key] is not None)
            avg_loss = total_loss / len(loss_keys)

            # Report the average loss to Optuna
            self.trial.report(avg_loss, step=state.global_step)

            # Check for pruning
            if self.should_prune and self.trial.should_prune():
                raise optuna.TrialPruned()
        else:
            print("Warning: No loss metrics found to report to Optuna.")
        
class StopCallback(TrainerCallback):
    def on_epoch_end(self, args, state, control, logs=None, **kwargs):
        control.should_training_stop = True
        control.should_save = True

    
class CustomTrainingArguments(TrainingArguments):
    def __init__(self, *args, wandb_run_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        if wandb_run_id:
            self.wandb_run_id = wandb_run_id

@dataclass
class DataCollatorForMultipleChoice:
    """
    Data collator that will dynamically pad the inputs for multiple choice received.
    """

    tokenizer: PreTrainedTokenizerBase
    padding: Union[bool, str, PaddingStrategy] = True
    max_length: Optional[int] = None
    pad_to_multiple_of: Optional[int] = None

    def __call__(self, features):
        label_name = "label" if "label" in features[0].keys() else "labels"
        labels = [feature.pop(label_name) for feature in features]
        batch_size = len(features)
        num_choices = len(features[0]["input_ids"])
        flattened_features = [
            [{k: v[i] for k, v in feature.items()} for i in range(num_choices)] for feature in features
        ]
        flattened_features = sum(flattened_features, [])

        batch = self.tokenizer.pad(
            flattened_features,
            padding=self.padding,
            max_length=self.max_length,
            pad_to_multiple_of=self.pad_to_multiple_of,
            return_tensors="pt",
        )

        batch = {k: v.view(batch_size, num_choices, -1) for k, v in batch.items()}
        batch["labels"] = torch.tensor(labels, dtype=torch.int64)
        return batch


class MultiDatasetTrainer(Trainer):
    def __init__(self, *args, eval_dataset, eval_datasets, **kwargs):
        super().__init__(*args, **kwargs)
        self.eval_dataset = eval_dataset
        self.eval_datasets = eval_datasets
    def evaluate(self, ignore_keys=None):
        results = {}
        # Evaluate the main dataset first if it's available

        print("Evaluating main dataset")
        main_results = super().evaluate(self.eval_dataset, ignore_keys)
        # Update results with plain metric names
        results.update(main_results)
        
        # Evaluate each additional dataset separately
        for dataset, name in self.eval_datasets:
            print(f"Evaluating dataset: {name}")
            individual_result = super().evaluate(dataset, ignore_keys)
            individual_result = {k:v for k, v in individual_result.items() if k not in [
                "eval_runtime",
                "eval_samples_per_second",
                "eval_steps_per_second"
                "epoch"
            ]}
            # Properly prefix each metric with the dataset name
            results.update({f"{name}_{k}": v for k, v in individual_result.items()})
        
        print(f"Metrics after evaluation: {results}")
        return results

    
def get_WRIME_metrics(predictions, labels, threshold=float(3/12)):
    
    from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score, accuracy_score
    from scipy.stats import pearsonr

    def compute_top_choice_accuracy(predictions, labels):
        correct_top_matches = 0
        total_samples = len(predictions)

        for pred, lab in zip(predictions, labels):
            # Determine the highest label values and indices
            lab_indices = np.argwhere(lab == np.max(lab)).flatten()
            
            # Number of top label indices with highest value
            num_top_labels = len(lab_indices)
            
            # Get the same number of highest prediction indices
            # First, sort predictions in descending order and select the top 'num_top_labels' values
            sorted_pred_indices = np.argsort(pred)[::-1][:num_top_labels]
            
            # Check if there's an intersection between these top prediction indices and top label indices
            if set(sorted_pred_indices) & set(lab_indices):
                correct_top_matches += 1

        return correct_top_matches / total_samples

    
    def get_pearson(pred, lab):
        return pearsonr(pred, lab)[0]
    
    pearson_values = [get_pearson(pred, lab) for pred, lab in zip(predictions, labels) if not np.isnan(get_pearson(pred, lab))]
    # First, apply sigmoid on predictions which are of shape (batch_size, num_labels)
    sigmoid = torch.nn.Sigmoid()
    probs = sigmoid(torch.Tensor(predictions))
    
    
    # Use the binarization threshold to turn them into integer predictions
    y_pred = (probs >= threshold).int().numpy()
    
    # Ensure labels are binary formatted as well
    y_true = (np.array(labels) >= threshold).astype(int)
    
    # Compute metrics
    f1_micro_average = f1_score(y_true=y_true, y_pred=y_pred, average='micro')
    precision_micro_average = precision_score(y_true=y_true, y_pred=y_pred, average='micro')
    recall_micro_average = recall_score(y_true=y_true, y_pred=y_pred, average='micro')
    roc_auc = roc_auc_score(y_true, y_pred, average='micro')
    
    
    # Return as dictionary
    metrics = {
               'top_choice_accuracy': compute_top_choice_accuracy(predictions, labels),
               'multi_label_pearson': np.mean(pearson_values),
               'NaNs': len(predictions) - len(pearson_values),
               'f1': f1_micro_average,
               'precision': precision_micro_average,
               'recall': recall_micro_average,
               'roc_auc': roc_auc
    }

    return metrics


def get_adapter_config(parameters):

    adapter_kwargs = parameters["adapter_kwargs"]
    config_kwargs = adapter_kwargs.get("config", {})
    config = config_kwargs.pop("type", "seq_bn")
    if config == "seq_bn":
        return SeqBnConfig(**config_kwargs)
    elif config == "double_seq_bn":
        return DoubleSeqBnConfig(**config_kwargs)
    elif config == "par_bn":
        return ParBnConfig(**config_kwargs)
    elif config == "seq_bn_inv":
        return SeqBnInvConfig(**config_kwargs)
    elif config == "double_seq_bn_inv":
        return DoubleSeqBnInvConfig(**config_kwargs)
    elif config == "compacter++":
        return CompacterPlusPlusConfig(**config_kwargs)
    elif config == "compacter":
        return CompacterConfig(**config_kwargs)
    elif config == "prefix_tuning":
        return PrefixTuningConfig(**config_kwargs)
    elif config == "prompt_tuning":
        return PromptTuningConfig(**config_kwargs)
    elif config == "lora":
        return LoRAConfig(**config_kwargs)
    elif config == "ia3":
        return IA3Config(**config_kwargs)
    elif config == "mam":
        return MAMConfig(**config_kwargs)
    elif config == "unipelt":
        return UniPELTConfig(**config_kwargs)


def get_compute_metrics(parameters, tokenizer = None, datasets=None, eval_split="validation"):
    

    eval_kwargs = parameters["evaluation_kwargs"]
    print(f"Evaluation kwargs: {eval_kwargs}")

    def compute_metrics(eval_pred):
        predictions, labels = eval_pred

        preset_metrics = eval_kwargs.get("preset_metrics", None)
        all_metrics = eval_kwargs.get("metrics", None)


        if preset_metrics:
            if preset_metrics == "stsb":
                print("Computing STSB metrics.")
                metrics = evaluate.load("glue", "stsb")
                return metrics.compute(predictions=predictions, references=labels)

            elif preset_metrics == "wrime":
                return get_WRIME_metrics(predictions, labels)

            elif preset_metrics == "squad":
                prepprocessed_dataset = datasets[eval_split]
                raw_dataset = datasets["raw"]
                raw_dataset = raw_dataset.filter(lambda x: x["id"] in prepprocessed_dataset["example_id"])
                return evaluate_qa_predictions(tokenizer, raw_dataset, prepprocessed_dataset, predictions)
        
        else:
            metrics = evaluate.combine(all_metrics)
            predictions = np.argmax(predictions, axis=1)
            if eval_kwargs.get("label_type") == "soft":
                labels = np.argmax(labels, axis=1)
            
            return metrics.compute(predictions=predictions, references=labels, average="micro")

    return compute_metrics

def preprocess_data_for_JSQuAD(
        dataset,
        tokenizer,
        max_length=384,
        stride=128,
        padding=True
        ):
    def get_offsets(input_ids: List[int],
                    context: str,
                    tokenizer: AutoTokenizer,
                    norm_form='NFKC') -> List[Tuple[int, int]]:
        '''The character-level start/end offsets of a token within a context.
        Algorithm:
        1. Make offsets of normalized context within the original context.
        2. Make offsets of tokens (input_ids) within the normalized context.

        Arguments:
        input_ids -- Token ids of tokenized context (by tokenizer).
        context -- String of context
        tokenizer
        norm_form

        Return:
            List[Tuple[int, int]]: Offsets of tokens within the input context.
            For each token, the offsets are presented as a tuple of (start
            position index, end position index). Both indices are inclusive.
        '''
        cxt_start = input_ids.index(tokenizer.sep_token_id) + 1
        # Continuing from the first SEP, find the next SEP token, which is after the first found SEP
        first_sep_end = cxt_start + input_ids[cxt_start:].index(tokenizer.sep_token_id)

        # Continue the search for the next SEP token from the position after the second SEP token
        cxt_end = first_sep_end + 1 + input_ids[first_sep_end + 1:].index(tokenizer.sep_token_id)
        tokens = tokenizer.convert_ids_to_tokens(input_ids[cxt_start:cxt_end])
        tokens = [tok[2:] if tok.startswith('##') else tok for tok in tokens]
        whitespace = string.whitespace + '\u3000'

        # 1. Make offsets of normalized context within the original context.
        offsets_norm_context = []
        norm_context = ''
        for idx, char in enumerate(context):
            norm_char = unicodedata.normalize(norm_form, char)
            norm_context += norm_char
            offsets_norm_context.extend([idx] * len(norm_char))
        norm_context_org = unicodedata.normalize(norm_form, context)
        assert norm_context == norm_context_org, \
            'Normalized contexts are not the same: ' \
            + f'{norm_context} != {norm_context_org}'
        assert len(norm_context) == len(offsets_norm_context), \
            'Normalized contexts have different numbers of tokens: ' \
            + f'{len(norm_context)} != {len(offsets_norm_context)}'


        # 2. Make offsets of tokens (input_ids) within the normalized context.
        offsets_token = []
        unk_pointer = None
        cid = 0
        tid = 0
        while tid < len(tokens):
            cur_token = tokens[tid]
            if cur_token == tokenizer.unk_token:
                unk_pointer = tid
                offsets_token.append([cid, cid])
                cid += 1
            elif norm_context[cid:cid + len(cur_token)] != cur_token:
                # Wrong offsets of the previous UNK token
                assert unk_pointer is not None, \
                    'Normalized context and tokens are not matched'
                prev_unk_expected = offsets_token[unk_pointer]
                prev_unk_expected[1] += norm_context[prev_unk_expected[1] + 2:]\
                    .index(tokens[unk_pointer + 1]) + 1
                tid = unk_pointer
                offsets_token = offsets_token[:tid] + [prev_unk_expected]
                cid = prev_unk_expected[1] + 1
            else:
                start_pos = norm_context[cid:].index(cur_token)
                if start_pos > 0 and tokens[tid - 1] == tokenizer.unk_token:
                    offsets_token[-1][1] += start_pos
                    cid += start_pos
                    start_pos = 0
                assert start_pos == 0, f'{start_pos} != 0 (cur: {cur_token}'
                offsets_token.append([cid, cid + len(cur_token) - 1])
                cid += len(cur_token)
                while cid < len(norm_context) and norm_context[cid] in whitespace:
                    offsets_token[-1][1] += 1
                    cid += 1
            tid += 1
        if tokens[-1] == tokenizer.unk_token:
            offsets_token[-1][1] = len(norm_context) - 1
        else:
            assert cid == len(norm_context) == offsets_token[-1][1] + 1, \
                'Offsets do not include all characters'
        assert len(offsets_token) == len(tokens), \
            'The numbers of tokens and offsets are different'

        offset_mapping = [(offsets_norm_context[start], offsets_norm_context[end])
                        for start, end in offsets_token]
        return [(-1, -1)] * cxt_start + offset_mapping

    def get_answer_positions(example):

        answers = example["answers"]["text"]
        start_chars = example["answers"]["answer_start"]
        
        offsets = example["offset_mapping"]
        input_ids = example["input_ids"]


        ctx_start = input_ids.index(tokenizer.sep_token_id) + 1
        answer_start_index = ctx_start
        answer_end_index = len(offsets) -1

        start_positions, end_positions = [], []

        for answer, start_char in zip(answers, start_chars):
            while offsets[answer_start_index][0] < start_char:
                answer_start_index += 1
            while offsets[answer_end_index][1] > start_char + len(answer):
                answer_end_index -= 1
            
            def check():
                cleaned_answer = re.sub(r'\s+', '', unicodedata.normalize("NFKC", answer))
                cleaned_prediction = re.sub(r'\s+', '', tokenizer.decode(input_ids[answer_start_index:answer_end_index+1]))
                return cleaned_answer == cleaned_prediction
            
            if not check(): # First correction attempt
                answer_end_index -= 1
            
        
            if not check(): # 1% of attempts fail. These are flagged for filtering
                answer_start_index, answer_end_index = -1, -1
            
            start_positions.append(answer_start_index)
            end_positions.append(answer_end_index)

        first_valid_answer, first_valid_start, first_valid_end = next(((a, s, e) for a, s, e in zip(answers, start_positions, end_positions) if s >= 0 and e >= 0), ("", -1, -1))
        for i in range(len(start_positions)):
            if start_positions[i] < 0 or end_positions[i] < 0:
                answers[i] = first_valid_answer
                start_positions[i] = first_valid_start
                end_positions[i] = first_valid_end
                    
        return {"start_positions": start_positions, "end_positions": end_positions, "answers": answers}

    def get_span_mapping(example, max_length=384, stride=128):
        span_mapping = []
        num_tokens = len(example["input_ids"])
        start = 1 # Remove CLS token
        end = num_tokens - 1 # Remove SEP token

        if num_tokens <= max_length:
            span_mapping.append((start, end)) 
            return span_mapping

        i = start
        effective_length = max_length - 2  # Accounting for CLS and SEP tokens

        
        while i < num_tokens:
            # Calculate the end of the current span
            end = i + effective_length

            if end > num_tokens:
                # Adjust to include the final tokens if the end surpasses the number of tokens
                end = num_tokens
                start = max(0, num_tokens - effective_length)  # Ensure at least 'effective_length' tokens are included
                span_mapping.append((start, end))
                break  # After adding the final span, break the loop
            else:
                # Add current span
                span_mapping.append((i, end))
            # Move start index by the stride
            i += stride

        return span_mapping

    def make_spans(example):

        output = {
                "example_id": [],
                "input_ids": [],
                "attention_mask": [],
                "token_type_ids": [],
                "offset_mapping": [],
                "start_positions": [],
                "end_positions": [],
                "answers": []
                }

        def get(column):
            return example[column]  # Remove CLS and SEP tokens

        example_id = example["id"]
        offset_mapping = example["offset_mapping"]
        start_positions = example["start_positions"]
        end_positions = example["end_positions"]
        answers = example["answers"]
        span_mapping = example["span_mapping"]
        input_ids = get("input_ids")
        attention_mask = get("attention_mask")
        token_type_ids = get("token_type_ids")

        # Add CLS and SEP tokens for each span
        def span_(data, start, end, start_token, end_token):
            return [start_token] + data[start:end] + [end_token]
        
        def adjust_positions(start_positions, end_positions, start, end):
            adjusted_starts = [(x+1) - start for x in start_positions]
            adjusted_ends = [(x+1) - start for x in end_positions]

            span_length = end - start
            for i in range(len(adjusted_starts)):
                if (adjusted_starts[i] < 0) or (adjusted_ends[i] >= span_length):
                    adjusted_starts[i] = 0
                    adjusted_ends[i] = 0
            return adjusted_starts, adjusted_ends
        
        for i in range(len(span_mapping)):
            start, end = span_mapping[i]
        
            output["input_ids"].append(span_(input_ids, start, end, tokenizer.cls_token_id, tokenizer.sep_token_id))
            output["attention_mask"].append(span_(attention_mask, start, end, 1, 1))
            output["token_type_ids"].append(span_(token_type_ids, start, end, token_type_ids[start], token_type_ids[end-1]))
            output["offset_mapping"].append(span_(offset_mapping, start, end, (-1, -1), (-1, -1)))

            output["example_id"].append(example_id)
            adjusted_starts, adjusted_ends = adjust_positions(start_positions, end_positions, start, end)
            first_valid_start, first_valid_end, first_valid_answer = next(((s, e, a) for s, e, a in zip(adjusted_starts, adjusted_ends, answers) if s >= 0 and e >= 0), (-1, -1, ""))
            output["start_positions"].append(first_valid_start)
            output["end_positions"].append(first_valid_end)
            output["answers"].append(first_valid_answer)

            assert len(output["input_ids"][-1]) == len(output["attention_mask"][-1]) == len(output["token_type_ids"][-1]), "Mappings are not the same length."
            assert len(output["input_ids"]) == len(output["attention_mask"]) == len(output["token_type_ids"]) == len(output["start_positions"]) == len(output["end_positions"]), "Lists are not the same length."

        return output

    def unpack_and_pad(dataset, pad_token_id, padding=False, max_length=384):
        df = dataset.to_pandas()[["input_ids", "attention_mask", "token_type_ids", "start_positions", "end_positions", "example_id", "offset_mapping"]]
        df = df.explode(df.columns.tolist())

        if padding:
            for idx, row in df.iterrows():
                pad_len = max_length - len(row["input_ids"])
                if pad_len > 0:
                    df.at[idx, "input_ids"] = row["input_ids"].tolist() + [pad_token_id] * pad_len
                    df.at[idx, "attention_mask"] = row["attention_mask"].tolist() + [0] * pad_len
                    df.at[idx, "token_type_ids"] = row["token_type_ids"].tolist() + [0] * pad_len
                    df.at[idx, "offset_mapping"] = row["offset_mapping"].tolist() + [(-1, -1)] * pad_len

        dataset = Dataset.from_pandas(df.reset_index(drop=True))
        return dataset

    def preprocess(
        dataset=dataset,
        tokenizer=tokenizer,
        max_length=max_length,
        stride=stride,
        padding=padding):
        
        tokenize_fn = lambda x: tokenizer(
            x["question"],
            x["context"]
        )
        dataset = dataset.map(tokenize_fn, batched=True, desc="Getting input_ids.", remove_columns = ["title", "is_impossible"])
        
        dataset = dataset.map(
            lambda x: {"offset_mapping": get_offsets(x["input_ids"], x["context"], tokenizer)},
            desc="Getting offsets.")
        
        dataset = dataset.map(get_answer_positions, desc="Getting answer positions.")
        dataset = dataset.filter(lambda x: x["start_positions"][0] > 0, desc="Filtering failed examples.")
        dataset = dataset.map(
            lambda x: {"span_mapping": get_span_mapping(x, max_length=max_length, stride=stride)},
            desc="Getting span mapping.")
        dataset = dataset.map(make_spans, desc="Making spans.")
        dataset = unpack_and_pad(
            dataset,
            pad_token_id= tokenizer.pad_token_id,
            padding=padding,
            max_length=max_length
        )
        return dataset

    return preprocess()

def postprocess_qa_predictions(tokenizer, raw_dataset, preprocessed_dataset, raw_predictions, n_best_size = 20, max_answer_length = 30):

    all_start_logits, all_end_logits = raw_predictions
    # Build a map example to its corresponding features.
    example_id_to_index = {k: i for i, k in enumerate(raw_dataset["id"])}
    features_per_example = collections.defaultdict(list)
    for i, feature in enumerate(preprocessed_dataset):
        features_per_example[example_id_to_index[feature["example_id"]]].append(i)

    # The dictionaries we have to fill.
    predictions = collections.OrderedDict()

    # Logging.
    print(f"Post-processing {len(raw_dataset)} example predictions split into {len(preprocessed_dataset)} features.")

    # Let's loop over all the examples!
    for example_index,  example in enumerate(tqdm(raw_dataset)):
        # Those are the indices of the features associated to the current example.
        feature_indices = features_per_example[example_index]

        min_null_score = None # Only used if squad_v2 is True.
        valid_answers = []
        
        context = example["context"]
        # Looping through all the features associated to the current example.
        for feature_index in feature_indices:
            # We grab the predictions of the model for this feature.
            start_logits = all_start_logits[feature_index]
            end_logits = all_end_logits[feature_index]
            # This is what will allow us to map some the positions in our logits to span of texts in the original
            # context.
            offset_mapping = preprocessed_dataset[feature_index]["offset_mapping"]

            # Update minimum null prediction.
            cls_index = preprocessed_dataset[feature_index]["input_ids"].index(tokenizer.cls_token_id)
            feature_null_score = start_logits[cls_index] + end_logits[cls_index]
            if min_null_score is None or min_null_score < feature_null_score:
                min_null_score = feature_null_score

            # Go through all possibilities for the `n_best_size` greater start and end logits.
            start_indexes = np.argsort(start_logits)[-1 : -n_best_size - 1 : -1].tolist()
            end_indexes = np.argsort(end_logits)[-1 : -n_best_size - 1 : -1].tolist()
            for start_index in start_indexes:
                for end_index in end_indexes:
                    # Don't consider out-of-scope answers, either because the indices are out of bounds or correspond
                    # to part of the input_ids that are not in the context.
                    if (
                        start_index >= len(offset_mapping)
                        or end_index >= len(offset_mapping)
                        or offset_mapping[start_index] == (-1, -1)
                        or offset_mapping[end_index] == (-1, -1)
                    ):
                        continue
                    # Don't consider answers with a length that is either < 0 or > max_answer_length.
                    if end_index < start_index or end_index - start_index + 1 > max_answer_length:
                        continue

                    start_char = offset_mapping[start_index][0]
                    end_char = offset_mapping[end_index][1]
                    valid_answers.append(
                        {
                            "score": start_logits[start_index] + end_logits[end_index],
                            "text": context[start_char: end_char+1]
                        }
                    )
        
        if len(valid_answers) > 0:
            best_answer = sorted(valid_answers, key=lambda x: x["score"], reverse=True)[0]
        else:
            # In the very rare edge case we have not a single non-null prediction, we create a fake prediction to avoid
            # failure.
            best_answer = {"text": "", "score": 0.0}
        
        # Let's pick our final answer: the best one or the null answer (only for squad_v2)
        # if not squad_v2:
        #     predictions[example["id"]] = best_answer["text"]
        # else:
        answer = best_answer["text"] if best_answer["score"] > min_null_score else ""
        predictions[example["id"]] = answer

    return predictions

def evaluate_qa_predictions(tokenizer, raw_dataset, preprocessed_dataset, raw_predictions, n_best_size = 20, max_answer_length = 30):
    tagger = fugashi.Tagger('-d "{}"'.format(unidic_lite.DICDIR))

    def normalize_answer(text):
        """Lower text and remove punctuation, articles and extra whitespace."""

        normalized = unicodedata.normalize('NFKC', text)
        tokenized = [word.surface for word in tagger(normalized) if '記号' not in word.feature.pos1]

        return " ".join(tokenized)

    final_predictions = postprocess_qa_predictions(tokenizer, raw_dataset, preprocessed_dataset, raw_predictions, n_best_size = n_best_size, max_answer_length = max_answer_length)
    formatted_predictions = [{"id": k, "prediction_text": normalize_answer(v)} for k, v in final_predictions.items()]
    raw_dataset = raw_dataset.map(lambda x: {"answers": {
        "answer_start": x["answers"]["answer_start"],
        "text": [normalize_answer(a) for a in x["answers"]["text"]]
    }})

    references = [{"id": example["id"], "answers": example["answers"]} for example in raw_dataset]
    metric = evaluate.load("squad")
    results = metric.compute(predictions=formatted_predictions, references=references)
    return results

def load_splits(
        parameters: str,
        tokenizer: AutoTokenizer=None
):
    
    dataset_kwargs = parameters["dataset_kwargs"]
    if dataset_kwargs.get("multi_dataset"):
        dataset_kwargs = [v for k, v in dataset_kwargs.items() if k != "multi_dataset"]
    else:
        dataset_kwargs = [dataset_kwargs]

    task = parameters["task"]

    def load_(split, columns, data_dir, task=task, preprocessed=False):
        if preprocessed:
            return load_dataset(os.path.join(data_dir, f"{split}.parquet"), output_type="Dataset")

        dataset = load_dataset(os.path.join(data_dir, f"{split}.parquet"), output_type="Dataset", columns=list(columns.values()) if columns else None)
        if columns and (columns.get("label") not in [None, "label"]):
            dataset = dataset.rename_column(columns["label"], "label")
        

        remove_columns = [col for col in columns.values() if col != columns.get("label")] if columns else None
                            
        tokenizer_kwargs = parameters.get("tokenizer_kwargs", {})
        if task in  ["MLM", "sequence_classification"]:
            tokenize_fn = lambda example: tokenizer(
                example[columns["text"]],
                **tokenizer_kwargs
            )
            return dataset.map(tokenize_fn, remove_columns=remove_columns) 

        elif task == "sequence_pair_classification":
            text1, text2 = columns["text1"], columns["text2"]

            tokenize_fn = lambda example: tokenizer(
                example[text1],
                example[text2],
                **tokenizer_kwargs
            )
            return dataset.map(tokenize_fn, remove_columns=remove_columns) 

        elif task == "multiple_choice":
            question = columns["question"]
            choices = [columns[choice] for choice in columns if "choice" in choice]

            tokenize_fn = lambda example: tokenizer(
                [example[question]]*len(choices),
                [example[c] for c in choices],
                return_tensors="pt",
                **tokenizer_kwargs
                )
            
            return dataset.map(tokenize_fn, remove_columns=remove_columns) 
        
        
        elif task == "JSQuAD":
            return preprocess_data_for_JSQuAD(dataset, tokenizer, **tokenizer_kwargs)
    
    tokenized_datasets = {}
    for kwargs in dataset_kwargs:
        splits = kwargs["splits"]
        data_dir = kwargs["data_dir"]
        
        for split in splits:
            name = split
            if kwargs.get("prefix"):
                name = f"{kwargs['prefix']}_{split}"

            columns = kwargs.get("columns")
            tokenized_datasets[name] = load_(split, columns, data_dir)

            if (task == "JSQuAD") and ("train" not in split):
                raw_dataset = load_dataset(
                    os.path.join(data_dir, f"{split}.parquet"),
                    output_type="Dataset", 
                    columns = ["id", "context", "answers"]
                    )
                tokenized_datasets[f"{name}_raw"] = raw_dataset
        
    def concat(split, tokenized_datasets):
        splits = [k for k in tokenized_datasets.keys() if split in k]
        if len(splits) <= 1:
            return tokenized_datasets
        else:
            combined = concatenate_datasets([tokenized_datasets[s] for s in splits]).shuffle()
            for s in splits:
                del tokenized_datasets[s]
            tokenized_datasets[split] = combined
            return tokenized_datasets
            
    tokenized_datasets = concat("train", tokenized_datasets)
    tokenized_datasets = concat("raw", tokenized_datasets)

    return tokenized_datasets

def get_study_name(config, group: str=None):
    if group:
        study_name = group
    else:
        study_name = config["fixed_parameters"]["group"]
    return study_name

def get_sampler(config):
    variable_parameters = config["variable_parameters"]

    search_type = variable_parameters["search_type"]
    if search_type == "TPE":
        sampler = optuna.samplers.TPESampler()
    if search_type == "random":
        sampler = optuna.samplers.RandomSampler()
    if search_type == "grid":
    
        search_field = variable_parameters["search_field"]
        def get_choices(parameter):
            param = search_field[parameter]
            type_ = search_field[parameter]["type"]
            if type_ in ["int", "float"]:
                start = param["low"]
                stop = param["high"] + param["step"]
                step = param["step"]
                choices = list(np.arange(start, stop, step))
            elif type_ == "categorical":
                choices = param["choices"]   
            return choices
        
        search_field = {k:get_choices(k) for k in search_field.keys()}
        sampler = optuna.samplers.GridSampler(search_field)
    return sampler

def get_data_collator(parameters, tokenizer):
    if parameters["task"] in ["sequence_classification", "sequence_pair_classification", "JSQuAD"]:
        return DataCollatorWithPadding(tokenizer=tokenizer)
    elif parameters["task"] == "MLM":
        return DataCollatorForLanguageModeling(tokenizer=tokenizer)
    elif parameters["task"] == "multiple_choice":
        return DataCollatorForMultipleChoice(tokenizer=tokenizer)


def get_model(parameters):
    adapter_model = True if parameters.get("adapter_kwargs") else False
    fusion_model = True if parameters.get("adapter_setup") else False
    model_kwargs = parameters.get("model_kwargs", {})

    config = AutoConfig.from_pretrained(parameters["path_to_model"], **model_kwargs)

    if not adapter_model:
        if parameters["task"] in ["sequence_classification", "sequence_pair_classification"]:
            model_class =  AutoModelForSequenceClassification
        elif parameters["task"] == "MLM":
            model_class = AutoModelForMaskedLM
        elif parameters["task"] == "multiple_choice":
            model_class = AutoModelForMultipleChoice
        elif parameters["task"] == "JSQuAD":
            model_class = AutoModelForQuestionAnswering
        model = model_class.from_pretrained(parameters["path_to_model"], ignore_mismatched_sizes = True, config=config)
        return model
        
    elif adapter_model:

        adapter_kwargs = parameters.get("adapter_kwargs", {})
        model = AutoAdapterModel.from_pretrained(parameters["path_to_model"], **adapter_kwargs.get("model_kwargs", {}))
        name = adapter_kwargs["name"]

        head_kwargs = adapter_kwargs.get("head_kwargs", {})
        task = parameters["task"]
        if task in ["sequence_classification", "sequence_pair_classification"]:
            model.add_classification_head(head_name=name, **head_kwargs)
        elif task == "multiple_choice":
            model.add_multiple_choice_head(head_name=name, **head_kwargs)
        elif task == "JSQuAD":
            model.add_qa_head(head_name=name, **head_kwargs)
        
        
        

        if not fusion_model:
            adapter_config = get_adapter_config(parameters)
            model.add_adapter(name, adapter_config)
            model.set_active_adapters(name)
            model.train_adapter(name)
            return model
        
        elif fusion_model:
            adapter_dir = parameters["path_to_adapters"]

            for adapter in parameters["adapter_setup"]:
                model.load_adapter(os.path.join(adapter_dir, adapter), with_head=False)

            adapter_setup = Fuse(*parameters["adapter_setup"])
            model.add_adapter_fusion(adapter_setup)
            model.set_active_adapters(adapter_setup)
            model.train_adapter_fusion(adapter_setup)

            return model


def get_optimizer(model, parameters, optimizer_state: str=None):

    optimizer = AdamW(
        params=model.parameters(),
        lr=parameters.get("learning_rate"),
        betas = (parameters.get("adam_beta1"), parameters.get("adam_beta2")),
        eps = parameters.get("adam_epsilon"),
        weight_decay = parameters.get("weight_decay", 0.0)
    )
    
    if optimizer_state:
        optimizer.load_state_dict(optimizer_state)

    return optimizer


def get_scheduler(train_dataset, parameters, optimizer, scheduler_state: str=None):


    lr_scheduler_type = parameters.get("lr_scheduler_type", "constant")
    batch_size = parameters.get("per_device_train_batch_size", 8)
    num_train_epochs = parameters.get("num_train_epochs", 1)
    num_cycles = parameters.get("num_cycles", 0.5)
    num_restarts = parameters.get("num_restarts", 0)
    warmup_steps = parameters.get("warmup_steps", 0)

    num_training_steps = len(train_dataset) // batch_size * num_train_epochs


    if lr_scheduler_type == "constant":
        scheduler = get_constant_schedule_with_warmup(
            optimizer=optimizer,
            num_warmup_steps=warmup_steps
        )
    elif lr_scheduler_type == "linear":
        scheduler = get_linear_schedule_with_warmup(
            optimizer=optimizer,
            num_warmup_steps=warmup_steps,
            num_training_steps= num_training_steps
        )
    
    elif lr_scheduler_type == "cosine":
        scheduler = get_cosine_schedule_with_warmup(
            optimizer=optimizer,
            num_warmup_steps=warmup_steps,
            num_training_steps= num_training_steps,
            num_cycles=num_cycles
        )
    elif lr_scheduler_type == "cosine_with_restarts":
        scheduler = get_cosine_with_hard_restarts_schedule_with_warmup(
            optimizer=optimizer,
            num_warmup_steps=warmup_steps,
            num_training_steps= num_training_steps,
            num_cycles=num_restarts
        )
    if scheduler_state:
        scheduler.load_state_dict(scheduler_state)

    return scheduler, parameters

def get_optimizers(model, parameters, train_dataset, last_checkpoint: str=""):
    optimizer_state, scheduler_state = None, None
    if last_checkpoint:
        optimizer_state = torch.load(os.path.join(last_checkpoint, "optimizer.pt"))
        scheduler_state = torch.load(os.path.join(last_checkpoint, "scheduler.pt"))

    optimizer = get_optimizer(model, parameters, optimizer_state)
    scheduler, parameters = get_scheduler(train_dataset, parameters, optimizer, scheduler_state)
    return (optimizer, scheduler), parameters

def get_current_epoch(last_checkpoint):
    return load_dict(os.path.join(last_checkpoint, "trainer_state.json"))["epoch"]

def get_paths(trial, parameters):
    join = lambda parent, child: os.path.join(parent, child)
    start = parameters["trial_number_start"] if "trial_number_start" in parameters.keys() else 1
    trial_number = str(trial.number+start).zfill(3)
    
    run_name = join(parameters["group"], f"trial-{trial_number}")
    dir_path = join(parameters["project"], run_name)

    paths = {
        "run_name": run_name,
        "trial_checkpoint": join(parameters["checkpoint_dir"], dir_path),
        "trial_complete": join(parameters["completed_dir"], dir_path)
    }
    return paths

def retrieve_paths(trial_checkpoint, config):
    join = lambda parent, child: os.path.join(parent, child)
    parent = lambda path: os.path.dirname(path)

    parameters = config["fixed_parameters"]

    trial_name = basename(trial_checkpoint)
    group = basename(parent(trial_checkpoint))
    project = basename(parent(parent(trial_checkpoint)))


    run_name = f"{group}/{trial_name}"
    run_path = f"{project}/{run_name}"

    paths = {
        "run_name": run_name,
        "trial_checkpoint": trial_checkpoint,
        "trial_complete": join(parameters["completed_dir"], run_path),
        "last_checkpoint": get_last_checkpoint(trial_checkpoint)
    }
    return paths


def get_callbacks(
        parameters,
        pause_on_epoch: bool=False, 
        trial=None,
        should_prune: bool=False, 
        current_epoch: float=0.0
        ):
    choices = parameters["callbacks"]

    callbacks = []
    if "early_stopping" in choices:
        patience = parameters["patience"]
        callbacks.append(EarlyStoppingCallback(early_stopping_patience=patience))
        print(f"EarlyStopping enabled. {patience=}")
    
    if "optuna" in choices:
        callbacks.append(OptunaCallback(trial, should_prune=should_prune))
        print(f"Optuna logging enabled. {should_prune=}")
    

    stop_epoch = parameters["num_train_epochs"]
    if pause_on_epoch:
        stop_epoch = int(current_epoch) + 1
        if stop_epoch< parameters["num_train_epochs"]:
            callbacks.append(StopCallback())
            print(f"Training will pause when epoch = {stop_epoch}.")
        else:
            print("Training will run to completion.")
    
    return callbacks, stop_epoch


def configure_dropout(model, config, parameters):
    dropout_parameters = [key for key in parameters.keys() if "dropout" in key]
    if not dropout_parameters:
        return model, config, parameters
    else:
        get = lambda parameter: parameters[parameter] if parameter in parameters.keys() else None
        def update(model, name, value): 
            model.config.update({name: value})
            parameters[name] = value
            return model, config, parameters

        for dropout in ["hidden_dropout_prob", "attention_probs_dropout_prob", "classifier_dropout"]:
            model, config, parameters = update(model, dropout, get(dropout))

        fixed_parameters, variable_parameters = config["fixed_parameters"], config["variable_parameters"]["search_field"]
        listify = lambda parameter: parameter if type(parameter) == list else [parameter]
        dropout_type = get("dropout_type")
        choice=None


        if "dropout_type" in fixed_parameters.keys():
            choice = listify(dropout_type)

        elif "dropout_type" in variable_parameters.keys():
            if dropout_type:
                label2choice = variable_parameters["dropout_type"]["label2choice"]
                choice = listify(label2choice[dropout_type])

        if choice:
            if "hidden" in choice:
                model, config, parameters = update(model, "hidden_dropout_prob", get("dropout_prob"))
            if "attention" in choice:
                model, config, parameters = update(model, "attention_probs_dropout_prob", get("dropout_prob"))
            if "classifier" in choice:
                model, config, parameters = update(model, "classifier_dropout", get("dropout_prob"))
                
        else:
            model, config, parameters = update(model, "dropout_prob", None)
    return model, config, parameters


def configure_training_args(
        parameters,
        paths,
        train_dataset
):
    if parameters.get("interval"):
        evaluation_strategy = save_strategy = "steps"
        eval_steps = save_steps = 1 / parameters["interval"] / parameters["num_train_epochs"]
    else:
        evaluation_strategy = save_strategy = "epoch"
        eval_steps = save_steps = 1
    
    if parameters.get("eval_delay") and evaluation_strategy == "steps":
        parameters["eval_delay"] = len(train_dataset) // parameters["per_device_train_batch_size"] * parameters["eval_delay"]
    
    if parameters.get("warmup_epochs"):
        warmup_steps = parameters["warmup_epochs"] * len(train_dataset) // parameters["per_device_train_batch_size"]
        parameters["warmup_steps"] = warmup_steps
    
    if parameters.get("warmup_ratio"):
        warmup_steps = parameters["warmup_ratio"] * parameters["num_train_epochs"] * len(train_dataset) // parameters["per_device_train_batch_size"]
        parameters["warmup_steps"] = warmup_steps


    training_args = CustomTrainingArguments(
        adam_beta1=parameters.get("adam_beta1"),
        adam_beta2=parameters.get("adam_beta2"),
        adam_epsilon=parameters.get("adam_epsilon"),
        eval_steps=eval_steps,
        eval_delay = parameters.get("eval_delay", 0),
        evaluation_strategy=evaluation_strategy,
        logging_steps= parameters.get("logging_steps", 500),
        learning_rate=parameters.get("learning_rate", 1e-5),
        load_best_model_at_end=parameters.get("load_best_model_at_end", False),
        lr_scheduler_type=parameters.get("lr_scheduler_type", "constant"),
        metric_for_best_model=parameters.get("metric_for_best_model", "loss"),
        num_train_epochs=parameters.get("num_train_epochs", 1),
        output_dir=paths["trial_checkpoint"],
        per_device_train_batch_size=parameters.get("per_device_train_batch_size", 8),
        per_device_eval_batch_size=parameters.get("per_device_eval_batch_size", 8),
        push_to_hub=parameters.get("push_to_hub", False),
        report_to=parameters.get("report_to", ["none"]),
        save_strategy=save_strategy,
        save_steps=save_steps,
        save_total_limit=parameters.get("save_total_limit", 2),
        warmup_ratio=parameters.get("warmup_ratio", 0.0),
        warmup_steps=parameters.get("warmup_steps", 0),
        wandb_run_id=parameters.get("wandb_run_id", None),
        weight_decay=parameters.get("weight_decay", 0)
        )
    
    return training_args, parameters


def suggest_parameter(trial, search_space, param_name):

            param_space = search_space[param_name]
            dtype = param_space["type"]
            if dtype == "fixed":
                return param_space["value"]
            elif dtype == "categorical":
                return trial.suggest_categorical(
                    name=param_name,
                    choices=param_space["choices"])
            elif dtype == "int":
                suggest_method = trial.suggest_int
            elif dtype == "float":
                suggest_method = trial.suggest_float
            else:
                raise ValueError("Please input a valid parameter type. Either 'fixed', 'categorical', 'int' or 'float'.")
            if "step" in param_space.keys():
                    return suggest_method(
                        name=param_name,
                        low=param_space["low"],
                        high=param_space["high"],
                        step=param_space["step"]
                    )
            elif "log" in param_space.keys():
                return suggest_method(
                    name=param_name,
                    low=param_space["low"],
                    high=param_space["high"],
                    log=param_space["log"]
                )
            else:
                return suggest_method(
                    name=param_name,
                    low=param_space["low"],
                    high=param_space["high"]
                )

def compile_parameters(search_space, trial):
    param_names = [name for name in search_space.keys() if name != "meta"]
    parameters = {name: suggest_parameter(trial, search_space, name) for name in param_names}
    return parameters

def init_parameters(trial, config, override_parameters={}, group: str=None):
    fixed_parameters = config["fixed_parameters"]
    if group:
        group_parameters = config["group_parameters"][group]
        group_parameters["group"] = group
    else:
        group_parameters = {}


    search_field = config["variable_parameters"]["search_field"]
    
    suggest = lambda variable: suggest_parameter(trial, search_field, variable)
    variable_parameters = {variable: suggest(variable) for variable in search_field.keys()}

    parameters = {**fixed_parameters, **group_parameters, **variable_parameters, **override_parameters}

    if "report_to" in parameters.keys():
        if type(parameters["report_to"]) == str:
            parameters["report_to"] = [parameters["report_to"]]
    return parameters

def init_wandb(parameters, paths, reinit: bool=False):
    trial_checkpoint, run_name = paths["trial_checkpoint"], paths["run_name"]
    project, group, entity = parameters["project"], parameters["group"], parameters["entity"]
    parameters["wandb_url"] = f"https://wandb.ai/{entity}/{project}/runs/{run_name}"

    if not reinit:
        os.makedirs(trial_checkpoint, exist_ok=True)
        wandb_run_id = wandb.util.generate_id()
        parameters["wandb_run_id"] = wandb_run_id

        wandb.init(
            project=project,
            id=parameters["wandb_run_id"],
            group=group,
            entity=entity,
            name=run_name,
            resume="allow",
            config=parameters,
            reinit=True
        )

    else:
        wandb_run_id = parameters["wandb_run_id"]

        wandb.init(
            project= project,
            id=wandb_run_id,
            resume="must"
            )
    return parameters

def print_parameters(config, parameters):
    
    print("\nFixed Params:")
    for key in config["fixed_parameters"].keys():
        print(f"{key}: {parameters[key]}")

    if "group_parameters" in config.keys():
        print("\nGroup Params:")
        groups = list(config["group_parameters"].keys())
        for key in config["group_parameters"][groups[0]].keys():
            print(f"{key}: {parameters[key]}")

    print("\nVariable Params:")
    for key in config["variable_parameters"]["search_field"].keys():
        if key in parameters.keys():
            print(f"{key}: {parameters[key]}")

    return

def print_run_init(model, config, parameters, paths, reinit: bool=False):
    teacher_model = True if parameters.get("path_to_teacher_model") else False
    if teacher_model:
        print("Teacher Model:", model.teacher_model.config)
        print("Trainee Model:", model.trainee_model.config)
    else:
        print("\n", model.config)
    print_parameters(config, parameters)

    if parameters.get("wandb_url", None):
        print("Wandb URL:", parameters["wandb_url"])
    if not reinit:
        print(f"Beginning {basename(paths['trial_checkpoint'])}. . .")

    else:
        print(f"Resuming {basename(paths['trial_checkpoint'])}. . .")
    return


def get_trainer(
        model,
        args,
        data_collator,
        datasets,
        tokenizer,
        compute_metrics,
        optimizers,
        callbacks,
        parameters
):
    adapter_model = True if parameters.get("adapter_kwargs") else False

    if parameters["dataset_kwargs"].get("multi_dataset"):
        if adapter_model:
            return ValueError("Multi-dataset training not supported with adapter models.")
        
        eval_datasets = [(dataset, name.split("_")[0]) for name, dataset in datasets.items() if "validation" in name]
        eval_dataset = concatenate_datasets([dataset for dataset, name in eval_datasets])

        trainer = MultiDatasetTrainer(
            model=model,
            args=args,
            data_collator=data_collator,
            train_dataset=datasets["train"],
            eval_dataset=eval_dataset,
            eval_datasets=eval_datasets,
            tokenizer=tokenizer,
            compute_metrics=compute_metrics,
            optimizers=optimizers,
            callbacks=callbacks
        )

    else:
        trainer_args= dict(
            model=model,
            args=args,
            data_collator=data_collator,
            train_dataset=datasets["train"],
            eval_dataset=datasets["validation"],
            tokenizer=tokenizer,
            compute_metrics=compute_metrics,
            optimizers=optimizers,
            callbacks=callbacks
        )

        trainer_class = AdapterTrainer if adapter_model else Trainer
        trainer = trainer_class(**trainer_args)
    
    return trainer
     

def init_run(
        trial, 
        config: dict, 
        datasets: dict,
        tokenizer,
        group: str="", 
        override_parameters: dict={}, 
        pause_on_epoch: bool=False, 
        should_prune: bool=False):
    
    device = "cuda" if torch.cuda.is_available() else RuntimeError("No GPU available.")
    parameters = init_parameters(
        trial, 
        config,
        override_parameters=override_parameters,  
        group=group)
    paths = get_paths(trial, parameters)
    model = get_model(parameters)
    data_collator = get_data_collator(parameters, tokenizer)
    model, config, parameters = configure_dropout(model, config, parameters)
    model.to(device)

    if "wandb" in list(parameters["report_to"]) :
        parameters = init_wandb(parameters, paths)

    training_args, parameters = configure_training_args(parameters, paths, datasets["train"])
    optimizers, parameters = get_optimizers(model, parameters, datasets["train"])
    if parameters.get("warmup_steps", None):
        training_args.warmup_steps = parameters["warmup_steps"]
    
    compute_metrics = get_compute_metrics(parameters, tokenizer, datasets)

    callbacks, stop_epoch = get_callbacks(
        parameters, 
        pause_on_epoch=pause_on_epoch,
        trial=trial,
        should_prune=should_prune)

    trainer = get_trainer(
        model,
        training_args,
        data_collator,
        datasets,
        tokenizer,
        compute_metrics,
        optimizers,
        callbacks,
        parameters
    )

    print_run_init(
        model, 
        config, 
        parameters,
        paths
        )
    
    return parameters, paths, trainer, stop_epoch

def get_last_checkpoint(trial_checkpoint: str):

    checkpoints = [os.path.join(trial_checkpoint, checkpoint) for checkpoint in os.listdir(trial_checkpoint) if os.path.isdir(os.path.join(trial_checkpoint, checkpoint))]
    return max(checkpoints, key=os.path.getctime)

def retrieve_parameters(trial_checkpoint, config, override_parameters={}):

    paths= retrieve_paths(trial_checkpoint, config)
    get = lambda target: os.path.join(paths["last_checkpoint"], target)
    training_args = torch.load(get("training_args.bin"))
    training_args_dict = {k:v for k,v in training_args.__dict__.items() if k != "callbacks"}

    model_config = load_dict(get("config.json"))
    parameters = {**config["fixed_parameters"], **training_args_dict, **model_config, **override_parameters}
    tokenizer = AutoTokenizer.from_pretrained(parameters["path_to_model"])

    model = get_model(parameters)
    data_collator = get_data_collator(parameters, tokenizer)
    model.config.update(model_config)

    device = "cuda" if torch.cuda.is_available() else RuntimeError("No GPU available.")
    model.to(device)
    return paths, training_args, parameters, tokenizer, model, data_collator

def reinit_run(
        trial_checkpoint, 
        config, 
        override_parameters: dict={},
        pause_on_epoch: bool=False
        ):
    
    paths, training_args, parameters, tokenizer, model, data_collator = retrieve_parameters(
        trial_checkpoint, 
        config,
        override_parameters=override_parameters)
    
    datasets = load_splits(
        parameters=parameters,
        tokenizer=tokenizer
        )
    
    
    optimizers, parameters = get_optimizers(model, parameters, datasets["train"], paths["last_checkpoint"])
    callbacks, stop_epoch = get_callbacks(
        parameters,
        pause_on_epoch=pause_on_epoch,
        current_epoch=get_current_epoch(paths["last_checkpoint"])
    )

    compute_metrics = get_compute_metrics(parameters, tokenizer, datasets)

    if "wandb" in list(parameters["report_to"]):
        init_wandb(parameters, paths, reinit=True)

    trainer = get_trainer(
        model,
        training_args,
        data_collator,
        datasets,
        tokenizer,
        compute_metrics,
        optimizers,
        callbacks,
        parameters
    )

    print_run_init(
        model,
        config,
        parameters,
        paths,
        reinit=True
    ) 
    return paths, parameters, datasets, trainer, stop_epoch

def check_if_complete(trainer, parameters, stop_epoch):
    def early_stopping_triggered():
        if "early_stopping" in parameters["callbacks"]:
            return trainer.state.epoch < stop_epoch
        else:
            return False
        
    current_epoch = trainer.state.epoch
    if early_stopping_triggered():
        print("EarlyStoppingCallback triggered.")
        complete = True

    elif current_epoch == parameters["num_train_epochs"]:
        print("Training complete.")
        complete = True
    else:
        complete = False
        print(f"Training paused. {current_epoch=}.")
    return complete

def complete_trial (
        trainer, 
        datasets,
        parameters, 
        paths
        ):
    
    trial_checkpoint, trial_complete = paths["trial_checkpoint"], paths["trial_complete"]
 # Handling development datasets
    if "development" in datasets:
        trainer.eval_dataset = datasets["development"]
    else:
        dev_datasets = [(ds, name.split("_")[0]) for name, ds in datasets.items() if "development" in name]
        if dev_datasets:
            trainer.eval_datasets = dev_datasets
            trainer.eval_dataset = concatenate_datasets([ds for ds, _ in dev_datasets])

    # Handling test datasets
    if "test" in datasets:
        trainer.eval_dataset = datasets["test"]
    else:
        test_datasets = [(ds, name.split("_")[0]) for name, ds in datasets.items() if "test" in name]
        if test_datasets:
            trainer.eval_datasets = test_datasets
            trainer.eval_dataset = concatenate_datasets([ds for ds, _ in test_datasets])

    # Additional task-specific configurations
    if parameters.get("task") == "JSQuAD":
        trainer.compute_metrics = get_compute_metrics(parameters, trainer.tokenizer, datasets, eval_split="development")

    # Run evaluation
    results = trainer.evaluate()
        
    print("\nResults:", results)

    trainer.save_model(trial_complete)
    if "wandb" in parameters["report_to"]:
        wandb.log(results)
        wandb.finish()
    #deletes the trial directory
    shutil.rmtree(trial_checkpoint)

    get = lambda parameter: parameters[parameter] if parameter in parameters.keys() else None
    if get("metric_for_best_trial"):
        trial_value = results[get("metric_for_best_trial")]
    elif get("metric_for_best_model"):
        trial_value = results[get("metric_for_best_model")]
    else:
        trial_value = results["eval_loss"] 
    return trial_value

def launch_study(
        config, 
        path_to_storage, 
        override_parameters: dict={},  
        group: str=""):

    if group:
        parameters = {**config["fixed_parameters"], **config["group_parameters"][group], **{"group": group}}
    else:
        parameters = config["fixed_parameters"]
    
    if override_parameters:
        parameters = {**parameters, **override_parameters}
    
    if parameters["metric_for_best_trial"] in ["accuracy", "eval_accuracy"]:
        direction = "maximize"

    elif parameters["metric_for_best_trial"] in ["loss", "eval_loss"]:
        direction = "minimize"

    path_to_model = parameters["path_to_teacher_model"] if parameters.get("path_to_teacher_model") else parameters["path_to_model"]
    tokenizer = AutoTokenizer.from_pretrained(path_to_model)

    datasets = load_splits(
        parameters=parameters,
        tokenizer=tokenizer
        )
    

    study = optuna.create_study(
        storage=path_to_storage,
        sampler=get_sampler(config),
        study_name=parameters["group"],
        direction=direction,
        load_if_exists=True,
        )
    
    return tokenizer, datasets, study