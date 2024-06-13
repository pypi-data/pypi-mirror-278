from transformers import (
    AutoTokenizer, 
    AutoModel,
    BertJapaneseTokenizer
    )
from process_twarc.util import (
    concat_dataset,
    get_files,
    make_dir,
    load_dict,
    get_output_path
    )
from tokenizers import (
    models,
    pre_tokenizers,
    trainers,
    Tokenizer
    )

from tqdm import tqdm
import torch
import pandas as pd
import os
from ntpath import basename


def build_tokenizer(
        training_corpus_dir: str,
        vocab_dir: str,
        new_tokenizer_dir: str,
        push_to_hub= "",
        vocab_size: int=32000,
        mask_low_freq_char: bool=True,
        standard_special_tokens = ["[PAD]", "[UNK]", "[CLS]", "[SEP]", "[MASK]"],
        additional_special_tokens = ["[URL]", "[USER]"],
        keep_newlines: bool=True,
        hashtags_masked: bool=True
):
    def get_training_corpus(dataset):
        for i in tqdm(range(0, len(dataset), 1000), desc="Training tokenizer"):
            yield dataset[i : i + 1000]["pre_tokenized"]
    
    def get_vocab():
        masks = "low_freq_char" if mask_low_freq_char else None

        dataset = concat_dataset(
            get_files(training_corpus_dir),
            output_type="Dataset",
            columns="pre_tokenized",
            masks=masks
        )
        trainer_special_tokens = standard_special_tokens + additional_special_tokens
        if keep_newlines:
            trainer_special_tokens = trainer_special_tokens + ["\n"]
        if hashtags_masked:
            trainer_special_tokens = trainer_special_tokens + ["#"]

        tokenizer = Tokenizer(models.WordPiece(unk_token="[UNK]"))
        tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()
        trainer = trainers.WordPieceTrainer(vocab_size=vocab_size, special_tokens=trainer_special_tokens)

        tokenizer.train_from_iterator(get_training_corpus(dataset), trainer=trainer)
        
        make_dir(vocab_dir)
        tokenizer_name = basename(training_corpus_dir)
        path_to_vocab_json = os.path.join(vocab_dir, f"{tokenizer_name}.json")
        tokenizer.save(path_to_vocab_json)
        return path_to_vocab_json, tokenizer_name
    
    def generate_sorted_vocab_list():
        path_to_vocab_json, tokenizer_name = get_vocab()
        vocab = list(load_dict(path_to_vocab_json)["model"]["vocab"].keys())
        vocab = [word for word in vocab if word != "\n"]
        length = lambda token: len(token.replace("##", ""))
        sort_key = lambda token: (length(token), token.startswith("##"), token)

        special_tokens = standard_special_tokens + additional_special_tokens
        non_special = [word for word in vocab if word not in special_tokens]
        non_special.sort(key=sort_key)
        sorted_vocab = special_tokens + non_special

        vocab_file = get_output_path(path_to_vocab_json, vocab_dir, file_type = "txt")
        with open(vocab_file, "w", encoding="utf-8") as f:
            f.write("\n".join(sorted_vocab))
        return vocab_file, tokenizer_name

    def configure_tokenizer():
        print("Configuring tokenizer...")
        vocab_file, tokenizer_name = generate_sorted_vocab_list()
        tokenizer = BertJapaneseTokenizer(
            vocab_file=vocab_file,
            word_tokenizer_type="mecab",
            mecab_kwargs={"mecab_dic": "unidic_lite"},
            keep_newlines=keep_newlines,
            model_max_length=512,
            additional_special_tokens=additional_special_tokens
        )
        if keep_newlines:
            tokenizer.add_tokens("\n")
        if additional_special_tokens:
            tokenizer.additional_special_tokens=additional_special_tokens
        
        tokenizer.save_pretrained(new_tokenizer_dir)
        print(f"Tokenizer saved to {new_tokenizer_dir}")
        if push_to_hub:
            tokenizer.push_to_hub(push_to_hub)
            print(f"Tokenizer pushed to {push_to_hub}")
    
    configure_tokenizer()

