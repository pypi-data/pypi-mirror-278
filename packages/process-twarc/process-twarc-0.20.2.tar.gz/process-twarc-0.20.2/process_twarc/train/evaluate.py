import sqlite3
import pandas as pd
from pandas import ExcelWriter
from process_twarc.util import load_dict, make_dir
from process_twarc.train.util import load_splits, get_compute_metrics
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, pipeline, AutoModelForMultipleChoice, AutoModelForQuestionAnswering
import os
from tqdm import tqdm
import shutil
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from adapters import AutoAdapterModel, AdapterTrainer
from datasets import concatenate_datasets
import logging

def generate_summary_table(
    path_to_db: str,
    n_best_trials: int=int(),
    path_to_trial_results: str=None
    ):
    """Generate a summary table of the best trials from an SQL database."""

    def SQL_to_pandas(path_to_db: str) -> dict:
        """Get data from an SQL database and return a dictionary of DataFrames."""

        def query(
            path_to_db: str,
            table_name: str,
            column_names: list=None
        ) -> pd.DataFrame:
            """Query an SQL database and return a Pandas DataFrame."""
            
            conn = sqlite3.connect(path_to_db)
            c = conn.cursor()
            
            if column_names is None:
                c.execute(f"SELECT * FROM {table_name}")
                column_names = [description[0] for description in c.description]
            else:
                # Validate column names to make sure they're properly formatted
                if not all(isinstance(col, str) for col in column_names):
                    print("Error: All column names must be strings.")
                    return None
            
            column_names_str = ", ".join(column_names)
            c.execute(f"SELECT {column_names_str} FROM {table_name}")
            
            rows = c.fetchall()
            df = pd.DataFrame(rows, columns=column_names)
            
            conn.close()
            
            return df

        queries = {
        "studies": [
            "study_id",
            "study_name"
        ],
        "study_directions": [
            "direction",
            "study_id"
        ],
        "trials": [
            "trial_id",
            "number",
            "study_id",
            "state"
        ],
        "trial_values": [
            "trial_id",
            "value"
        ],
        "trial_intermediate_values": [
            "trial_id",
            "step"
        ],
        "trial_params": [
            "trial_id",
            "param_name",
            "param_value"
        ]
        }
        
        data = {}
        for table_name, column_names in queries.items():
            data[table_name] = query(path_to_db, table_name, column_names)
        
        return data


    def get_run_name(row):
        trial = f"trial-{str(row['number']+1).zfill(3)}"
        return f"{row['study_name']}/{trial}"

    def get_epochs(trial_intermediate_values):
        trial_id2epoch = {}
        for group, df in trial_intermediate_values.groupby("trial_id"):
            trial_id2epoch[group] = len(df)
        return trial_id2epoch

    def get_params(trial_params):
        trial_id2params = {}
        for group, df in trial_params.groupby("trial_id"):
            trial_id2params[group] = df.set_index("param_name")["param_value"].to_dict()
        return trial_id2params

    def unpack_params(row):
        params = row["params"]
        for param, value in params.items():
            row[param] = value
        return row
    
    print("Generating summary table.")
    data = SQL_to_pandas(path_to_db)
    trial_values = data["trial_values"]
    trial_values = trial_values.merge(data["trials"], on="trial_id")
    trial_values = trial_values.merge(data["studies"], on="study_id")
    trial_values = trial_values.merge(data["study_directions"], on="study_id")
    trial_values = trial_values[trial_values["state"] == "COMPLETE"]
    trial_values["epochs"] = trial_values["trial_id"].map(get_epochs(data["trial_intermediate_values"]))
    trial_values["params"] = trial_values["trial_id"].map(get_params(data["trial_params"]))
    trial_values = trial_values.apply(unpack_params, axis=1)
    trial_values["run_name"] = trial_values.apply(get_run_name, axis=1)
    #make a dictionary of trial values where the key is the study name
    trial_values = {group: df for group, df in trial_values.groupby("study_name")}

    if n_best_trials:
        print(f"Trimming to best trials. {n_best_trials=}")
        best_trials = {}
        for group, df in trial_values.items():
           
            direction = df["direction"].iloc[0]
            if direction == "MAXIMIZE":
                ascending=False
            else:
                ascending=True
            df = df.sort_values("value", ascending=ascending).reset_index(drop=True)
            if n_best_trials > len(df):
                print(f"Warning: {group} has less than {n_best_trials} trials.")
                best_trials[group] = df
            else:
                best_trials[group] = df[:n_best_trials]
        trial_values = best_trials

    if path_to_trial_results:
        print(f"Saving to {path_to_trial_results}.")
        with ExcelWriter(path_to_trial_results) as writer:
            for study_name, df in trial_values.items():
                if "/" in study_name:
                    study_name = study_name.split("/")[-1]
                df = df[[col for col in df.columns if "Unnamed" not in col]]
                df.to_excel(writer, sheet_name=study_name, index=True if study_name =="summary" else False)

    
    return trial_values

