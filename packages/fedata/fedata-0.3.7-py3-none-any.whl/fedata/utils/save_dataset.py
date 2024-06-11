import datasets
import os

def save_dataset(path: str,
                 name: str,
                 loaded_dataset: int):
    n = os.path.join(path, name)
    dataset_length = len(loaded_dataset[1])
    dataset = {"orchestrator_test_set": loaded_dataset[0]}
    for client in range(dataset_length):
        dataset[f"client_{client}_train_set"] = loaded_dataset[1][client][0]
        dataset[f"client_{client}_test_set"] = loaded_dataset[1][client][1]
    print(f"The dataset was packed and will be save in format: {dataset}")
    dataset = datasets.DatasetDict(dataset)
    dataset.save_to_disk(n)