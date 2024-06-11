import os
import pandas as pd

class Dataset:
    def __init__(self, train_dataset_path, test_dataset_path):
        self.X_train, self.Y_train = self.loadandprocess(train_dataset_path, predtype=1, scaled=False)
        self.X_test, self.Y_test = self.loadandprocess(test_dataset_path, predtype=1, scaled=False)
    def loadandprocess(self, file, sep='\t', predtype=1, scaled=True):
        """
        this function is used to divide the original data into train features(predictors) X and labels Y
        For trainset X:
            if we set scaled = True, then all the train features will be normalized(scale to [0,1]);
            if we set predtype = 1, it means the last column features is target, others are predictors
            if we set predtype = 2, it means the first column is index(we could ignore) and the last column features
            is target, others are predictors
        """
        file_type = os.path.splitext(file)[1]
        if file_type == ".csv":
            df = pd.read_csv(file)
        else:
            df = pd.read_csv(file, sep, lineterminator='\n')
        # cols=[0,532]
        # predset = df.drop(df.columns[cols],axis=1)
        if predtype == 1:
            X = df.iloc[:, :-1]  # all columns except for the last one are predictors
        elif predtype == 2:
            X = df.iloc[:, 1:-1]  # all columns except for the first and last ones are predictors
        # If scaled is true, Normalized to [0,1]. Default is true.
        if scaled:
            scaler = MinMaxScaler()
            scaler.fit(predset)
            X = scaler.transform(X)

        print(f'pred shape: {X.shape}')
        print(f'pred dimension: {X.ndim}')
        # tarcol2 = n.array(df.columns[-1])
        Y = df.iloc[:, -1]
        print(Y.head(4))
        print(f'target frame dimension: {Y.ndim}')
        print(f'target frame shape: {Y.shape}')
        Y = Y.to_numpy()
        print(f'target dimension: {Y.ndim}')
        X = X.to_numpy()
        # if have a problem"numpy.ndarray' object has no attribute 'to_numpy" when scale = True,
        # you can just comment"predset = predset.to_numpy()" because predset = scaler.transform(predset) will return numpy object directly
        # which we want to make a prediction
        return X,Y
