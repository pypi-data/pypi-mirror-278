import pandas as pd
from datasets import Dataset, concatenate_datasets
import pyarrow as pa
import pyarrow.parquet as pq
from tqdm import tqdm
from ntpath import basename
import os
import json
from typing import Union
import torch
import webbrowser
import sys
from io import StringIO
import contextlib

def reverse_mapping(original_dict):
    reversed_dict = {}
    for key, value_list in original_dict.items():
        for value in value_list:
            # Directly assign the original key to the reversed dictionary
            # This will overwrite any previous key associated with the value
            reversed_dict[value] = key
    return reversed_dict

@contextlib.contextmanager
def capture_output():
    new_stdout, new_stderr = StringIO(), StringIO()
    old_stdout, old_stderr = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_stdout, new_stderr
        yield sys.stdout
    finally:
        sys.stdout, sys.stderr = old_stdout, old_stderr

def format_and_execute(code, path_to_output=""):
    if not path_to_output:
        path_to_output = 'formatted_code_output.txt'
    os.makedirs(os.path.dirname(path_to_output), exist_ok=True)
    with open(path_to_output, 'w', encoding='utf-8') as file, capture_output() as output:
        # Write the code to the file with >>>
        for line in code.split('\n'):
            file.write(f'>>> {line}\n')
        
        # Execute the code and capture output
        exec(code, globals(), locals())
        
        # Write captured output to the file
        file.write('\n' + output.getvalue())
    
    print(f'Code and output have been written to {path_to_output}')

def custom_serialize(obj, indent=4, level=0):
    spaces = ' ' * indent * level
    if isinstance(obj, dict):
        items = []
        for key, value in obj.items():
            formatted_value = custom_serialize(value, indent, level+1)
            items.append(f'\n{spaces}{indent*" "}"{key}": {formatted_value}')
        return f'{{{",".join(items)}\n{spaces}}}'
    elif isinstance(obj, list) and all(isinstance(x, str) for x in obj):
        # Serialize the list on a single line if it contains only strings
        return '[' + ', '.join(json.dumps(item) for item in obj) + ']'
    elif isinstance(obj, list):
        items = [custom_serialize(item, indent, level+1) for item in obj]
        return f'[\n{spaces}{indent*" "}' + f',\n{spaces}{indent*" "}'.join(items) + f'\n{spaces}]'
    else:
        # Use json.dumps to handle other data types (strings, numbers, etc.)
        return json.dumps(obj)

def make_dir(directory):
    """
    Create a new directory if it does not exist.

    Args:
        directory (str): The directory to be created.
    """
    if directory == "": return
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_file_type(file_path):
    """
    Get the file type from the file path.

    Args:
        file_path (str): The file path.

    Returns:
        str: The file type.
    """
    return file_path.split(".")[-1]

def get_files(
        directory, 
        remainder: bool=False, 
        output_dir: str=None, 
        smallest: bool=False, 
        batch_number: int=None, 
        batch_size: int=10):
    """
    Get a list of all files from all directories within the specified directory.

    Args:
        directory (str): The directory containing multiple directories.

    Returns:
        list: A list of file paths from all directories within the specified directory.
    """
    def _get(directory):
        file_list = []
        for root, _, files in os.walk(directory):
            for file in files:
                file_list.append(os.path.join(root, file))
        return file_list
    
    files = _get(directory)
    if remainder:
        if not output_dir:
            raise ValueError("Please provide an output directory.")
        finished = _get(output_dir)
        base = lambda file_path: basename(file_path).split(".")[0]
        files = [f for f in files if base(f) not in [base(f2) for f2 in finished]]
    if smallest:
        sized_files = [(file_path, os.path.getsize(file_path)) for file_path in files]
        sized_files.sort(key=lambda x: x[1])
        files = [file[0] for file in sized_files]
    
    if batch_number:
        batch_number -= 1
        start = batch_number * batch_size
        end = start + batch_size
        files = files[start:end]
    return files

def load_parquet(file_path: str, output_type: str = "pd", columns=None):
    """
    Load a data structure of the selected type from a parquet file.

    Args:
        file_path (str): Path to the parquet file.
        output_type (str, defaults to "pd"): Type of the output data structure. Either "pd" for pandas DataFrame or "Dataset" for custom Dataset.
        columns (str or list, optional): Columns to load. If provided, only load the specified columns.

    Returns:
        object: Loaded data structure.
    """
    if isinstance(columns, str):
        columns = list(columns)

    if output_type == "pd":
        if columns:
            dataset = pd.read_parquet(file_path, columns=columns)
        else:
            dataset = pd.read_parquet(file_path)
    elif output_type == "Dataset":
        if columns:
            table = pq.read_table(file_path, columns=columns)
        else:
            table = pq.read_table(file_path)
        dataset = Dataset(table)
    else:
        raise ValueError("Please input a valid output type. Either 'pd' or 'Dataset'.")

    return dataset

def merge_lists(*args):
    """Helper function for load_dataset"""
    merged_list = [element for arg in args for element in arg]
    return list(set(merged_list))

