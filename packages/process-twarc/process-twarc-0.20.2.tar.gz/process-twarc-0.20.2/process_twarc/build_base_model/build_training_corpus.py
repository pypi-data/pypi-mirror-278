from process_twarc.util import (
    concat_dataset, 
    get_files, 
    save_to_parquet, 
    get_output_path, 
    load_dataset,
    make_dir
)
from nltk import FreqDist
from itertools import chain
import os
import pandas as pd
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
import unicodedata
from tqdm import tqdm
import fugashi
import unidic_lite
import re
from datasets import Dataset

"""
The HuggingFace tokenizer trainer is designed to work with space segmented text.
To use it with Japanese text, the text must be pre-tokenized.

This pipeline normalizes the text, removes tags, and pretokenizes the text using fugashi and unidic_lite.

In this process, character sets are also generated for each tweet. This will be used to determine
"""

def pretokenize_dataset(
        file: str,
        pre_tokenized_dir: str = "",
        tokenizer = fugashi.Tagger('-d "{}"'.format(unidic_lite.DICDIR))

        ) -> Dataset:
    """
    Prepares the text for building a corpus for training a tokenizer.
    
    Args:
        file (str): The file to process
        pre_tokenized_dir (str): The directory to save the pre-tokenized data
        tokenizer (fugashi.Tagger): The tokenizer to use
    
    Returns:
        Dataset: The pre-tokenized dataset with the following columns:
            "tweet_id": The tweet id
            "text": The original text
            "hashtags_masked": The text with hashtags masked
            "user_cap": Bool with True if the tweet is to be masked when Users are capped.
            "normalized": The normalized text
            "charset": The character set of the normalized text
            "cleaned_text": The normalized text with tags removed
            "pre_tokenized": The cleaned text, pre_tokenized by fugashi
    """
    
    # Normalizes by same method as the HuggingFace BertJapaneseTokenizer
    def normalize_fn(text):
       return unicodedata.normalize("NFKC", text)

    # Compresses the normalized text to a set of unique characters
    def charset_fn(normalized):
        return list(set(normalized))
    
    # Removes tags from the normalized text
    def clean_fn(normalized):
        return re.sub(r"\[(URL|USER|HASHTAG)\]", "", normalized)
    
    # Tokenizes the cleaned text using fugashi
    def tokenize_fn(cleaned_text):
        return " ".join([word.surface for word in tokenizer(cleaned_text)])
    
    
    make_dir(pre_tokenized_dir)
    dataset = load_dataset(
        file,
        output_type = "Dataset",
        columns = ["tweet_id", "text", "hashtags_masked", "user_cap"],
        masks = ["duplicate", "pattern"]
        )
    
    dataset = dataset.map(lambda x: {"normalized": normalize_fn(x["text"])}, desc="Normalizing. . .")
    dataset = dataset.map(lambda x: {"charset": charset_fn(x["normalized"])}, desc="Generating character sets. . .")
    dataset = dataset.map(lambda x: {"cleaned_text": clean_fn(x["normalized"])}, desc="Cleaning tags from text. . .")
    dataset = dataset.map(lambda x: {"pre_tokenized": tokenize_fn(x["cleaned_text"])}, desc="Pre-tokenizing text. . .")

    if pre_tokenized_dir:
        output_path = get_output_path(file, pre_tokenized_dir)
        save_to_parquet(dataset, output_path)
    return dataset

def pre_tokenize_pipeline(
    data_dir: str,
    pre_tokenized_dir: str,
    tokenizer = fugashi.Tagger('-d "{}"'.format(unidic_lite.DICDIR))
    ):
    """Given an input and an output directory, pre-tokenizes the datasets."""
    for file in tqdm(get_files(data_dir), desc="Pre-tokenizing datasets"):
        pretokenize_dataset(
            file, 
            pre_tokenized_dir,
            tokenizer=tokenizer)

