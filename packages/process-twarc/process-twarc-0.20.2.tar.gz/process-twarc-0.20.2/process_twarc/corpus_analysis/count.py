import itertools
from process_twarc.util import get_output_path, load_dataset, get_files, save_to_parquet
import pandas as pd
import re
from nltk import FreqDist
from tqdm import tqdm
import os
from itertools import chain
from nltk import ngrams

def count_characters(
        file_path: str, 
        output_dir: str=""
        ):
    """
    For decision-making purposes.

    The tokenizer cannot include all characters present in the dataset.

    This function counts the number of Tweets in which each character appears at least once.

    Args:
        file_path (str): Path to a dataset.
        output_dir (str, optional): Path to a directory where the output will be saved.

    Returns:
        character_counts (dict): A dictionary of characters and their counts.
    """
    dataset = load_dataset(
        file_path, 
        output_type="Dataset", 
        columns="text")
    def charset_fn(text):
        return list(set(text))
    
    dataset = dataset.map(lambda example: {"charset": charset_fn(example["text"])})
    characters = itertools.chain.from_iterable(dataset["charset"])
    result = FreqDist(characters)
    result = pd.DataFrame(result.items(), columns=["character", "count"])
    result = result.sort_values(by="count", ascending=False)
    if output_dir:
        path_to_output = get_output_path(file_path, output_dir, file_type="csv")
        result.to_csv(path_to_output, index=False)
    return result

def character_count_pipeline(
        data_dir: str,
        intermediate_dir: str= "character_counts/files/",
        output_dir: str="character_counts/combined",
        batch_number: int=None,
        batch_size: int=10,
        combine_counts: bool=False
        
):
    """Pipeline that will count characters by file, and then combine files."""

    files = get_files(
        data_dir,
        remainder=True,
        output_dir=intermediate_dir,
        batch_number=batch_number,
        batch_size=batch_size)
    for file in tqdm(files, desc="Counting characters"):
        count_characters(file, intermediate_dir)

    print("All characters counted.")
    if combine_counts:
        print("Combining counts.")
        os.makedirs(output_dir, exist_ok=True)
        results = pd.concat([pd.read_csv(file) for file in get_files(intermediate_dir)])
        results = results.groupby("character").sum().reset_index()
        results = results.sort_values(by="count", ascending=False)
        results.to_csv(os.path.join(output_dir, "character_counts.csv"), index=False)
        return results

def extract_tags(
        file_path: str,
        tag_type: str,
        masks: list = None,
        output_dir: str=""
        ):
    """
    For corpus analysis.

    This functions extracts a tag of choice and writes the results to a file.

    Args:
        file_path (str): Path to a dataset.
        output_dir (str, optional): Path to a directory where the output will be saved.

    Returns:
        hashtags (pd): A dataframe of tags and their counts.
    """
    if tag_type not in ["hashtags", "mentions"]:
        raise ValueError("tag_type must be either 'hashtags' or 'mentions'.")
    if tag_type == "hashtags":
        pattern = r"#\w+"
    elif tag_type == "mentions":
        pattern = r"@\w+"
    
    dataset = load_dataset(file_path, columns="raw_text", masks=masks)
    tags = list(itertools.chain.from_iterable([re.findall(pattern, text) for text in dataset["raw_text"]]))
    result = pd.DataFrame(FreqDist(tags).items(), columns=["tag", "count"])
    result = result.sort_values(by="count", ascending=False)
    if output_dir:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        path_to_output = get_output_path(file_path, output_dir, file_type="csv")
        result.to_csv(path_to_output, index=False)

def tag_extraction_pipeline(
        tag_type: str,
        data_dir: str,
        intermediate_dir: str,
        masks: list = None,
        output_dir: str="tag_counts",
        batch_number: int=None,
        batch_size: int=10,
        combine_counts: bool=False
        ):
    
    """Pipe that will count the selected tag by file, then combine all files."""

    if tag_type not in ["hashtags", "mentions"]:
        raise ValueError("tag_type must be either 'hashtags' or 'mentions'.")
    
    files = get_files(
        data_dir,
        remainder=True,
        output_dir=intermediate_dir,
        batch_number=batch_number,
        batch_size=batch_size)
    
    for file in tqdm(files, desc= f"Extracting {tag_type}"):
        extract_tags(file, tag_type, masks=masks, output_dir=intermediate_dir)

    print(f"All {tag_type}s counted.")
    
    if combine_counts:
        os.makedirs(output_dir, exist_ok=True)
        results = pd.concat([pd.read_csv(file) for file in get_files(intermediate_dir)])
        results = results.groupby("tag").sum().reset_index()
        results = results.sort_values(by="count", ascending=False)
        results.to_csv(os.path.join(output_dir, f"{tag_type}.csv"), index=False)
        return results