def load_dataset(file_path: str, output_type: str = "pd", columns=None, masks=None, inverse_mask=False, drop_mask_columns=True):
    """
    Load a data structure of the selected type from a parquet file and apply optional masking.

    Args:
        file_path (str): Path to the parquet file.
        output_type (str, defaults to "pd"): Type of the output data structure. Either "pd" for pandas DataFrame or "Dataset" for custom Dataset.
        columns (str or list, optional): Columns to load. If provided, only load the specified columns.
        masks (str or list, optional): Mask column(s) to apply and remove rows where the mask is True.

    Returns:
        object: Loaded data structure.
    """
    if columns and isinstance(columns, str):
        columns = [columns]
    
    if masks:
        if isinstance(masks, str):
            masks = [masks]
        if masks and columns:
            columns = list(set(columns+masks))
        
        load_type = "pd"
        dataset = load_parquet(file_path, load_type, columns)
        mask = dataset[masks].any(axis=1) if not inverse_mask else ~dataset[masks].any(axis=1)
        dataset = dataset[~mask].reset_index(drop=True)

        if drop_mask_columns:
            dataset = dataset.drop(columns=masks)

        if output_type == "Dataset":
            dataset = Dataset(pa.Table.from_pandas(dataset))
        return dataset

    else:
        dataset = load_parquet(file_path, output_type, columns)
        return dataset


def concat_dataset(file_paths, output_type="pd", columns=None, masks=None, inverse_mask=False, drop_mask_columns=True):
    """
    Concatenate multiple datasets from parquet files and apply optional masking.

    Args:
        file_paths (list[str]): Paths to the parquet files.
        output_type (str, defaults to "pd"): Type of the output data structure. Either "pd" for pandas DataFrame or "Dataset" for custom Dataset.
        columns (str or list[str], optional): Columns to load. If provided, only load the specified columns.
        masks (str or list[str], optional): Mask column(s) to apply and remove rows where the mask is True.

    Returns:
        object: Concatenated and optionally masked data structure.
    """
    datasets = []
    
    for file_path in tqdm(file_paths, desc = "Loading dataset"):
        dataset = load_dataset(
            file_path=file_path, 
            output_type=output_type,
            columns=columns, 
            masks=masks, 
            inverse_mask=inverse_mask, 
            drop_mask_columns=drop_mask_columns)
        datasets.append(dataset)
    
    concatenated = pd.concat(datasets) if output_type == "pd" else concatenate_datasets(datasets)
    
    return concatenated

def get_output_path(file_path:str, output_dir:str, file_type:str=""):
    """
    Generate a new file path for transforming data from one filetype to another.

    Given the original file path and the destination folder, generate a new file path
    with the destination folder and the specified file type.

    Args:
        file_path (str): The original file path.
        output_dir (str): The destination folder where the transformed file will be saved.
        file_type (str, Optional): The desired file type for the transformed file.

    Returns:
        str: The new file path with the destination folder and file type.
    """
    if file_type:
        file = basename(file_path).split(".")[0]
        ouput_path = f"{output_dir}/{file}.{file_type}"
    else:
        file = basename(file_path)
        ouput_path = f"{output_dir}/{file}"
    return ouput_path

def save_to_parquet(data, file_path):
    make_dir(os.path.dirname(file_path))
    if isinstance(data, pd.DataFrame):
        data.to_parquet(file_path)
    elif isinstance(data, Dataset):
        data_frame = pd.DataFrame(data)
        data_frame.to_parquet(file_path)
    else:
        raise ValueError("Data must be either a pd.DataFrame or a HuggingFace Dataset.")
    
def save_dict(dict:dict, save_path: str):
    """
    Save a dictionary to the JSON file format.

    Args:
        dict (dict): Dictionary to be saved.
        save_path (str): Path where the JSON file will be saved.
    """
    with open(save_path, 'w', encoding="utf-8") as f:
        json.dump(dict, f, ensure_ascii=False, indent=2)
        return


def load_dict(path_to_dict: str):
    """Loads a dictionary from a JSON file."""
    with open(path_to_dict, "r", encoding="utf-8") as f:
        return json.load(f)

def find_examples(
        token_sets_dir: str,
        tokens: Union[str, list[str]], 
) -> dict[str, pd.DataFrame]:
    """Provided a directory to a set of tokenized datasets, find examples of tweets containing the specified tokens."""
    dataset = concat_dataset(
        get_files(token_sets_dir),
        columns = ["tweet_id", "tokens"]
    )

    if isinstance(tokens, str):
        tokens = [tokens]
    return {token: dataset[dataset["tokens"].apply(lambda x: token in x)] for token in tokens}

def display_examples(
        examples: dict[str, pd.DataFrame],
        n = 10
):
    """Display a random sample of n tweets from each token set."""
    sample = examples.sample(n)
    for tweet in sample["tweet_id"].tolist():
        webbrowser.open(f"https://twitter.com/anyuser/status/{tweet}")

def get_embedding(
        token: str,
        tokenizer,
        model,
        method: str):
    if method not in ["token", "first_token", "CLS"]:
        raise ValueError("Invalid method. Method must be either 'token' or 'CLS'.")

    if method == "token":
        if len(tokenizer.tokenize(token)) != 1:
            raise ValueError("Tokenized length should be equal to 1 for token method.")
        token_id = tokenizer.convert_tokens_to_ids(token)  # Extracting the token ID
        token_tensor = torch.tensor([token_id])  # Convert token ID to tensor
        embedding = model.embeddings.word_embeddings(token_tensor).detach().numpy()
        embedding = embedding.squeeze()  # Accessing the embedding layer directly
    elif method == "CLS":
        input_ids = tokenizer.encode(token, return_tensors="pt")
        with torch.no_grad():
            output = model(input_ids)
        embedding = output.last_hidden_state.mean(dim=1).squeeze().numpy()

    return embedding

    
    

