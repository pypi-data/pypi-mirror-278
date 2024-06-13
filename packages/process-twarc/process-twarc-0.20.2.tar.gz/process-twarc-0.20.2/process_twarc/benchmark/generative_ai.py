import json
import pandas as pd
from process_twarc.util import load_dict, load_dataset, make_dir, save_dict
import re
import os
import numpy as np
from sklearn.metrics import f1_score
from collections import Counter
import math
import torch
from datasets import concatenate_datasets, Dataset
import time

def get_template(lang):
    if lang == "en":
        template = {
            "instructions": {
                "Task": "Sentiment Classification. Read the following Tweet and classify the sentiment as Positive, Negative, or Neutral. It is crucial to accurately understand the nuances of the language to perform this classification.",
                "Labels": [
                    "Positive: Positive sentiment refers to expressions of happiness, approval, or optimism in the text. While the text might contain mixed sentiments, the dominant sentiment is positive.",
                    "Negative: Negative sentiment refers to expressions of sadness, disapproval, or pessimism in the text. The text primarily conveys adverse emotions or opinions.",
                    "Neutral: Neutral sentiment signifies the absence of any strong emotions, opinions, or bias in the text. It represents factual or objective statements."
                ]
            },
            "slotfill_txt": {
                "examples": "Examples",
                "input": "Input",
                "output": "Output",
                "end-single": "What is the sentiment of this tweet? (positive, negative, neutral). You must respond with a single word.",
                "end-batch": "What are the sentiments of these tweets? You must return your answer as JSON object. The tweet_id must be indentical to the input tweet_id."
                }
        }
    elif lang == "ja":
        template = {
            "instructions": {
                "Task": "センチメントの分類 次の日本語のツイートを読んで、センチメントをポジティブ、ネガティブ、ニュートラルのいずれかに分類してください。この分類を行うには、日本語のニュアンスを正確に理解することが重要です。",
                "Labels": [
                    "ポジティブ: 肯定的な感情とは、文章中の幸福、承認、楽観の表現を指す。テキストには様々な感情が含まれているかもしれないが、支配的な感情はポジティブである。",
                    "ネガティブ: 否定的な感情とは、文章中の悲しみ、不承認、悲観の表現を指す。主に不利な感情や意見を伝えている。",
                    "ニュートラル: 中立的な感情とは、文章に強い感情や意見、偏見がないことを意味する。事実や客観的な記述を表します。"
                ]
            },
            "slotfill_txt": {
                "examples": "例",
                "input": "入力",
                "output": "出力",
                "end-single": "このツイートの感情は何ですか？ (ポジティブ、ネガティブ、ニュートラル). 回答は一言に限る。",
                "end-batch": "これらのツイートの感情は何ですか？ 必ずJSONオブジェクトとして返してください。tweet_idは入力のtweet_idと同じでなければなりません。"
            }
        }
    return template

