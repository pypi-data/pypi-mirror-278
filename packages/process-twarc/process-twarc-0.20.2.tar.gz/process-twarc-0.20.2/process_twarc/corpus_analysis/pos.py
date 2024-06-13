from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer
from collections import Counter
from datasets import Dataset
import numpy as np
from fuzzywuzzy.process import extractOne
from process_twarc.util import load_dataset, get_files, get_output_path, save_to_parquet
from tqdm import tqdm
import json
import unidic_lite
import os
import pandas as pd
from typing import Union
from itertools import chain
import fugashi
import nltk

def upos_process(
        data_dir: str,
        tokenizers: dict [str, object],
        path_to_upos_model: str,
        intermediate_dir: str,
        masks = ["duplicate", "pattern"],
        test: bool = False,
        batch_number: int = None,
        batch_size: int = 10
):
    combine_dicts = lambda dict_list: dict(sum((Counter(d) for d in dict_list), Counter()))
    idx2pos = {
        0: 'ADJ',
        1: 'ADP',
        2: 'ADV',
        3: 'AUX',
        4: 'CCONJ',
        5: 'DET',
        6: 'INTJ',
        7: 'NOUN',
        8: 'NUM',
        9: 'PART',
        10: 'PRON',
        11: 'PROPN',
        12: 'PUNCT',
        13: 'SCONJ',
        14: 'SYM',
        15: 'VERB'
        }
    UPOS = list(idx2pos.values())
    pos2idx = {v: k for k, v in idx2pos.items()}


    def tags2onehot(
            tags: Union[str, list[str]], 
            pos2idx=pos2idx) -> list[int]:
        
        """helper function to convert pos tags to onehot encoding."""

        tags = [tags] if type(tags) == str else tags
        onehot = np.zeros(len(pos2idx))

        if tags:
            for key, value in Counter(tags).items():
                if not key:
                    continue
                index = pos2idx[key]
                onehot[index] = value
        return list(onehot)
        
    def get_upos_columns(
        dataset: Dataset,
        path_to_upos_model: str=path_to_upos_model
        ) -> Dataset:

        """Helper function that makes an inference on the text using the UPOS model."""

        upos_tokenizer = AutoTokenizer.from_pretrained(path_to_upos_model)
        dataset = dataset.map(lambda example: {"upos_tokens": upos_tokenizer.tokenize(example["text"])})
        pos = pipeline(
            task = "token-classification",
            model=AutoModelForTokenClassification.from_pretrained(path_to_upos_model),
            tokenizer= upos_tokenizer,
            device="cuda"
            )
        dataset = dataset.map(lambda example: {"upos_score": pos(example["text"])})
        return dataset

    def find_target_tokens(
        target_tokens: list[str], 
        upos_tokens: list[str]
        ) -> dict[str, dict[str, str]]:

        "Helper function to line up idexes of subwords from UPOS model and full words from other models"

        upos_tokens = list(enumerate(upos_tokens))
        target_tokens = list(target_tokens)
        #join tokens with ## stripped, if any
        get_word = lambda span: "".join([tok.replace("##", "") for (_, tok) in upos_tokens[span[0]:span[1]+1]])
        get_subwords = lambda span: {str(idx): {"token": upos_tokens[idx][1]} for idx in range(span[0], span[1]+1)}
        result = {}

        for target in target_tokens:
        
            start = target[0]
            end = target[-1]
            starts = [(idx, token) for (idx, token) in upos_tokens if token.startswith(start)]
            ends = [(idx, token) for (idx, token) in upos_tokens if token.endswith(end)]

            spans = []
            for (idx1, _) in starts:
                for (idx2, _) in ends:
                    if idx2 > idx1:
                        spans.append((idx1, idx2))

            entries = {str(span):
                    {
                        "word": get_word(span),
                        "subwords": get_subwords(span)
                    } for span in spans if get_word(span) == target}
            entries = {k: v for k, v in entries.items() if v}
            result.update(entries)
        
        result = {k: v for k, v in result.items() if v}
        return result

    def get_target_ids(
        dataset: Dataset, 
        tokenizers: dict
        ) -> pd.DataFrame:

        """Generates two columns. One is a list of tokens from test models. 
        The other lines up tokens from the UPOS model with the tokens from the test models."""

        dataset = get_upos_columns(dataset)
        
        for name, tokenizer in tokenizers.items():
            dataset = dataset.map(lambda example: {f"{name}_target_tokens": tokenizer.tokenize(example["text"])})
        
        df = dataset.to_pandas()
        for name in tokenizers.keys():
            df[f"{name}_targets"] = df.apply(lambda x: find_target_tokens(x[f"{name}_target_tokens"], x["upos_tokens"]), axis=1) 
        return df
    
    def generate_upos_onehots(
        dataset: Dataset, 
        tokenizers: dict=tokenizers) -> pd.DataFrame:

        """Generates a onehot encoding of UPOS tags for each word in the dataset."""
        
        extract_pos = lambda x: extractOne(x, UPOS)[0]
        df = get_target_ids(dataset, tokenizers)


        def dumps(idx, name, x):
            df.at[idx, f"{name}_result"] = json.dumps(x, ensure_ascii=False)
        
        for idx1, row in df.iterrows():
            for name, _ in tokenizers.items():

                score = row["upos_score"]
                tags = {
                        int(s["index"]):{
                            "word": s["word"],
                            "upos_score": {extract_pos(s["entity"]): 1},
                        } for s in score
                    } if isinstance(score, np.ndarray) else {}

                targets = row[f"{name}_targets"]

                result = {} 
                for span in targets.keys():
                    word = targets[span]
                    subwords = word["subwords"]
                
                    for idx2 in subwords:
                        subword = subwords[idx2]
                        upos_score = tags.pop(int(idx2)+1, {"upos_score": None}) if tags else {"upos_score": None}
                        subword["upos_score"] = upos_score["upos_score"]    

                    #get all_scores by creating a dictionary of all pos_scores, then summing the values for each key
                        
                    all_scores = [subword["upos_score"] for subword in subwords.values() if subword["upos_score"]]
                    if all_scores:
                        all_scores = combine_dicts(all_scores)


                    word["upos_onehot"] = tags2onehot(all_scores)
                    result[span] = word
                
                if tags:
                    for idx3 in tags.keys():

                        old_word = {idx3: {
                            "word": tags[idx3]["word"],
                            "upos_onehot": tags2onehot(tags[idx3]["upos_score"]),
                        }
                        }
                        result.update(old_word)
                
                dumps(idx1, name, result)
        return df

    def tabulate_onehots(
            df: pd.DataFrame, 
            tokenizers: dict=tokenizers) -> pd.DataFrame:
        
        """Tabulates the onehot encodings of UPOS tags for each word in the dataset."""
        
        output = {}
        for name, tokenizer in tokenizers.items():
            
            result = [json.loads(x) for x in df[f"{name}_result"]]
            df[f"{name}_result"] = result
            result = df[f"{name}_result"].apply(pd.Series).stack().to_frame().reset_index()
            get_column = lambda col: result[0].apply(lambda x: x[col] if col in x else None)

            result["word"] = get_column("word")
            result["upos_onehot"] = get_column("upos_onehot")
            for pos in UPOS:
                result[pos] = result["upos_onehot"].apply(lambda x: x[pos2idx[pos]])
            result = result[["word"] + UPOS]
            result = result.groupby("word").sum().reset_index(drop=True)
            
            vocab = set(tokenizer.get_vocab().keys())
            result = result[result["word"].isin(vocab)].reset_index(drop=True)

            output[name] = result
        return output

    def process(
            data_dir: str=data_dir,
            tokenizers: dict=tokenizers,
            masks: list[str]=masks,
            test: bool=test,
            batch_number: int=batch_number,
            batch_size: int=batch_size
    ):
        """Main function that processes the data."""
        last_tok = list(tokenizers.keys())[-1]
        files = get_files(
            data_dir,
            remainder=True,
            smallest=True,
            output_dir=os.path.join(intermediate_dir, last_tok),
            batch_number=batch_number,
            batch_size=batch_size
        )
        if test:
            files = files[:3]

        for file in tqdm(files, desc= "Assigning UPOS tags"):
            dataset = load_dataset(
                file_path=file,
                output_type="Dataset",
                columns="text",
                masks=masks
            )
            if test:
                dataset = dataset.select(range(100))

            df = generate_upos_onehots(dataset)
            result = tabulate_onehots(df)

            for name, df in result.items():
                tok_dir = os.path.join(intermediate_dir, name)
                os.makedirs(tok_dir, exist_ok=True)
                output_path = get_output_path(file, tok_dir)
                df.to_parquet(output_path)
    process()