def check_results(
    path_to_trial_results: dict,
    path_to_config: str,
    groups_to_finish: list=[],
    only_check_groups_to_finish: bool=True,
    finished_groups: list=[],
    project: str=None
):
    
    def check_trials(
            trials = pd.read_excel(path_to_trial_results, sheet_name=None),
            config = load_dict(path_to_config)
            ):


        for group, df in trials.items():
            if group in finished_groups:
                print(f"Skipping {group} because it is finished.")
                continue
            if only_check_groups_to_finish and group not in groups_to_finish:
                print(f"Skipping {group} because it is not finished..")
                continue
            else:
                print(f"Checking {group}.")

            def retrieve_parameters(group=group, config=config):
                fixed = config["fixed_parameters"]
                group = config["group_parameters"].get(group, {})
                parameters = {**fixed, **group} 
                return parameters
            

            def retrieve_splits(parameters):
                tokenizer = AutoTokenizer.from_pretrained(parameters["path_to_model"])
                datasets = load_splits(parameters, tokenizer)

                datasets = {k: v for k, v in datasets.items() if not any(x in k for x in ["train", "validation"])}
                unique_splits = list(set([k.split("_")[-1] for k in datasets.keys()]))
                for split in unique_splits:
                    datasets[split] = concatenate_datasets([v for k, v in datasets.items() if k.endswith(split)])
                # load = lambda data_dir, task, columns, tokenizer_kwargs, splits: load_splits(
                #     data_dir=data_dir,
                #     task=task,
                #     column_dict=columns,
                #     tokenizer_kwargs=tokenizer_kwargs,
                #     splits=splits,
                #     tokenizer=tokenizer
                # )

                # dataset_kwargs = parameters["dataset_kwargs"]
                # multi_dataset = dataset_kwargs.get("multi_dataset", False)
                # if multi_dataset:
                #     dataset_kwargs = [v for k, v in dataset_kwargs.items() if k != "multi_dataset"]
                # else:
                #     dataset_kwargs = [dataset_kwargs]
                
                # for kwargs in dataset_kwargs:
                #     prefix = kwargs.get("prefix", "")
                #     splits = [s for s in kwargs["splits"] if s != "train"]
                #     datasets = load(
                #         data_dir=kwargs["data_dir"],
                #         task=parameters["task"],
                #         columns = kwargs["columns"],
                #         tokenizer_kwargs=parameters["tokenizer_kwargs"],
                #         splits=splits
                #     )
                #     if prefix:
                #         datasets = {f"{prefix}_{k}": v for k, v in datasets.items()}
                
                # for split in splits:
                #     datasets[split] =  concatenate_datasets([ds for k, ds in datasets.items() if k.endswith(split)])

                return datasets, tokenizer
            
            def get_model(parameters, path_to_trained):
                if "adapter_kwargs" in parameters:
                    adapter_kwargs = parameters["adapter_kwargs"]
                    model = AutoAdapterModel.from_pretrained(parameters["path_to_model"])


                    adapter = model.load_adapter(os.path.join(path_to_trained, adapter_kwargs["name"]), with_head=True)
                    model.set_active_adapters(adapter)
                    print("Adapter model loaded.")
                    return model
                
                task = parameters["task"]
                if task in ["sequence_classification", "sequence_pair_classification"]:
                    model_class = AutoModelForSequenceClassification
                elif task == "multiple_choice":
                    model_class = AutoModelForMultipleChoice
                elif task == "JSQuAD":
                    model_class = AutoModelForQuestionAnswering
                
                return model_class.from_pretrained(path_to_trained)
            
  
            def init_trainer(run_name, parameters, tokenizer, project=project):
                project = project if project else parameters["project"]
                trained = os.path.join(parameters["completed_dir"], project, run_name)
                if not os.path.exists(trained):
                    print(f"Model {run_name} does not exist. Skipping...")
                    return None
                
                trainer_class = AdapterTrainer if parameters.get("adapter_kwargs") else Trainer

                trainer = trainer_class(
                    model=get_model(parameters, trained),
                    tokenizer=tokenizer)
                return trainer
            
            def evaluate(run_name, parameters, datasets, tokenizer):
                logging.basicConfig(level=logging.DEBUG)

                trainer = init_trainer(run_name, parameters, tokenizer)
                if not trainer:
                        logging.debug("Trainer initialization failed.")
                        return None
                
                logging.debug(f"Trainer initialized for run: {run_name}")

                evaluation_kwargs = parameters["evaluation_kwargs"]
                preset_metrics = evaluation_kwargs.get("preset_metrics")
                if preset_metrics == "stsb":
                    all_metrics = ["loss", "pearson", "spearmanr"]
                elif preset_metrics == "squad":
                    all_metrics = ["loss", "exact_match", "f1"]
                elif preset_metrics == "wrime":
                    all_metrics = ["loss", "top_choice_accuracy", "f1", "multi_label_pearson", "precision", "recall", "roc_auc"]
                
                else:
                    all_metrics = ["loss"] + evaluation_kwargs.get("metrics", [])

                results = {}
                for split, dataset in datasets.items():
                    # Skip validation datasets
                    if "validation" in split:
                        continue

                    logging.debug(f"Evaluating {split} split with {len(dataset)} examples")

                    # Skip if dataset is None or empty
                    if dataset is None or len(dataset) == 0:
                        logging.debug(f"No data available for {split} split, skipping...")
                        continue

                    # Setting up metrics computation
                    trainer.compute_metrics = get_compute_metrics(parameters, tokenizer, datasets, split)

                    # Attempt to evaluate the dataset
                    try:
                        values = trainer.evaluate(dataset)
                        logging.debug(f"Results for {split}: {values}")
                    except Exception as e:
                        logging.error(f"Error during evaluation of {split} split: {str(e)}")
                        continue

                    # Process and log the results for each metric
                    for metric in all_metrics:
                        if f"eval_{metric}" in values:
                            result_value = values.get(f"eval_{metric}", 0)
                            results[f"{split}_{metric}"] = result_value
                            print(f"{split}_{metric}: {result_value}")
                        else:
                            logging.warning(f"Metric '{metric}' not found in results for {split}")

                # Calculate combined results for each metric except 'loss'
                for metric in all_metrics:
                    if metric == "loss":
                        continue
                    try:
                        combined_metric_key = f"combined_{metric}"
                        dev_metric_key = f"development_{metric}"
                        test_metric_key = f"test_{metric}"

                        # Ensure both metrics exist before combining them
                        if dev_metric_key in results and test_metric_key in results:
                            results[combined_metric_key] = (results[dev_metric_key] + results[test_metric_key]) / 2
                            logging.debug(f"Computed {combined_metric_key}: {results[combined_metric_key]}")
                        else:
                            logging.warning(f"Could not compute {combined_metric_key} due to missing data.")
                    except Exception as e:
                        logging.error(f"Error computing combined metric {metric}: {str(e)}")

                return results
            
            def validate_results(df, parameters):
                metric_for_best_trial = parameters["metric_for_best_trial"].replace("eval_", "")
                df["validated"] = df.apply(lambda x: abs(x[f"development_{metric_for_best_trial}"] - x["value"]) <= 1e-4 * max(1e-4, abs(x[f"development_{metric_for_best_trial}"]), abs(x["value"])), axis=1)
                return df

            parameters = retrieve_parameters()
            datasets, tokenizer = retrieve_splits(parameters)

            for idx, row in tqdm(df.iterrows(), desc=f"Checking {group}"):
                run_name = row["run_name"]
                results = evaluate(run_name, parameters, datasets, tokenizer)
                if not results:
                    continue
                for key, value in results.items():
                    df.at[idx, key] = value
            df = df.dropna().reset_index(drop=True)
            df = validate_results(df, parameters)
            trials[group] = df
        return trials
            
    
    def generate_summary_sheet(trials):
        output = {}
        checked = {group: df for group, df in trials.items() if "validated" in df.columns}
        if not checked:
            print("No finished groups to summarize.")
            return trials

        for group, df in checked.items():
            df = df[[col for col in df.columns if any(x in col for x in ["epoch", "development", "test", "combined", "value"])]]
            df = df.drop(columns=["validated"], errors='ignore')  # Use errors='ignore' to avoid KeyError if the column doesn't exist
            summary = {}

            # Calculate summary for epochs
            if "epochs" in df.columns:
                summary[("epochs", "mean")] = int(df["epochs"].mean())
                summary[("epochs", "std")] = int(df["epochs"].std())

            # Calculate summary for other columns
            for col in [c for c in df.columns if c not in ["epochs", "value"]]:  # Exclude 'value' from the loop
                summary[(col, "mean")] = df[col].mean().round(3)
                summary[(col, "std")] = df[col].std().round(3)
                summary[(col, "min")] = df[col].min().round(3)
                summary[(col, "max")] = df[col].max().round(3)
                if "value" in df.columns:  # Ensure 'value' column exists for correlation calculation
                    summary[(col, "value_corr")] = df[col].corr(df["value"]).round(3)

            # Store the summary for the current group
            output[group] = summary

        # Convert the output dictionary to a DataFrame with super columns
        summary_df = pd.DataFrame(output).T  # Transpose to get groups as rows and summaries as columns
        summary_df.columns = pd.MultiIndex.from_tuples(summary_df.columns)  # Create MultiIndex for super columns
        trials["summary"] = summary_df
        return trials

    trials = check_trials()
    trials = generate_summary_sheet(trials)
    with ExcelWriter(path_to_trial_results) as writer:
        for group, df in trials.items():
            df.to_excel(writer, sheet_name=group, index=True if group =="summary" else False)
    return

