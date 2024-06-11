import logging
import datasets
from fedata.load.load_cifar import load_cifar
from fedata.load.load_fmnist import load_fmnist
from fedata.load.load_mnist import load_mnist
from fedata.utils.save_blueprint import save_blueprint
from fedata.exceptions.fetchdataexceptions import InvalidDatasetName
from fedata.utils.save_dataset import save_dataset
import pickle
import os

def load_data(settings:dict) -> list[datasets.arrow_dataset.Dataset,
                                       list[list[list[datasets.arrow_dataset.Dataset]]]]:
    """Loads specified dataset, splits it into the number of shards, pre-process selected
    shards (subsets) and returns in a following format:
    list[   
        "Orchestrator Data"[
            Dataset
            ],   
        "Agents Data"[
            "Agent N"[
                "Train Data"[
                Dataset
                ],
                "Test Data"[
                Dataset
                ]
            ]]]
    Where all 'Datasets' are an instances of hugging face container datasets.arrow_dataset.Dataset
    ---------
    Args:
        settings (dict) : A dictionary containing all the dataset settings.
    Returns:
        list[datasets.arrow_dataset.Dataset,
                                       list[list[list[datasets.arrow_dataset.Dataset]]]]"""
    
    dataset_name = settings['dataset_name']
    if dataset_name == 'mnist':
        loaded_dataset = load_mnist(settings=settings)
        if settings['save_dataset'] == True:
            dataset_name = f"MNIST_{settings['shards']}_dataset_pointers"
            path = os.path.join(settings['save_path'])
            with open(os.path.join(path, dataset_name), 'wb') as file:
                pickle.dump(loaded_dataset, file)
            save_dataset(path=path, name=f"MNIST_{settings['shards']}_dataset", loaded_dataset=loaded_dataset)
        if settings['save_blueprint'] == True:
            blueprint_name = f"MNIST_{settings['shards']}_dataset_blueprint"
            save_blueprint(loaded_dataset, settings['save_path'], blueprint_name)
        return loaded_dataset
    elif dataset_name == 'cifar10':
        loaded_dataset = load_cifar(settings=settings)
        if settings['save_dataset'] == True:
            dataset_name = f"CIFAR10_{settings['shards']}_dataset_pointers"
            path = os.path.join(settings['save_path'])
            with open(os.path.join(path, dataset_name), 'wb') as file:
                pickle.dump(loaded_dataset, file)
            save_dataset(path=path, name=f"CIFAR10_{settings['shards']}_dataset", loaded_dataset=loaded_dataset)
        if settings['save_blueprint'] == True:
            blueprint_name = f"CIFAR10_{settings['shards']}_dataset_blueprint"
            save_blueprint(loaded_dataset, settings['save_path'], blueprint_name)
        return loaded_dataset
    elif dataset_name == 'fmnist':
        loaded_dataset = load_fmnist(settings=settings)
        if settings['save_dataset'] == True:
            dataset_name = f"FMNIST_{settings['shards']}_dataset_pointers"
            path = os.path.join(settings['save_path'])
            with open(os.path.join(path, dataset_name), 'wb') as file:
                pickle.dump(loaded_dataset, file)
            save_dataset(path=path, name=f"FMNIST_{settings['shards']}_dataset", loaded_dataset=loaded_dataset)
        if settings['save_blueprint'] == True:
            blueprint_name = f"FMNIST_{settings['shards']}_dataset_blueprint"
            save_blueprint(loaded_dataset, settings['save_path'], blueprint_name)
        return loaded_dataset
    else:
        raise InvalidDatasetName
       