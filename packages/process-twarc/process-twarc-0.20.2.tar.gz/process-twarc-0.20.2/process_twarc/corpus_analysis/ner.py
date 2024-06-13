from process_twarc.util import load_dataset, get_output_path
from unicodeblock.blocks import of as block
import pandas as pd
import json
from transformers import pipeline
from collections import Counter
import itertools
import os

def get_blocks(token):
    token = token.replace("##", "")

    return ", ".join(list(set([block(char) if block(char) else "none" for char in token])))

def get_new_vocab(tokenizers):
    vocab = lambda tok: set(tok.vocab.keys())
    old_tok = tokenizers["old_tok"]

    result = {}
    for name, tokenizer in tokenizers.items():
        if name == "old_tok":
            continue
        new_tok = tokenizer
        new_vocab = vocab(new_tok) - vocab(old_tok)

        df = pd.DataFrame({"token": list(new_vocab)})
        df["blocks"] = df["token"].apply(get_blocks)

        whitelist = [
            "HIRAGANA",
            "KATAKANA",
            "CJK",
            "LATIN",
            "NUM",
            "DIGIT"
        ]
        #filter for rows where any member of the whitelist is present in blocks
        df = df[df["blocks"].str.contains("|".join(whitelist))]
        df["tok_encoding"] = df["token"].apply(lambda x: new_tok.vocab[x])
        result[name] = df
    return result

def find_target_tokens(target_tokens, ner_tokens):

    ner_tokens = list(enumerate(ner_tokens))
    target_tokens = list(target_tokens)
    result = {}

    for target in target_tokens:
    
    
        start = target[0]
        end = target[-1]
        starts = [(idx, token) for (idx, token) in ner_tokens if token.startswith(start)]
        ends = [(idx, token) for (idx, token) in ner_tokens if token.endswith(end)]

        spans = []
        for (idx1, _) in starts:
            for (idx2, _) in ends:
                if idx2 > idx1:
                    spans.append((idx1, idx2))

        #join tokens with ## stripped, if any
        get_word = lambda span: "".join([tok.replace("##", "") for (_, tok) in ner_tokens[span[0]:span[1]+1]])
        get_subwords = lambda span: {idx: {"token": ner_tokens[idx][1]} for idx in range(span[0], span[1]+1)}
        
        entries = {str(span): 
                  {
                      "word": get_word(span), 
                      "subwords": get_subwords(span)
                      } for span in spans if get_word(span) == target}
        result.update(entries)
                 
                
    return result

def get_ner_columns(dataset, tokenizers, model):
    tokenizer = tokenizers["old_tok"]

    dataset["ner_tokens"] = dataset["text"].apply(lambda x: tokenizer.tokenize(x))
    ner = pipeline("ner", model=model, tokenizer=tokenizer, device="cuda")
    dataset["ner_scores"] = dataset["text"].apply(lambda x: ner(x))
    return dataset

def get_target_ids(dataset, tokenizers, model):
    new_vocab = get_new_vocab(tokenizers)
    dataset = get_ner_columns(dataset, tokenizers, model)
    for name, vocab in new_vocab.items():
        tokenizer = tokenizers[name]
        dataset[f"{name}_input_ids"] = dataset["text"].apply(lambda x: tokenizer(x)["input_ids"])
        target = vocab["tok_encoding"].values
        dataset[f"{name}_target_ids"] = dataset[f"{name}_input_ids"].apply(lambda x: [i for i in x if i in target]) 
        dataset[f"{name}_target_tokens"] = dataset[f"{name}_target_ids"].apply(lambda x: [tokenizer.decode([i]) for i in x])

        targets = lambda row: find_target_tokens(row[f"{name}_target_tokens"], row["ner_tokens"])
        dataset[f"{name}_targets"] = dataset.apply(lambda x: json.dumps(targets(x), ensure_ascii=False), axis=1)
    return dataset