def copy_best_trials(
        path_to_trial_results: str,
        groups_to_finish: list,
        path_to_config: str,
        best_trials_dir: str,
        n_best_trials: int=10,
        finished_groups: list=[],
        project = None
):
    parameters = load_dict(path_to_config)["fixed_parameters"]
    project = project if project else parameters["project"]
    metric_for_best_results = parameters["metric_for_best_results"].replace("eval_", "")

    completed_trials_dir = os.path.join(parameters["completed_dir"], project)
    best_results_column = f"combined_{metric_for_best_results}"

    trials = pd.read_excel(path_to_trial_results, sheet_name=None)
    #iterate through sheets
    for name, df in trials.items():
        if name not in groups_to_finish:
            continue
        if name in finished_groups:
            print(f"Skipping {name} because it is finished.")
            continue
        print(f"Copying best trials for {name}.")
        if n_best_trials:
            ascending = True if metric_for_best_results == "loss" else False
            df = df.sort_values(best_results_column, ascending=ascending)[:n_best_trials].reset_index(drop=True)

        for _, row in df.iterrows():
            run_name = row["run_name"]
            source_path = os.path.join(completed_trials_dir, run_name)
            dest_path = os.path.join(best_trials_dir, run_name)
            if os.path.exists(source_path):
                if not os.path.exists(dest_path):
                    shutil.copytree(source_path, dest_path)
                else:
                    print(f"Destination directory {dest_path} already exists. Skipping...")
            else:
                print(f"Source directory {source_path} does not exist. Skipping...")