def prompt_for_few_shot_classification(
    datasets: dict,
    params: dict,
    column_dict: dict,
    ):
    
    eos_token = params.get("eos_token", "")
    lang = params.get("lang", "en")
    template = get_template(lang)
    instructions, txt = template["instructions"], template["slotfill_txt"]

    id = column_dict["id"]
    text = column_dict["text"]

    def get_samples(datasets, n_examples_per_class=2, batch_size=1):
        all, response = datasets["all"], datasets["response"]
        test = all[~all[id].isin(response[id])].reset_index(drop=True) if not response.empty else all


        test = test.sample(min(batch_size, (test.shape[0]))).reset_index(drop=True)
        train = all[~all[id].isin(test[id])].reset_index(drop=True)
        examples = train.groupby("label").apply(lambda x: x.sample(n_examples_per_class)).sample(frac=1).reset_index(drop=True)

        samples = {
            "train": examples,
            "test": test
        }
        return samples

    def init_prompt(instructions=instructions):
        prompt = []
        for key, value in instructions.items():
            prompt.append(key + ":\n\n")
            if isinstance(value, dict):
                for k, v in value.items():
                    prompt.append(k + ":\n")
                    prompt.append(json.dumps(v, ensure_ascii=False) + "\n")
            elif isinstance(value, list):
                for item in value:
                    prompt.append(item + "\n")
            elif isinstance(value, str): 
                prompt.append(value + "\n")
            prompt.append("\n")
        
        prompt = "".join(prompt)
        return prompt

    def get_examples(
            prompt,
            samples,
            txt=txt,
            batch_size=params.get("batch_size", 1),
            strategy=params.get("strategy", "batch")
            ):

        train = samples["train"] 
        if strategy == "batch":
            train["batch"] = train.index // batch_size
            for batch in train["batch"].unique():

                prompt += f"{txt['input']}:\n\n```\n"
                for _, row in train[train["batch"] == batch].iterrows():
                    prompt += json.dumps(row[[id, text]].to_dict(), ensure_ascii=False)
                    prompt += "\n"
                prompt += "```\n\n"

                prompt += f"{txt['end-batch']}\n\n"
                prompt += f"{txt['output']}:\n\n```\n"
                for _, row in train[train["batch"] == batch].iterrows():
                    prompt += json.dumps(row[[id, "label"]].to_dict(), ensure_ascii=False)
                    prompt += "\n"
                prompt += "```\n\n"
                if eos_token:
                    prompt += f"{eos_token}\n\n"

        elif params["strategy"] == "single":
            prompt += f"{txt['examples']}:\n\n```"

            for _, row in train.iterrows():
                prompt += f"tweet:\n{row[text]}\n\n"
                prompt += f"label:\n{row['label']}{eos_token}\n\n"
            prompt += "```\n\n"
        return prompt
        
    def get_test_data(
            prompt,
            samples,
            txt=txt,
            strategy=params.get("strategy", "batch")
    ):
        
        test = samples["test"] 
        test_ids = test[id].tolist()

        if strategy == "single":
            prompt += f"tweet:\n{test[text].values[0]}\n\n"
            prompt += f"{txt['end-single']}\n\n"
        
        elif strategy == "batch":
            prompt += f"{txt['input']}:\n\n```"
            for _, row in test.iterrows():
                prompt += json.dumps(row[[id, text]].to_dict(), ensure_ascii=False)
                prompt += "\n"
            prompt += "```\n\n"
            prompt += f"{txt['end-batch']}\n\n"
            prompt += f"{txt['output']}:\n\n```"

        return prompt, test_ids

    samples = get_samples(
        datasets, 
        n_examples_per_class=params.get("n_examples_per_class", 2), 
        batch_size=params.get("batch_size", 1))
    prompt = init_prompt()
    prompt = get_examples(prompt, samples)
    prompt, test_ids = get_test_data(prompt, samples)
    return prompt, test_ids

def extract_label(response):
    # Compile regex pattern to match expected labels, allowing for non-alphanumeric characters surrounding the label
    pattern = re.compile(r'(positive|negative|neutral|ポジティブ|ネガティブ|ニュートラル)', re.IGNORECASE)
    
    # Find all occurrences of any of the labels
    matches = pattern.findall(response)
    
    # Convert all matches to lower case to ensure consistent formatting
    lower_case_matches = [match.lower() for match in matches]
    
    # Count occurrences of each label
    if lower_case_matches:
        label_counts = Counter(lower_case_matches)
        # Retrieve the two most common labels
        most_common_labels = label_counts.most_common(2)
        # Check if there is a tie
        if len(most_common_labels) > 1 and most_common_labels[0][1] == most_common_labels[1][1]:
            return None  # There's a tie for the most common label
        else:
            return most_common_labels[0][0]  # Return the most common label
    else:
        # Return None if no labels are found
        return None

