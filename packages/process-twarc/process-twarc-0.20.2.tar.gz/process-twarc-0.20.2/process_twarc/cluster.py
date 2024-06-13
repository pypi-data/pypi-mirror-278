from process_twarc.util import save_to_parquet
from transformers import AutoTokenizer, AutoModel
import torch
import pickle
from datasets import Dataset


def generate_tweet_embeddings(
    dataset: Dataset,
    path_to_model: str,
    path_to_output: str=""
):

    tokenizer = AutoTokenizer.from_pretrained(path_to_model)
    model = AutoModel.from_pretrained(path_to_model)
    dataset = dataset.map(
        lambda x: tokenizer(x["text"], truncation=True, padding="max_length"),
        batched=True,
        batch_size=1000
    )
    print("toeknization done")

    dataset = dataset.to_pandas()

    dataset["tokens"] = dataset["input_ids"].apply(lambda x: tokenizer.convert_ids_to_tokens(x))

    def get_cls_embedding(example):
        with torch.no_grad():
            inputs = tokenizer.encode_plus(example["tokens"], add_special_tokens=True, return_tensors='pt')
            output = model(**inputs)
            cls_embedding = output.last_hidden_state[0][0]
        return cls_embedding
    
    dataset["cls_embedding"] = dataset.apply(get_cls_embedding, axis=1)
    dataset = dataset.drop(columns=["tokens", "input_ids", "attention_mask", "token_type_ids"])
    if path_to_output:
        with open(path_to_output, "wb") as f:
            pickle.dump(dataset, f)
    return dataset