# def generate_test_results_boxplot(
#         path_to_trial_results: str,
#         value_column: str,
#         groups: list=None, 
#         title=""):
#     """
#     This function takes a dictionary where keys are model names and values are DataFrames containing
#     trial_id, epochs, and test_results. It generates a combined box plot for the test_results of all models.
    
#     Parameters:
#     - results: dict, where keys are model names and values are DataFrames.
#     """
#     trials = pd.read_excel(path_to_trial_results, sheet_name=None)
#     if groups:
#         trials = {group: df for group, df in trials.items() if group in groups}
#     # Initialize an empty DataFrame for combined results
#     combined_df = pd.DataFrame()
    
#     # Loop through each model and its DataFrame, appending the data with an additional 'Model' column
#     for model_name, df in trials.items():
#         df['Model'] = model_name  # Add a column with the model name
#         combined_df = pd.concat([combined_df, df], ignore_index=True).dropna()
    
#     # Create a combined box plot
#     plt.figure(figsize=(10, 6))
#     sns.boxplot(x='Model', y=value_column, data=combined_df)
    
#     plt.title(title)
#     plt.xlabel('Model')
#     plt.ylabel(f'{" ".join(value_column.split("_")).title()}')
#     plt.grid(True, axis='y')

#     # Show the plot
#     plt.show()