def batch_response_to_df(response, column_dict):
    id = column_dict["id"]
    # Remove excessive whitespace
    formatted_str = re.sub(r'\s+', ' ', response).strip()

    # First strategy: Find all objects enclosed in braces
    object_list = re.findall(r'\{.*?\}', formatted_str)
    valid_objects = []
    for obj_str in object_list:
        try:
            json_obj = json.loads(obj_str)
            valid_objects.append(json_obj)
        except json.JSONDecodeError:
            continue

    # Try to create DataFrame from JSON objects
    try:
        df = pd.DataFrame(valid_objects)
        if id in df.columns and "label" in df.columns:
            df[id] = df[id].astype(str)
            df.rename(columns={"label": "prediction"}, inplace=True)
            return df[[id, "prediction"]]
    except Exception:
        pass  # If failed, move to the second strategy

    # Second strategy: Split into new lines and use regex
    lines = response.split('\n')
    ids = []
    labels = []

    id_pattern = re.compile(r'(\d+)')
    label_pattern = re.compile(r'(positive|negative|neutral|ポジティブ|ネガティブ|ニュートラル)', re.IGNORECASE)

    for line in lines:
        id_match = id_pattern.search(line)
        label_match = label_pattern.search(line)
        if id_match and label_match:
            ids.append(id_match.group(1))
            labels.append(label_match.group(0))

    if ids and labels:
        df = pd.DataFrame({
            id: ids,
            "predicted_label": labels
        })
        df[id] = df[id].astype(str)
        return df

    return None

def format_response(response, test_ids, strategy, column_dict):
    id = column_dict["id"]
    if strategy == "single":
        label = extract_label(response)
        if not label:
            return pd.DataFrame()
        output = pd.DataFrame({
            id: test_ids,
            "predicted_label": [label]
        })
    
    elif strategy == "batch":
        output = batch_response_to_df(response, column_dict=column_dict)
        if output is None:
            return pd.DataFrame()
        output = output[output[id].isin(test_ids)] 
    return output