def score_text_by_rank(
        pretokenized_dir: str,
        corpus_settings: dict,
        character_freqs_dir: str,
        training_corpus_dir: str,
        whitelist: set = set()
) -> None:
    
    """Scores tweets by the rank of their lowest frequency character. 

    The score informs which tweets will be used to train the tokenizer.
    
    Args:
        pretokenized_dir (str): The directory of the pre-tokenized data
        corpus_settings (dict[str, dict[str, bool]]): The settings for each corpus
            Dict format: {"corpus_name": {"mask_column": bool}}
            ex: {"full_corpus": {"user_cap": False}}

        character_freqs_dir (str): The directory of the character frequency data 
        training_corpus_dir (str): The directory to save the scored data
        whitelist (set[str]): A set of tokens to always include in the training data
    """
    def get_mask_columns(
        corpus_settings: dict,
        ) -> list[str]:
        """Helper funtion. Takes the corpus settings, and returns a list of all the mask columns"""

        return list({mask for value in corpus_settings.values() for mask in value})

    def tabulate_char_freqs(
            pre_tokenized_dir: str,
            character_freqs_dir: str,
            corpus_settings: dict,
        ) -> None:
        """From the pre_tokenized_dir, tabulates the frequency of each character in the charset column."""

        mask_columns = get_mask_columns(corpus_settings)
        df = concat_dataset(
            get_files(pre_tokenized_dir),
            columns = ["charset"] + mask_columns
        )
        def tabulate_fn(df):
            fdist = FreqDist(chain.from_iterable(df.charset.tolist()))
            fdist = pd.DataFrame(fdist.items(), columns=["char","freq"]).sort_values("freq",ascending=False).reset_index(drop=True)
            fdist["rank"] = fdist.index + 1
            return fdist
        results = {}
        for name, settings in corpus_settings.items():
            new_df = df.copy()
            for column, value in settings.items():
                if value:
                    new_df = new_df[new_df[column] == False]
            results[name] = tabulate_fn(new_df)

        for name, result in results.items():
            result.to_csv(f"{character_freqs_dir}/{name}.csv", index=False)
        return results

    def load_char2rank(
            corpus_settings=corpus_settings, 
            character_freqs_dir=character_freqs_dir,
            whitelist=whitelist
            ) -> dict:
        """Loads the character frequency data and returns a dictionary of character to rank mappings."""

        char2rank = {}
        for corpus in corpus_settings.keys():
            df = pd.read_csv(os.path.join(character_freqs_dir, corpus + ".csv"))
            char2rank[corpus] = {k:v for k,v in zip(df["char"], df["rank"])}
            if whitelist:
                for token in whitelist:
                    char2rank[corpus][token] = 1
        return char2rank
    
    def score_fn(text, char2rank):
        """Scores the text by the rank of its lowest frequency character."""

        return max([char2rank.get(c, np.inf) for c in text])
    
    #Check if the character frequency data exists. If not, create it.
    if not all(os.path.exists(os.path.join(character_freqs_dir, corpus + ".csv")) for corpus in corpus_settings.keys()):
        tabulate_char_freqs(pretokenized_dir, character_freqs_dir, corpus_settings)

    
    char2rank = load_char2rank()
    mask_columns = get_mask_columns(corpus_settings)

    for file in tqdm(get_files(pretokenized_dir)):
        df = load_dataset(file)
        for corpus, settings in corpus_settings.items():
            new_df = df.copy()
            if mask_columns:
                for column, value in settings.items():
                    if value:
                        new_df = new_df[new_df[column] == False]

            new_df["score"] = new_df.charset.apply(lambda x: score_fn(x, char2rank[corpus])) 
            output_dir = os.path.join(training_corpus_dir, corpus)
            save_to_parquet(new_df, get_output_path(file, output_dir))
    
def generate_histogram_with_rank_cutoff(
        training_corpus_dir: str,
        target_percentile_cutoff=99,
        show_plot: bool = True,
        title: str = "Rank Frequency with Cutoff",
        path_to_output: str = "",
        ) -> int:
    """Generates a histogram of the character rank scores and returns the cutoff rank for the target percentile.
    
    Args:
        training_corpus_dir (str): The directory of the scored data
        target_percentile_cutoff (int): The target percentile cutoff for the rank
        show_plot (bool): If True, shows the plot
        save_plot (bool): If True, saves the plot
        corpus_name (str): The name of the corpus
        path_to_output (str): The path to save the plot
    """
    def extract_score_array(char_freqs_dir:str):
        dataset = concat_dataset(
            get_files(char_freqs_dir),
            columns=["score"]
        )
        return np.array(dataset["score"])

    score_arr = extract_score_array(training_corpus_dir)
    histogram, bins = np.histogram(score_arr, bins=np.arange(min(score_arr), max(score_arr)+2))
    
    # Compute the cumulative histogram
    cumulative_histogram = np.cumsum(histogram)
    final_cumulative_count = cumulative_histogram[-1]
    
    # Compute the relative cumulative histogram
    relative_cumulative_histogram = cumulative_histogram / final_cumulative_count * 100
    
    # Find the relative cutoff value where cumulative count is equal to 90% of the final cumulative count
    target_percentile_cutoff = target_percentile_cutoff
    cutoff_rank = None
    for i, value in enumerate(relative_cumulative_histogram):
        if value >= target_percentile_cutoff:
            cutoff_rank = bins[i]
            break
    
    # Plot the relative cumulative histogram
    plt.bar(bins[:-1], relative_cumulative_histogram)
    plt.xlabel('Rank')
    plt.ylabel('Cumulative Percentile (%)')
    plt.title(title)
    
    # Highlight the target value
    if cutoff_rank is not None:
        plt.axvline(x=cutoff_rank, color='r', linestyle='--', label=f'Cutoff Rank: {cutoff_rank}')
        plt.legend()
    
    if path_to_output:
        plt.savefig(path_to_output)
    if show_plot:
        plt.show()
    return cutoff_rank


def generate_low_freq_char_mask(
    training_corpus_dir: str,
    restart: bool = True
):
    """Generates a mask for the low frequency characters in the training data.
    
    Args:
        training_corpus_dir (str): The directory of the scored data
        restart (bool): If True, restarts the process
    """
    corpus_names = os.listdir(training_corpus_dir)

    for name in corpus_names:
        data_dir = os.path.join(training_corpus_dir, name)
        cutoff_rank = generate_histogram_with_rank_cutoff()

        for file in tqdm(get_files(data_dir)):
            dataset = load_dataset(file, output_type = "Dataset")
            if not restart and "low_freq_char" in dataset.column_names:
                continue
            dataset = dataset.map(lambda example: {"low_freq_char": example["score"] > cutoff_rank})
            save_to_parquet(dataset, file)

def build_training_corpus_pipeline(
        data_dir: str,
        corpus_settings: dict,
        whitelist: set = set(),
        pre_tokenized_dir: str="pre_tokenized",
        tokenizer: object=fugashi.Tagger('-d "{}"'.format(unidic_lite.DICDIR)),
        character_freqs_dir: str = "character_freqs",
        training_corpus_dir: str = "training_corpus",
        restart: bool = True
):
    pre_tokenize_pipeline(
        data_dir,
        pre_tokenized_dir,
        tokenizer=tokenizer
    )
    score_text_by_rank(
        pre_tokenized_dir,
        corpus_settings,
        character_freqs_dir,
        training_corpus_dir,
        whitelist=whitelist
    )
    generate_low_freq_char_mask(
        training_corpus_dir,
        restart=restart
    )