def jpos_process(
        data_dir: str,
        tokenizers: object | list[object],
        intermediate_dir: str,
        tagger = fugashi.Tagger('-d "{}"'.format(unidic_lite.DICDIR)),
        masks = ["duplicate", "pattern"],
        test: bool = False,
        batch_number: int = None,
        batch_size: int = 10
):
    """Processes the data using fugashi to assign JPOS tags to each word in the dataset."""
    
    tokenizers = list(tokenizers)
    vocab = set(chain(*[tokenizer.get_vocab().keys() for tokenizer in tokenizers]))
    files = get_files(
        data_dir, 
        remainder=True, 
        output_dir=intermediate_dir,
        batch_number=batch_number,
        batch_size=batch_size)
    if test:
        files = files[:3]

    for file in tqdm(files, desc="Assigning JPOS tags"):
        df = load_dataset(
            file,
            columns="text",
            masks=masks
        )
        if test:
            df = df.head(100)

        df["tagged"] = df["text"].apply(lambda x: [(word.surface, word.pos.split(",")[0]) for word in tagger(x)])
        tagged = [tag for tag in list(chain(*df["tagged"].tolist())) if tag[0] in vocab]
        df = pd.DataFrame(nltk.ConditionalFreqDist(tagged)).T.fillna(0)
        df = df.reset_index().rename(columns={"index": "word"})

        os.makedirs(intermediate_dir, exist_ok=True)
        path_to_output = get_output_path(file, intermediate_dir)
        save_to_parquet(df, path_to_output)