def init_prompt_response_io(
        model_name: tuple,
        path_to_api_key: str,
        model_dir: str,
        params: dict
):
    def get_system_prompt(
            strategy = params.get("strategy", "batch"),
            lang = params.get("lang", "en")
        ):
        prompts = {
            "single": {
                "en": "You must respond with a single word. (positive, negative, neutral)",
                "ja": "回答は一言に限る。 (ポジティブ、ネガティブ、ニュートラル)"
            },
            "batch": {
                "en": "You must return your answer as JSON object. The tweet_id must be indentical to the input tweet_id.",
                "ja": "必ずJSONオブジェクトとして返してください。tweet_idは入力のtweet_idと同じでなければなりません。"
            }
        }
        return prompts[strategy][lang]


    system_prompt = get_system_prompt()
    generation_kwargs = params.get("generation_kwargs", {})
    
    def init_hf_model():
        from transformers import AutoModelForCausalLM, AutoTokenizer

        path_to_model = os.path.join(model_dir, model_name[0], model_name[1])
        tokenizer = AutoTokenizer.from_pretrained(path_to_model)
        model = AutoModelForCausalLM.from_pretrained(path_to_model, torch_dtype = "auto")

        if torch.cuda.is_available():
            model = model.to("cuda")
        
        
        return model, tokenizer
    
    
    if model_name[0] == "openai":
        import openai

        openai.api_key = load_dict(path_to_api_key)["api_key"]

        get_response = lambda prompt: openai.ChatCompletion.create(
            model=model_name[1],
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
                ],
            **generation_kwargs
        ).choices[0].message["content"]
    
        return get_response
    
    elif model_name[0] == "google":
        import vertexai
        from vertexai.preview.generative_models import GenerativeModel
        from vertexai.preview.generative_models import GenerationConfig
        api_key = load_dict(path_to_api_key)

        vertexai.init(project = api_key["project_id"], location = api_key["location"])

        def get_response(prompt: str):
            model = GenerativeModel(
                model_name[1],
                generation_config = GenerationConfig(**generation_kwargs))
            chat = model.start_chat(response_validation=False)
            response = chat.send_message(prompt).text
            return response
        return get_response

    elif model_name[0] in ["meta", "mistralai"]:
        print("Using Replicate API")

        import replicate

        os.environ["REPLICATE_API_TOKEN"] = load_dict(path_to_api_key)["api_key"]

        def get_response(prompt: str):

            response = replicate.run(
                "/".join(model_name),
                input={"prompt": prompt, **generation_kwargs}
            )

            response = "".join(response)
            return response
        return get_response
    
    elif model_name[0] in ["tokyotech-llm", "stabilityai", "ELYZA"]:

        B_INST, E_INST = "[INST]", "[/INST]"
        B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"

        model, tokenizer = init_hf_model()
        
        def get_response(prompt: str, model=model):
            formatted_prompt = "{bos_token}{b_inst} {system}{prompt} {e_inst} ".format(
                bos_token=tokenizer.bos_token,
                b_inst=B_INST,
                system=f"{B_SYS}{system_prompt}{E_SYS}",
                prompt=prompt,
                e_inst=E_INST,
            )

            with torch.no_grad():
                token_ids = tokenizer.encode(formatted_prompt, add_special_tokens=False, return_tensors="pt")

                output_ids = model.generate(
                    token_ids.to(model.device),
                    pad_token_id=tokenizer.pad_token_id,
                    eos_token_id=tokenizer.eos_token_id,
                    **generation_kwargs
                )
            response = tokenizer.decode(output_ids.tolist()[0][token_ids.size(1) :], skip_special_tokens=True)
            return response
    
    elif model_name[0] in  ["haqishen", "alfredplpl"]:

        model, tokenizer = init_hf_model()
        
        def get_response(prompt: str, model=model, tokenizer=tokenizer):
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]

            input_ids = tokenizer.apply_chat_template(
                messages,
                add_generation_prompt=True,
                return_tensors="pt"
            ).to(model.device)

            terminators = [
                tokenizer.eos_token_id
            ]

            if params.get("eos_token", None):
                terminators.append(tokenizer.convert_tokens_to_ids(params["eos_token"]))

            outputs = model.generate(
                input_ids,
                eos_token_id=terminators,
                pad_token_id=tokenizer.pad_token_id,
                attention_mask=torch.ones_like(input_ids),
                **generation_kwargs
            )

            response = outputs[0][input_ids.shape[-1]:]
            response = tokenizer.decode(response, skip_special_tokens=True)
            return response
    
    
    elif model_name[0] == "lightblue":
        from vllm import LLM, SamplingParams

        path_to_model = os.path.join(model_dir, model_name[0], model_name[1])
        llm = LLM(model=path_to_model)
        sampling_params = SamplingParams(**generation_kwargs)

        def get_response(prompt: str, llm=llm):
            output = llm.generate(prompt, sampling_params)
            response = output[0].outputs[0].text
            return response

    return get_response

def get_evaluation_metrics(params, output, output_dir, n_calls, min_calls):
    metrics = {
            "accuracy": (output["label"] == output["predicted_label"]).mean(),
            "macro_f1": f1_score(output["label"], output["predicted_label"], average="macro"),
            "micro_f1": f1_score(output["label"], output["predicted_label"], average="micro"),
            "weighted_f1": f1_score(output["label"], output["predicted_label"], average="weighted"),
            "n_calls": n_calls,
            "min_calls": min_calls
    }
    for label in output["label"].unique():
        metrics[f"{label}_f1"] = f1_score(output["label"] == label, output["predicted_label"] == label)

    metrics = {k:v.round(3) if isinstance(v, float) else v for k, v in metrics.items()}
    for k, v in metrics.items():
        print(f"{k}: {v}")
    
    output = {**metrics, **{"params": params}}
    save_dict(output, os.path.join(output_dir, "metrics.json"))

def build_confusion_matrix(output, id2label, output_dir):
    # Initialize the confusion matrix
    cm = np.zeros((len(id2label), len(id2label)))

    # Convert dataset columns to numpy arrays
    true_labels = np.array([label.lower() for label in output["label"].tolist()])
    predicted_labels = np.array([label.lower() for label in output["predicted_label"].tolist()])

    # Create label to index mapping
    label2idx = {v:k for k, v in id2label.items()}
    sorted_labels = [k for k, v in sorted(label2idx.items(), key=lambda x: x[1])]

    # Fill the confusion matrix
    for t, p in zip(true_labels, predicted_labels):
        cm[label2idx[t], label2idx[p]] += 1

    print(cm)
    # Save the confusion matrix and labels
    np.savez_compressed(os.path.join(output_dir, "cm.npz"), cm=cm, labels=sorted_labels)

