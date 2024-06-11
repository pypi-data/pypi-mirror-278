import numpy as np
import os
from Dataset import Dataset
from Hyperparameter import Hyperparameter
from Process import Process
if __name__ == '__main__':
    """
    read dataset path and transfer to matrix that could be put in the models
    """
    train_dataset_path = os.path.join("../../../dataset/split_train_and_test_dataset","LSM-5Year-split80-train.csv")
    test_dataset_path = os.path.join("../../../dataset/split_train_and_test_dataset","LSM-5Year-split20-test.csv")

    dataset = Dataset(train_dataset_path, test_dataset_path)
    X_train, Y_train, X_test, Y_test = dataset.X_train, dataset.Y_train, dataset.X_test, dataset.Y_test

    """
   Based on the provided hyperparameters grid, randomly generate a limited number of hyperparameter settings.
    """
    # length = X_train.shape[0]
    # dimension = X_train.shape[1]
    # hyperparameters_grid = {
    #     'number_of_hidden_nodes': np.arange(1, length + 1, step=1),
    #     'number_of_hidden_layer': [1, 2, 3, 4],
    #     'idim': [dimension],  # the dimension of the input layer
    #     'drate': np.arange(0, 0.51, step=0.01),
    #     'kinit': ['constant', 'glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform'],
    #     'iacti': ['relu', 'sigmoid', 'softmax', 'tanh'],
    #     'hacti': ['relu', 'sigmoid', 'softmax', 'tanh'],
    #     'oacti': ['sigmoid'],
    #     'opti': ['SGD', 'adam', 'Adagrad', 'Nadam', 'Adamax'],
    #     'lrate': np.arange(0.001, 0.101, step=0.001),
    #     'momen': np.arange(0.01, 1, step=0.01),
    #     'dec': np.arange(0, 0.101, step=0.001),
    #     'ls': ['binary_crossentropy'],
    #     'batch_size': np.arange(1, length + 1, step=1),
    #     'epochs': np.arange(5, 1001, step=1),
    #     'L1': np.arange(0, 0.101, step=0.001),
    #     'L2': np.arange(0, 0.101, step=0.001),
    #     'ltype': [3]
    # }
    #
    # # iter = 100
    # # handle_hyperparameters = Hyperparameter(hyperparameters_grid)
    # # hyperparameter_settings = handle_hyperparameters.get_hyperparameter_settings(iter)
    # # print(hyperparameter_settings)
    #
    # """
    # store hyperparameter settings
    # """
    # # handle_hyperparameters = Hyperparameter(hyperparameters_grid)
    # # hyperparameter_path = "test.csv"
    # # iter = 100
    # # handle_hyperparameters.get_hyperparameter_settings(iter)
    # # handle_hyperparameters.store_hyperparameter_settings(hyperparameter_path)
    #
    # """
    # already have a file stored hyperparameter settings, read it and retrieve hyperparameters
    # """
    # handle_hyperparameters = Hyperparameter()
    # hyperparameter_path = "test.csv"
    # hyperparameter_settings = handle_hyperparameters.retrieve_hyperparameter_settings(hyperparameter_path)
    # print(hyperparameter_settings)

    # """
    # could use the stored hyperparameter grids based on method name
    # """
    # handle_hyperparameters = Hyperparameter()
    # handle_hyperparameters.get_hyperparameter_grid( 'Adst', dataset)

    """
    train 
    """
    # handle_hyperparameters = Hyperparameter()
    # method_name = 'DecisionTree'
    # handle_hyperparameters.get_hyperparameter_grid(method_name, dataset)
    # handle_hyperparameters.get_hyperparameter_settings(2)
    # process = Process(dataset = dataset,
    #                   hyperparameter_settings = handle_hyperparameters.hyperparameter_settings,
    #                   method_name = method_name)
    # result_path = "test_result_without_test_auc.csv"
    # process.train_without_test(result_path=result_path)

    """
    train and test
    """
    handle_hyperparameters = Hyperparameter()
    method_name = 'SVC'
    handle_hyperparameters.get_hyperparameter_grid(method_name, dataset)
    handle_hyperparameters.get_hyperparameter_settings(2)
    process = Process(dataset=dataset,
                      hyperparameter_settings=handle_hyperparameters.hyperparameter_settings,
                      method_name=method_name)
    result_path = "test_result_with_test_auc.csv"
    process.train_with_test(result_path=result_path)