def build_model(
        path_to_new_tokenizer: str,
        ordered_donors: list,
        donate_token_embeddings: bool=True,
        donate_cls_embeddings: bool=True,
        push_to_hub: str=""
):
    
    def get_vocab(tokenizer):
        return set(tokenizer.get_vocab().keys())

    def get_tokenizers_and_models(
        ordered_donors,
        path_to_new_tokenizer=path_to_new_tokenizer
    ):
        if type(ordered_donors) == str:
            ordered_donors = [ordered_donors]
        
        load_tokenizer = lambda path: AutoTokenizer.from_pretrained(path)
        load_model = lambda path: AutoModel.from_pretrained(path)

        donors = {path: {
            "tokenizer": load_tokenizer(path),
            "model": load_model(path),
        } for path in ordered_donors}

        for path in donors.keys():
            donors[path]["vocab"] = get_vocab(donors[path]["tokenizer"])

        print()
        new_tokenizer = load_tokenizer(path_to_new_tokenizer)
        print(f"Initializing new from {ordered_donors[0]}...")
        new_model = load_model(ordered_donors[0])

        print(f"Resizing token embeddings to {len(new_tokenizer)}...")
        new_model.resize_token_embeddings(len(new_tokenizer))

        print(f"Initializing new token embeddings...")
        print()
        new_model.embeddings.word_embeddings.weight.data.normal_(mean=0.0, std=new_model.config.initializer_range)

        return donors, new_tokenizer, new_model
    
    def assign_donors(
        new_tokenizer,
        ordered_donors,
        donors, 
        donate_cls_embeddings=donate_cls_embeddings
        ):

        def assign_fn(token):
            for path in ordered_donors:
                if token in donors[path]["vocab"]:
                    return (path, "token")
            
            if donate_cls_embeddings:
                for path in ordered_donors:
                    if not "[UNK]" in donors[path]["tokenizer"].tokenize(token):
                        return (path, "cls")
            return ("random", None)
        
        vocab = get_vocab(new_tokenizer)
        assignments = [assign_fn(token) for token in vocab]

        donor_df = pd.DataFrame({
            "token": list(vocab),
            "donor": [a[0] for a in assignments],
            "method": [a[1] for a in assignments]
        })
        print_df = donor_df.groupby(["donor", "method"]).size().reset_index(name="counts")
        for i, row in print_df.iterrows():

            print(f"\n{row['donor']} donating {row['counts']} tokens using {row['method']} method\n")
        print()
        return donor_df

    def compare_embeddings(
            old_model,
            new_model,
            old_token_id,
            new_token_id
            ):
        old_embedding = old_model.embeddings.word_embeddings.weight[old_token_id]
        new_embedding = new_model.embeddings.word_embeddings.weight[new_token_id]
        similarity = torch.nn.functional.cosine_similarity(old_embedding, new_embedding, dim=0)
        return similarity.item()

    def migrate_token_embeddings(
            new_tokenizer,
            new_model,
            tokens,
            donor
            ):
        
        donor_tokenizer, donor_model = donor["tokenizer"], donor["model"]
        token_id_mapping = {}
        with torch.no_grad():
            for token in tqdm(tokens):
                old_token_id = donor_tokenizer.convert_tokens_to_ids(token)
                new_token_id = new_tokenizer.convert_tokens_to_ids(token)
                new_model.embeddings.word_embeddings.weight[new_token_id] = donor_model.embeddings.word_embeddings.weight[old_token_id]
                token_id_mapping[old_token_id] = new_token_id
        threshold = 0.9
        mismatched_tokens = []
        for old_token_id, new_token_id in token_id_mapping.items():
            similarity = compare_embeddings(donor_model, new_model, old_token_id, new_token_id)
            if similarity < threshold:
                mismatched_tokens.append(new_tokenizer.convert_ids_to_tokens(new_token_id))

        if not mismatched_tokens:
            print()
            print("All migrated embeddings are similar above the threshold.")
        else:
            print(f"Mismatched tokens: {mismatched_tokens}")
        return new_model

    def migrate_cls_embeddings(
            new_tokenizer,
            new_model,
            tokens,
            donor):
        
        donor_tokenizer, donor_model = donor["tokenizer"], donor["model"]
        with torch.no_grad():
            for token in tqdm(tokens):
                inputs = donor_tokenizer(token, return_tensors="pt", add_special_tokens=True)
                input_ids = inputs['input_ids']
                attention_mask = inputs['attention_mask']

                ouputs = donor_model(input_ids, attention_mask=attention_mask)
                
                cls_embedding = ouputs.last_hidden_state[:, 0, :]
                new_token_id = new_tokenizer.convert_tokens_to_ids(token)
                new_model.embeddings.word_embeddings.weight[new_token_id] = cls_embedding
        return new_model
    
    donors, new_tokenizer, new_model = get_tokenizers_and_models(ordered_donors)

    donor_df = assign_donors(new_tokenizer, ordered_donors, donors)
    for group, df in donor_df.groupby(["donor", "method"] ):
        if group[1] == "token" and donate_token_embeddings:
            print(f"Migrating token embeddings from {group[0]}...")
            new_model = migrate_token_embeddings(new_tokenizer, new_model, df["token"], donors[group[0]])
        elif group[1] == "cls" and donate_cls_embeddings:
            print(f"Migrating cls embeddings from {group[0]}...")
            new_model = migrate_cls_embeddings(new_tokenizer, new_model, df["token"], donors[group[0]])
    
    new_model.save_pretrained(path_to_new_tokenizer)
    new_tokenizer.save_pretrained(path_to_new_tokenizer)
    print(f"Model saved to {path_to_new_tokenizer}")
    if push_to_hub:
        new_model.push_to_hub(push_to_hub)
        new_tokenizer.push_to_hub(push_to_hub)
        print(f"Model pushed to {push_to_hub}")

def build_tokenizer_and_model(
        training_corpus_dir: str,
        ordered_donors: list,
        vocab_dir: str="vocab",
        model_dir: str="new_model",
        push_to_hub: str="",
        vocab_size: int=32000,
        mask_low_freq_char: bool=True,
        standard_special_tokens = ["[PAD]", "[UNK]", "[CLS]", "[SEP]", "[MASK]"],
        additional_special_tokens = ["[URL]", "[USER]"],
        keep_newlines: bool=True,
        hashtags_masked: bool=True,
        donate_token_embeddings: bool=True,
        donate_cls_embeddings: bool=True
):

    build_tokenizer(
        training_corpus_dir=training_corpus_dir,
        vocab_dir=vocab_dir,
        new_tokenizer_dir=model_dir,
        push_to_hub=push_to_hub,
        vocab_size=vocab_size,
        mask_low_freq_char=mask_low_freq_char,
        standard_special_tokens=standard_special_tokens,
        additional_special_tokens=additional_special_tokens,
        keep_newlines=keep_newlines,
        hashtags_masked=hashtags_masked
    )
    build_model(
        path_to_new_tokenizer=model_dir,
        ordered_donors=ordered_donors,
        donate_token_embeddings=donate_token_embeddings,
        donate_cls_embeddings=donate_cls_embeddings,
        push_to_hub=push_to_hub
    )
    