def benchmark_gai_pipeline(
    data_dir: str,
    id2label: dict,
    column_dict: dict,
    model_name: tuple,
    path_to_api_key: str,
    model_dir: str,
    output_dir: str,
    params: dict,
    print_prompt: bool = False,
    print_response: bool = False,
    print_output: bool = False
):
    
    output_dir = os.path.join(output_dir, model_name[0], model_name[1])
    path_to_output = os.path.join(output_dir, "response.parquet")
    path_to_call_record = os.path.join(output_dir, "call_record.json")
    make_dir(output_dir)

    def load_datasets(
        data_dir = data_dir,
        column_dict = column_dict,
        id2label = id2label,
        path_to_output = path_to_output
        ):


        def load_ (split):
            dataset = load_dataset(
                file_path = os.path.join(data_dir, split),
                columns = list(column_dict.values())
            )
            dataset = dataset.rename(columns={column_dict["label"]: "label"})
            dataset["label"] = dataset["label"].map(id2label)
            return dataset
        
        datasets = {}
        datasets["all"] = pd.concat([load_(f"{split}.parquet") for split in ["test", "development"]]).reset_index(drop=True)
        datasets["response"] = load_dataset(path_to_output) if os.path.exists(path_to_output) else pd.DataFrame()
        return datasets
    
    def get_next_batch():
        datasets = load_datasets()
        response = datasets["response"]

        remainder = len(datasets["all"]) - len(response)
        if not remainder:
            print("All tweets have been classified")
            return None
        print(f"Remaining tweets: {remainder}")
        return datasets
    
    def get_min_calls(batch_size = params.get("batch_size", 1)):
        datasets = load_datasets()
        print(datasets)
        return math.ceil(datasets["all"].shape[0] / batch_size)
    
    def evaluate_response(n_calls, min_calls=get_min_calls()):
        def merge_response():
            datasets = load_datasets()
            if not "label" in datasets["response"].columns:
                output = datasets["test"].merge(datasets["response"], on=column_dict["id"])
                output.to_parquet(path_to_output, index=False)
            else:
                output = datasets["response"]
            return output
        
        output = merge_response()
        get_evaluation_metrics(params, output, output_dir, n_calls, min_calls)
        build_confusion_matrix(output, id2label, output_dir)

    datasets = get_next_batch()
    get_response = init_prompt_response_io(
        model_name=model_name, 
        path_to_api_key=path_to_api_key,
        model_dir=model_dir,
        params=params)
    
    print("Starting benchmarking pipeline")
    
    n_calls = 0
    if os.path.exists(path_to_call_record):
        call_record = load_dict(path_to_call_record)
        n_calls = call_record["n_calls"]
    

    while datasets is not None:
        prompt, test_id = prompt_for_few_shot_classification(
            datasets=datasets,
            params=params,
            column_dict=column_dict
            )
        if print_prompt:
            print(prompt)
        response = get_response(prompt)
        n_calls += 1
        save_dict({"n_calls": n_calls}, path_to_call_record)
        if print_response:
            print(response)
        output = format_response(response, test_id, params.get("strategy", "batch"), column_dict)
        output = output.merge(datasets["all"][[column_dict["id"], column_dict["text"], "label"]], on = column_dict["id"], how="left")
        if print_output:
            print(output)
        if output.empty:
            print("No response received")
            continue

        

        datasets["response"] = pd.concat([datasets["response"], output]).dropna().drop_duplicates(keep="first").reset_index(drop=True)
        datasets["response"].to_parquet(path_to_output, index=False)
        
        datasets = get_next_batch()
    evaluate_response(n_calls)
    
