import random
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier


class Hyperparameter:
    def __init__(self, hyperparameters_grid = {}, hyperparameter_settings = []):
        self.hyperparameter_grid= hyperparameters_grid
        self.hyperparameter_settings = hyperparameter_settings

    def get_hyperparameter_settings(self, iter):
        for i in range(iter):
            self.hyperparameter_settings.append(self.choose_hyperparameter_setting_for_one_iter())
        return self.hyperparameter_settings

    def choose_hyperparameter_setting_for_one_iter(self):
        random_params = {}
        if 'number_of_hidden_layer' in self.hyperparameter_grid and 'number_of_hidden_nodes' in self.hyperparameter_grid:
            number_of_hidden_layer, number_of_hidden_nodes = random.sample(self.hyperparameter_grid['number_of_hidden_layer'], 1)[0], \
                                                             self.hyperparameter_grid['number_of_hidden_nodes']
            random_params['mstruct'] = [self.create_a_network(number_of_hidden_layer, low=number_of_hidden_nodes[0],
                                                              high=number_of_hidden_nodes[-1])]
        for k, v in self.hyperparameter_grid.items():
            if k == 'number_of_hidden_layer' or k == 'number_of_hidden_nodes': continue
            random_params[k] = random.sample(list(self.hyperparameter_grid[k]), 1)
            if isinstance(random_params[k][0], np.float64):
                random_params[k][0] = round(random_params[k][0], 5)
        return random_params

    def store_hyperparameter_settings(self, hyperparameter_path):
        if len(self.hyperparameter_settings) != 0:
            for hyperparameter_setting in self.hyperparameter_settings:
                for key in hyperparameter_setting:
                    hyperparameter_setting[key] = hyperparameter_setting[key][0]
            df = pd.DataFrame(self.hyperparameter_settings)
            df.to_csv(hyperparameter_path, index = False)
        else:
            print("error!You didn't have hyperparameter settings, please use /get_hyperparameter_settings/ function")

    def retrieve_hyperparameter_settings(self, hyperparameter_path):
        hyperparameters_df = pd.read_csv(hyperparameter_path)
        #hyperparameters_df = hyperparameters_df.drop(columns=['running_times'])
        if 'mstruct' in hyperparameters_df.columns:
            hyperparameters_df['mstruct'] = [eval(x) for x in hyperparameters_df['mstruct']]
            self.hyperparameter_settings = hyperparameters_df.to_dict(orient='records')

        return self.hyperparameter_settings
    def create_a_network(self, number_of_hidden_layer, low, high):
        network = []
        for i in range(number_of_hidden_layer):
            network.append(random.randint(low, high))
        network.append(1)
        return tuple(network)

    def correct_hyperparameters_type(self, hyperparameters):
        hyperparameter_settings = [eval(h) for h in hyperparameters]
        return hyperparameter_settings

    def change_hyperparameters_values(self, hyperparameters, new_hyperparameter_values):
        for i in range(len(hyperparameters)):
            for key in new_hyperparameter_values:
                hyperparameters[i][key] = new_hyperparameter_values[key][i]
            for key in hyperparameters[i]:
                hyperparameters[i][key] = [hyperparameters[i][key]]
        return hyperparameters

    def get_hyperparameter_grid(self,method_name, dataset):
        try:
            self.X_train, self.Y_train, self.X_test, self.Y_test = dataset.X_train, dataset.Y_train, dataset.X_test, dataset.Y_test
            hyperparameter_grids = {
                "DFNN":
                    {
                        'number_of_hidden_nodes': np.arange(1, len(self.X_train) + 1, step=1),
                        'number_of_hidden_layer': [1, 2, 3, 4],
                        'idim': [len(self.X_train[0])],  # the dimension of the input layer
                        'drate': np.arange(0, 0.51, step=0.01),
                        'kinit': ['constant', 'glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform'],
                        'iacti': ['relu', 'sigmoid', 'softmax', 'tanh'],
                        'hacti': ['relu', 'sigmoid', 'softmax', 'tanh'],
                        'oacti': ['sigmoid'],
                        'opti': ['SGD', 'adam', 'Adagrad', 'Nadam', 'Adamax'],
                        'lrate': np.arange(0.001, 0.101, step=0.001),
                        'momen': np.arange(0.01, 1, step=0.01),
                        'dec': np.arange(0, 0.101, step=0.001),
                        'ls': ['binary_crossentropy'],
                        'batch_size': np.arange(1, len(self.X_train) + 1, step=1),
                        'epochs': np.arange(5, 1001, step=1),
                        'L1': np.arange(0, 0.101, step=0.001),
                        'L2': np.arange(0, 0.101, step=0.001),
                        'ltype': [3]
                    },
                "AdaBoost":
                    {
                        "base_estimator": [LogisticRegression(), RandomForestClassifier(), DecisionTreeClassifier()],
                        "n_estimators": np.arange(1, 1001, step=1),
                        'learning_rate': np.arange(0.001, 0.101, step=0.001),
                        "algorithm": ["SAMME"]
                    },
                "NaiveBayes":
                    {
                        'alpha': np.arange(0.00001, 100.0001, step=0.00001),  # usually 0 - 10 is the range
                        'min_categories': np.arange(5, 16, step=1),  # based on  our datset, should be more than 4
                        'fit_prior': [True, False]
                    },
                "DecisionTree":
                    {
                        "criterion": ["gini", "entropy", "log_loss"],
                        "splitter": ["best", "random"],
                        "max_depth": np.arange(1, 101, step=1),
                        "min_samples_split": np.arange(2, len(self.X_train) + 1, step=1),
                        "min_samples_leaf": np.arange(1, len(self.X_train) // 2 + 1, step=1),
                        "min_weight_fraction_leaf": np.arange(0, 0.501, step=0.001),
                        # "max_features":np.arange(1,len(X_train[0])+1, step=1),
                        "max_features": np.arange(1, 18, step=1),
                        "max_leaf_nodes": np.arange(2, len(self.X_train) + 1, step=1),
                        "min_impurity_decrease": np.arange(0, 0.011, step=0.001),
                        "class_weight": ['balanced', None]
                    },
                "KNN":{
                    "n_neighbors": np.arange(1, 101, step=1),
                                   "weights": ["uniform", "distance", None],
                    "algorithm": ["auto", "ball_tree", "kd_tree", "brute"],
                    'leaf_size': np.arange(1, len(self.X_train) + 1, step=1),
                },
                "LASSO":{
                    "max_iter": np.arange(5, 1001, step=1),  # epochs
                    "tol": np.arange(0.00001, 0.01001, step=0.00005),
                    "C": np.arange(0, 100.001, step=0.005),
                    "class_weight": ['balanced', None],
                    'solver': ['liblinear', 'saga']
                },
                "LR":{
                    "max_iter": np.arange(5, 1001, step=1),  # epochs
                    "tol": np.arange(0.00001, 0.01001, step=0.00005),
                    "C": np.arange(0, 100.001, step=0.005),
                    "class_weight": ['balanced', None],
                    "map_penalty_solver": {
                        'none': ['lbfgs', 'newton-cg', 'sag', 'newton-cholesky', 'saga'],
                        'l1': ['liblinear', 'saga'],
                        'l2': ['liblinear', 'lbfgs', 'newton-cg', 'newton-cholesky', 'sag', 'saga'],
                        'elasticnet': ['saga']}
                },
                "RandomForest":{
                    "n_estimators": np.arange(1, 1001, step=1),
                    "criterion": ["gini", "entropy", "log_loss"],
                    "max_depth": np.arange(1, 101, step=1),
                    "min_samples_split": np.arange(2, len(self.X_train) + 1, step=1),
                    "min_samples_leaf": np.arange(1, len(self.X_train) // 2 + 1, step=1),
                    "min_weight_fraction_leaf": np.arange(0, 0.501, step=0.001),
                    # "max_features":np.arange(1,len(X_train[0])+1, step=1),
                    "max_features": np.arange(1, 18, step=1),
                    "max_leaf_nodes": np.arange(2, len(self.X_train) + 1, step=1),
                    "min_impurity_decrease": np.arange(0, 0.011, step=0.001),
                    "class_weight": ['balanced', None]
                },
                "SVM":{
                    "C": np.arange(0, 100.001, step=0.005),
                    "kernel": ["linear", "poly", "rbf", "sigmoid"],
                    "degree": np.arange(0, 6, step=1),
                    "gamma": ["scale", "auto"],
                    "shrinking": [True, False],
                    "tol": np.arange(0.00001, 0.01001, step=0.00005),
                    "class_weight": ['balanced', None],
                    "max_iter": np.arange(5, 1001, step=1),  # epochs
                },
                "XGBoost":{
                    "booster": ["gbtree", "gblinear", "dart"],
                    "eta": np.arange(0.001, 0.101, step=0.001),
                    "gamma": np.arange(0, 10.01, step=0.01),
                    "max_depth": np.arange(1, 101, step=1),
                    "subsample": np.arange(0.01, 1.01, step=0.01),
                    "sampling_method": ["uniform", "gradient_based"],
                    'alpha': np.arange(0, 100.0001, step=0.00001),
                    'lambda': np.arange(0, 100.0001, step=0.00001),
                    'tree_method': ['auto', 'exact', 'approx', 'hist'],
                    'objective': ['binary:logistic']
                }

            }
            self.hyperparameter_grid = hyperparameter_grids[method_name]
            return self.hyperparameter_grid
        except:
            print(f"sorry, we don't provide hyperparmaeter grids for the method - {method_name}, or the dataset object is wrong")