def compile_NER_results(dataset: pd.DataFrame, tokenizers: dict, model: object):
    dataset = get_target_ids(dataset, tokenizers, model)


    def dumps(idx, name, x):
        dataset.at[idx, f"{name}_result"] = json.dumps(x, ensure_ascii=False)
    
    for idx1, row in dataset.iterrows():
        for name, _ in tokenizers.items():
            score = {
                    (s["index"]):{
                        "word": s["word"],
                        "score": float(s["score"]),
                        "entity": s["entity"]
                    } for s in row["ner_scores"]
                } if row["ner_scores"] else {}
            
            if name == "old_tok":
                tokens = list(enumerate(row["ner_tokens"]))
                result = {
                    tup[0]: {
                        "word": tup[1],
                        "score": score.get(tup[0]+1, {"score": 0})["score"],
                        "entities": [score.get(tup[0]+1, {"entity": None})["entity"]],
                        "group": "old_vocab"
                        } for tup in tokens
                }

                dumps(idx1, name, result)
                
            else:
                non_entity_tokens = list(enumerate(row["ner_tokens"]))
                targets = json.loads(row[f"{name}_targets"])

                result = {} 
                for span in targets.keys():
                    word = targets[span]
                    subwords = word["subwords"]
                
                    for idx2 in subwords:
                        non_entity_tokens = [t for t in non_entity_tokens if t[0] != int(idx2)]
                        subword = subwords[idx2]
                        subword_score = score.pop(int(idx2)+1, {"score": 0, "entity": None}) if score else {"score": 0, "entity": None}
                        subword["score"], subword["entity"] = subword_score["score"], subword_score["entity"]    

                    average_score = sum([subword["score"] for subword in subwords.values()]) / len(subwords)
                    entities = list(set([subword["entity"] for subword in subwords.values()]))

                    word["score"] = average_score
                    word["entities"] = entities
                    word["group"] = "new_vocab"
                    result[span] = word
                
                if score:
                    for idx3 in score.keys():
                        non_entity_tokens = [t for t in non_entity_tokens if (t[0]+1) != int(idx3)]

                        old_word = {idx3: {
                            "word": score[idx3]["word"],
                            "score": score[idx3]["score"],
                            "entities": [score[idx3]["entity"]],
                            "group": "old_vocab"
                        }
                        }
                        result.update(old_word)
                
                result["non_entity_tokens"] = [t[1] for t in non_entity_tokens]
                dumps(idx1, name, result)
    return dataset

def tabulate_results(dataset, tokenizers):
    flatten = lambda list_of_lists: list(itertools.chain.from_iterable(list_of_lists))
    output = {}
    for name, _ in tokenizers.items():
        result = [json.loads(x) for x in dataset[f"{name}_result"]]
        if name != "old_tok":
            non_entity_tokens = Counter(flatten([x.pop("non_entity_tokens") for x in result]))
        else:
            non_entity_tokens = None
        dataset[f"{name}_result"] = result
        result = dataset[f"{name}_result"].apply(pd.Series).stack().to_frame().reset_index()

        get_column = lambda col: result[0].apply(lambda x: x[col])

        result["word"] = get_column("word")
        result["score"] = get_column("score")
        result["entities"] = get_column("entities")
        result["group"] = get_column("group")
    
        result = result.drop(columns=[0, "level_1"]).rename(columns={"level_0": "tweet_id"})
        result = result.groupby(["word", "group"]).agg({"score": "mean", "entities": "sum", "tweet_id": "count"}).reset_index()
        result["entities"] = result["entities"].apply(lambda x: list(set(x)))
        result.rename(columns={"tweet_id": "count"}, inplace=True)

        result = result.set_index("word")
        
        if non_entity_tokens:
            for (token, count) in non_entity_tokens.items():
                if token in result.index:
                    old_count = result.loc[token, "count"]
                    old_score = result.loc[token, "score"]
                    new_count = old_count + count
                    new_score = old_score * (old_count / new_count)
                    result.at[token, "count"] = new_count
                    result.at[token, "score"] = new_score
                else:
                    result.loc[token] = ["old_vocab", 0, [None], count]
        
        output[name] = result.reset_index()
    return output

def process(path_to_dataset, tokenizers, model, output_dir):
    dataset = load_dataset(
        path_to_dataset,
        columns = ["tweet_id", "text"],
        masks = ["duplicate", "pattern", "user_cap"])
    dataset = compile_NER_results(dataset, tokenizers, model)
    output = tabulate_results(dataset, tokenizers)

    intermediate_dir = f"{output_dir}/intermediate"
    ner_count_dirs = {name: f"{output_dir}/ner_counts_{name}" for name in tokenizers.keys()}
    for dir in list(ner_count_dirs.values()) + [intermediate_dir]:
        os.makedirs(dir, exist_ok=True)
    
    dataset.to_parquet(get_output_path(path_to_dataset, intermediate_dir))
    for name, df in output.items():
        df.to_parquet(get_output_path(path_to_dataset, ner_count_dirs[name]))

    return dataset, output