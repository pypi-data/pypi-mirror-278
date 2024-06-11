import datasets
import os

def save_blueprint(dataset: list[datasets.arrow_dataset.Dataset, datasets.arrow_dataset.Dataset], 
                   path:str,
                   blueprine_name:str):
    name = os.path.join(path, (blueprine_name + ".csv"))
    with open(name, 'a+', ) as csv_file:
        orchestrator_data = dataset[0]
        nodes_data = dataset[1]
        
        # WRITE HEADERS
        header = ["client_id", "partition", "total_samples"]
        labels = nodes_data[0][0].features['label'].names
        header.extend(labels)
        csv_file.write(",".join(header) + '\n')
        
        translation = False
        try:
            labels = [int(label) for label in labels]
        except ValueError:
            translation = True
            labels_translation = {integer: label for (integer, label) in zip(range(len(labels)), labels)}
            labels = [value for value in labels_translation.keys()]

        # WRITE ORCHESTRATOR
        row = ['orchestrator', 'central_test_set', str(len(orchestrator_data))]
        for label in labels:
            row.append(str(len(orchestrator_data.filter(lambda inst: inst['label'] == label))))
        csv_file.write(",".join(row) + '\n')

        # WRITE CLIENTS
        for client, data in enumerate(nodes_data):
            row = [str(client), 'train_set', str(len(data[0]))]
            for label in labels:
                row.append(str(len(data[0].filter(lambda inst: inst['label'] == label))))
            csv_file.write(",".join(row) + '\n')

            row = [str(client), 'test_set', str(len(data[1]))]
            for label in labels:
                row.append(str(len(data[1].filter(lambda inst: inst['label'] == label))))
            csv_file.write(",".join(row) + '\n')
        
    #Optional: write labels (if translated)
    if translation:
        name = os.path.join(path, (blueprine_name + "translation" + ".txt"))
        with open(name, "w+") as txt_file:
            for integer, label in labels_translation.items():
                txt_file.write(f"{str(integer)}: {label}")