# def generate_test_results_CM(
#         results_dir: str,
#         best_trials_dir:str,
#         splits_dir: str,
#         path_to_config: str,
#         ):
#         groups = os.listdir(best_trials_dir)
#         CM_dir = os.path.join(results_dir, "confusion-matrices")

#         for group in groups:
#             output_dir = os.path.join(CM_dir, group)
#             make_dir(output_dir)

#             def get_predictions(
#             trial,
#             path_to_config=path_to_config,
#             group=group,
#             best_trials_dir=best_trials_dir
#             ):
#                 parameters = load_dict(path_to_config)
#                 trained = os.path.join(best_trials_dir, group, trial)
#                 # if "adapter_name" in parameters["fixed_parameters"]:
#                 #     model = AutoModelForSequenceClassification.from_pretrained(parameters["path_to_model"])
#                 #     init(model)
#                 #     adapter = model.load_adapter(trained)
#                 #     model.set_active_adapters(adapter)
#                 #     print("Adapter model loaded.")
#                 # else:
#                 model = AutoModelForSequenceClassification.from_pretrained(trained)
#                 tokenizer = AutoTokenizer.from_pretrained(trained)

                
#                 parameters = {**parameters["fixed_parameters"], **parameters["group_parameters"].get(group, {})}
#                 dataset_kwargs = parameters["dataset_kwargs"]
#                 multi_dataset = dataset_kwargs.get("multi_dataset", False)
#                 if multi_dataset:
#                     dataset_kwargs = [v for k, v in dataset_kwargs.items() if k != "multi_dataset"]
#                 else:
#                     dataset_kwargs = [dataset_kwargs]

#                 if "soft" in label_column:
#                     label_column = label_column.replace("soft", "hard")
#                 dataset = load_splits(
#                     data_dir=splits_dir,
#                     splits=["test"],
#                     tokenizer=tokenizer,
#                     label_column=label_column
#                 )["test"]

#                 id2label = model.config.id2label
#                 dataset = dataset.map(lambda example: {"label": id2label[example["label"]]})

#                 nlp = pipeline("text-classification", model=model, tokenizer=tokenizer, framework="pt")
#                 predict_fn = lambda example: nlp(example["text"])[0]["label"]
#                 dataset = dataset.map(lambda example: {"prediction": predict_fn(example)})
#                 return dataset, id2label, output_dir

#             def build_confusion_matrix(dataset, id2label, output_dir, trial):
#                 # Initialize the confusion matrix
#                 cm = np.zeros((len(id2label), len(id2label)))

