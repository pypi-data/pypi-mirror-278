# RGSP

This package is designed to simplify the process of finding optimal hyperparameters for machine learning models using an enhanced grid search approach. It enables users to conveniently explore a wide range of hyperparameter combinations and identify the best settings for their models.

## Key Features

### 1. Dataset Handling (`Dataset.py`)
- Reads training and testing datasets from specified paths (`train_dataset_path` and `test_dataset_path`).
- Converts datasets into matrices suitable for model processing.

### 2. Hyperparameter Management (`hyperparameter.py`)
- Generates multiple hyperparameter settings based on a provided hyperparameter grid.
- Users can input hyperparameters in three ways:

  #### a. Direct List Input
  Provide hyperparameter settings as a list that can be directly used.
  ```python
  handle_hyperparameter = Hyperparameter(hyperparameter_settings)
  handle_hyperparameter.hyperparameter_settings
  ```

  #### b. Grid Input with Random Generation
  Provide a hyperparameter grid as a dictionary and specify the number of settings to generate randomly.
  ```python
  handle_hyperparameter = Hyperparameter(hyperparameter_grid)
  handle_hyperparameter.get_hyperparameter_settings(iter)
  handle_hyperparameter.hyperparameter_settings
  ```

  #### c. Default Grid
  Input only the method name to use the default hyperparameter grid for that method. Specify the number of settings to generate randomly. Requires the dataset object and method name.
  Method names we provided: AdaBoost, NaiveBayes, DecisionTree, KNN, LASSO, LR, RandomForest, SVC, XGBoost
  
  ```python
  handle_hyperparameter = Hyperparameter()
  handle_hyperparameter.get_hyperparameter_grid('AdaBoost', dataset)
  ```

### 3. Process Implementation (`Process.py`)
- Implements DFNN method and nine other machine learning methods:
  - AdaBoost
  - Categorical Naive Bayes
  - Decision Tree
  - KNN
  - Lasso
  - Logistic Regression
  - Random Forest
  - SVM
  - XGBoost
- Users can opt to test the model during training.
    ```python
    process = Process(dataset=dataset,
                      hyperparameter_settings=handle_hyperparameters.hyperparameter_settings,
                      method_name=method_name)
    process.train_with_test(result_path=result_path) #test the model during training
    process.train_without_test(result_path=result_path) #train all hyperparameter settings in one grid search, and do not test
    ```
- Results are stored in a tabular format for easy analysis.

## Installation

To install this package, run:
```bash
pip install RGS
```

## Usage

### Dataset Handling
```python
from RGS import Dataset

dataset = Dataset(train_dataset_path, test_dataset_path)
train_matrix = dataset.get_train_matrix()
test_matrix = dataset.get_test_matrix()
```

### Hyperparameter Management
#### Direct List Input
```python
from RGS import Hyperparameter

hyperparameter_settings = [...]
handle_hyperparameter = Hyperparameter(hyperparameter_settings)
print(handle_hyperparameter.hyperparameter_settings)
```

#### Grid Input with Random Generation
```python
hyperparameter_grid = {...}
handle_hyperparameter = Hyperparameter(hyperparameter_grid)
handle_hyperparameter.get_hyperparameter_settings(iter)
print(handle_hyperparameter.hyperparameter_settings)
```

#### Default Grid
```python
handle_hyperparameter = Hyperparameter()
dataset = Dataset(train_dataset_path, test_dataset_path)
handle_hyperparameter.get_hyperparameter_grid('AdaBoost', dataset)
```

### Process Implementation
```python
from RGS import Process

process = Process(method='AdaBoost', dataset=dataset, test=True)
process.train_with_test(result_path=result_path)
```

## Contributing

This project exists thanks to all the people who contribute.   
[Xia Jiang](https://github.com/XiaJiang-2)   
[Yijun Zhou](https://github.com/HakunaZoe) 

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