def tokenize_for_counting(
        file_path: str,
        tokenizers: dict,
        keep_all_columns: bool=False,
        tokenized_dir: str="tokenized",
        text_column: str="text",
        masks: list = ["duplicate", "pattern"],
        combine_tokens: bool=False
        ):
    """Tokenize function that will generate tokenized lists for all experimental tokenizers.
    Also generates a column with a set of all tokens, which is useful for looking for examples of 
    tokens in the corpus."""

    if text_column not in ["text", "hashtags_masked"]:
        raise ValueError("text_column must be either 'text' or 'hashtags_masked'.")
    dataset = load_dataset(
        file_path,
        output_type="Dataset",
        columns=["tweet_id", text_column, "user_cap"] if not keep_all_columns else None,
        masks=masks
    )
    dataset = dataset.rename_columns({text_column: "text"})
    # Define tokenize functions outside of the loop to avoid redefining them on each iteration.
    def bert_tokenize_fn(name, tokenizer, example):
        return {f"{name}_tokens": tokenizer.tokenize(example["text"])}

    def mecab_tokenize_fn(name, tokenizer, example):
        return {f"{name}_tokens": [word.surface for word in tokenizer(example["text"])]}

    for name, tok_data in tokenizers.items():
        tok_type = tok_data["type"]
        tokenizer = tok_data["tokenizer"]

        # Use a closure to "capture" the current name and tokenizer.
        if tok_type == "bert":
            tokenize_fn = lambda example, name=name, tokenizer=tokenizer: bert_tokenize_fn(name, tokenizer, example)
        else:
            tokenize_fn = lambda example, name=name, tokenizer=tokenizer: mecab_tokenize_fn(name, tokenizer, example)

        dataset = dataset.map(tokenize_fn)

    def combine_fn(row):
        columns = [f"{name}_tokens" for (name, tok_data) in tokenizers.items() if tok_data["type"] == "bert"]
        tokens = list(set(chain(*[row[col] for col in columns])))
        return {"all_tokens": tokens}
    
    if combine_tokens:
        dataset = dataset.map(combine_fn)
    os.makedirs(tokenized_dir, exist_ok=True)
    path_to_output = get_output_path(file_path, tokenized_dir)
    save_to_parquet(dataset, path_to_output)

def  tokenize_pipeline(
        data_dir: str,
        tokenizers: dict,
        keep_all_columns: bool=False,
        tokenized_dir: str="tokenized",
        text_column: str="text",
        combine_tokens: bool=False,
        masks: list = ["duplicate", "pattern"],
        batch_number: int=None,
        batch_size: int=10
):
    """Pipeline that will tokenize and save tokenized lists for all experimental tokenizers."""
    files = get_files(
        data_dir, 
        remainder=True, 
        output_dir=tokenized_dir,
        batch_number=batch_number,
        batch_size=batch_size
        )
    for file in tqdm(files, desc="Tokenizing"):
        tokenize_for_counting(
            file, 
            tokenizers,
            keep_all_columns=keep_all_columns, 
            tokenized_dir=tokenized_dir,
            text_column=text_column,
            masks=masks,
            combine_tokens=combine_tokens)

def token_count_pipeline(
        tokenized_dir: str,
        tokenizers: dict,
        tokenized_counts_dir: str="token_counts/files",
        combine_counts: bool=False,
        output_dir: str="token_counts/combined",
        batch_number: int=None,
        batch_size: int=10,
        max_ngrams: int=0
):
    """Pipeline that will count tokenized lists by file and then combine tokens for each experimental tokenizer."""
    last_tok = list(tokenizers.keys())[-1]
    files = get_files(
        tokenized_dir, 
        remainder=True, 
        output_dir=os.path.join(tokenized_counts_dir, last_tok),
        batch_number=batch_number,
        batch_size=batch_size)

    for file in tqdm(files, desc="Counting tokens."):
        dataset = load_dataset(file)

        for name, tok_data in tokenizers.items():
            if tok_data["user_cap"]:
                dataset = dataset[dataset["user_cap"]==False]

            tokens = list(chain(*dataset[f"{name}_tokens"].tolist()))
            freqs = FreqDist(tokens)
            result = pd.DataFrame(freqs.items(), columns=["token", "count"])
            result_dir = os.path.join(tokenized_counts_dir, name)
            if max_ngrams:
                result_dir = os.path.join(result_dir, "1_grams")
            path_to_output = get_output_path(file, result_dir)
            save_to_parquet(result, path_to_output)

            if max_ngrams:
                for n in range(2, max_ngrams + 1):
                    ngram_freqs = FreqDist(ngrams(tokens, n))
                    ngram_result = pd.DataFrame(ngram_freqs.items(), columns=["token", "count"])
                    result_dir = os.path.join(tokenized_counts_dir, name, f"{n}_grams")
                    path_to_output = get_output_path(file, result_dir)
                    save_to_parquet(ngram_result, path_to_output)
    
    print("All tokens counted. Combining counts")

    if combine_counts:
        for name in tokenizers.keys():
            os.makedirs(output_dir, exist_ok=True)
            files = get_files(os.path.join(tokenized_counts_dir, name))
            result = pd.concat([load_dataset(file) for file in files]).groupby("token").sum().reset_index()
            path_to_output = os.path.join(output_dir, f"{name}_token_counts.csv")
            result.to_csv(path_to_output)
        

def find_kaomoji(
        example: list, 
        tokenizer_dict: dict,
        vocab_table: pd.DataFrame):
    vocab = vocab[["token", "char_family"]]
    target = vocab[vocab["char_family"].isin(["SYMBOL", "PUNCTUATION", "SCRIPT"])]["token"].tolist()


    start_idx = None
    count = 0
    chains = []

    name, bert_tokenizer = tokenizer_dict
    tokenized = list(enumerate([True if token in target else False for token in example[name]]))
    chains = []
    for idx, is_true in tokenized:
        if is_true==True:
            count += 1
            if start_idx is None:
                start_idx = idx
            if count >= 5 and idx == len(tokenized) - 1:
                chains.append((start_idx, idx))
        else:
            if count >= 5:
                chains.append((start_idx, idx - 1))
            start_idx = None
            count = 0
     
    encoded = [bert_tokenizer.encode(example[name][start:end+1])[1:-1] for start, end in chains]
    kaomoji = [bert_tokenizer.decode(encoded).replace(" ", "") for encoded in encoded]
    return {f"{name}_kaomoji": kaomoji}