def combine_tables(
        pos_type: str,
        intermediate_dir: str,
        path_to_output: str="") -> pd.DataFrame:
    
    """Combines all results. Compresses retults into a single table with realtive values for each POS tag.
    Also assigns the most likely POS tag for each word, adding the top 5 most likely POS tags as columns."""

    files = get_files(intermediate_dir)

    combined = pd.concat([pd.read_parquet(file) for file in files]).groupby("word").sum()
    combined = combined[combined.index.isin(vocab)]
    pos_columns = combined.columns
    combined = combined.div(combined.sum(axis=1), axis=0)
    

    def get_top_n_tags(x, n=5):
        try:
            # Get the nlargest n values' indices (POS tags)
            largest_values = x.nlargest(n)
            # Filter out any indices where the value is <= 0.1 to adhere to the original intent
            filtered_indices = largest_values[largest_values > 0.1].index.tolist()
            return filtered_indices
        except TypeError:
            # Handle or ignore columns where nlargest cannot be applied
            return []
    
    combined[pos_columns] = combined[pos_columns].applymap(lambda x: round(x, 2))
    combined = combined.reset_index()

    combined[f"{pos_type}"] = combined[pos_columns].apply(get_top_n_tags, axis=1)
    if path_to_output:
        os.makedirs(os.path.dirname(path_to_output), exist_ok=True)
        combined.to_csv(path_to_output, index=False)
    return combined