#                 # Convert dataset columns to numpy arrays
#                 true_labels = np.array(dataset["label"])
#                 predicted_labels = np.array(dataset["prediction"])
#                 sorted_labels = sorted(set(id2label.values()))

#                 # Create label to index mapping
#                 label2idx = {label: idx for idx, label in enumerate(sorted_labels)}

#                 # Fill the confusion matrix
#                 for t, p in zip(true_labels, predicted_labels):
#                     cm[label2idx[t], label2idx[p]] += 1

#                 # Save the confusion matrix and labels
#                 np.savez_compressed(os.path.join(output_dir, f"{trial}.npz"), cm=cm, labels=sorted_labels)


#             for trial in os.listdir(os.path.join(best_trials_dir, group)):
#                 if os.path.exists(os.path.join(output_dir, f"{trial}.npz")):
#                     print(f"Confusion matrix for {trial} already exists. Skipping...")
#                     continue
#                 dataset, id2label, output_dir = get_predictions(trial)
#                 build_confusion_matrix(dataset, id2label, output_dir, trial)


def evaluate_pipeline(
    path_to_db: str,
    results_dir: str,
    path_to_config: dict,
    project: str=None,
    restart: bool=True,
    generate_confusion_matrices: bool=True,
    boxplot_settings: dict=None,
    evaluate_n_best_trials: int=int(),
    groups_to_finish: list=None,
    only_check_groups_to_finish: bool=True,
    copy_n_best_trials: int=10
):
    #Makes directories for everything
    def init_evaluation(results_dir=results_dir):
        best_trials_dir = os.path.join(results_dir, "best-trials")
        path_to_results = os.path.join(results_dir, "results.xlsx")
        make_dir(results_dir), make_dir(best_trials_dir)
        finished_groups = os.listdir(best_trials_dir)
        return path_to_results, best_trials_dir, finished_groups

    def get_results(
            path_to_db=path_to_db,
            restart=restart,
            evaluate_n_best_trials=evaluate_n_best_trials,
            ):
        
        path_to_results, best_trials_dir, finished_groups= init_evaluation()
        if not os.path.exists(path_to_results):
            generate_summary_table(
                path_to_db=path_to_db,
                n_best_trials=evaluate_n_best_trials,
                path_to_trial_results=path_to_results
            )
        else:
            if restart:
                old_results = pd.read_excel(path_to_results, sheet_name=None)
                new_results = generate_summary_table(
                    path_to_db=path_to_db,
                    n_best_trials=evaluate_n_best_trials
                )
                if not finished_groups:
                    pass
                else:
                    for group in finished_groups:
                        new_results[group] = old_results[group]
                with ExcelWriter(path_to_results) as writer:
                    for group, df in new_results.items():
                        df.to_excel(writer, sheet_name=group, index = True if group == "summary" else False)
        return path_to_results, best_trials_dir, finished_groups
    
    path_to_results, best_trials_dir, finished_groups = get_results()
    
    check_results(
        path_to_trial_results=path_to_results,
        path_to_config=path_to_config,
        groups_to_finish=groups_to_finish,
        only_check_groups_to_finish=only_check_groups_to_finish,
        finished_groups=finished_groups,
        project=project
    )

    # if boxplot_settings:
    #     generate_test_results_boxplot(
    #         results=pd.read_excel(path_to_results, sheet_name=None),
    #         **boxplot_settings
    #     )
    
    

    # if groups_to_finish and copy_n_best_trials:
    #     copy_best_trials(
    #         path_to_trial_results=path_to_results,
    #         groups_to_finish=groups_to_finish,
    #         path_to_config=path_to_config,
    #         best_trials_dir=best_trials_dir,
    #         n_best_trials=copy_n_best_trials,
    #         finished_groups=finished_groups,
    #         project=project
    #     )

    # if generate_confusion_matrices:
    #     generate_test_results_CM(
    #         results_dir=results_dir,
    #         best_trials_dir=best_trials_dir,
    #         splits_dir=splits_dir,
    #         path_to_config=path_to_config
    #     )
