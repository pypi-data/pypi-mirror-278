from sklearn.tree import DecisionTreeClassifier
from datetime import datetime
import cpuinformation
from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from keras.wrappers.scikit_learn import KerasClassifier
from keras.layers import Dense
from keras.layers import Dropout
from keras.models import Sequential
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import roc_curve, auc
from sklearn.ensemble import AdaBoostClassifier
from store_result import write_table
from sklearn.naive_bayes import CategoricalNB
from keras import regularizers
import keras.optimizers as opt

class Process:
    def __init__(self,  dataset, hyperparameter_settings, method_name="",):
        self.method_name = method_name
        self.X_train, self.Y_train, self.X_test, self.Y_test = dataset.X_train, dataset.Y_train, dataset.X_test, dataset.Y_test
        self.hyperparameter_settings = hyperparameter_settings

    def train_without_test(self, nsplits=5, scores={'AUC': 'roc_auc', 'f1': 'f1'}, seed=123, result_path =''):
        print("*************begin to train****************")
        start_time = datetime.now()
        cur_cv = StratifiedKFold(n_splits=nsplits, shuffle=True, random_state=seed)
        if self.method_name == "DecisionTree":
            clf = DecisionTreeClassifier()
        elif self.method_name == "AdaBoost":
            clf = AdaBoostClassifier()
        elif self.method_name == "NaiveBayes":
            clf = CategoricalNB()
        elif self.method_name == "DecisionTree":
            clf = DecisionTreeClassifier()
        elif self.method_name == "KNN":
            clf = KNeighborsClassifier()
        elif self.method_name == "LASSO":
            clf = LogisticRegression(penalty='l1')
        elif self.method_name == "LR":
            clf = LogisticRegression()
        elif self.method_name == "RandomForest":
            clf = RandomForestClassifier()
        elif self.method_name == "SVC":
            clf = SVC(probability=True)
        elif self.method_name == "XGBoost":
            clf = XGBClassifier()
        elif self.method_name == "DFNN":
            clf = KerasClassifier(build_fn=self.create_model)
        g_search = GridSearchCV(clf, param_grid=self.hyperparameter_settings, cv=cur_cv, refit='AUC',
                                scoring=scores, return_train_score=True, n_jobs=-1)
        gs = g_search.fit(X=self.X_train, y= self.Y_train)
        end_time = datetime.now()
        print("*************train successfully****************")
        if len(result_path) != '':
            print("*************begin to store result in table****************")
            write_table(
                    tablename=result_path,
                    grid_result=gs,
                    start_time=start_time,
                    end_time=end_time,
                    seed=seed,
                    cpu_state=cpuinformation.record_cpu_information(),
                    ml_classifier_name=self.method_name,
                    experiment_iden="",
                    table="",
            )
            print("*************successfully store in table****************")
        return gs

    def train_with_test(self, nsplits=5, scores={'AUC': 'roc_auc', 'f1': 'f1'}, seed=123, result_path =''):
        print("*************begin to train and write****************")
        cur_cv = StratifiedKFold(n_splits=nsplits, shuffle=True, random_state=seed)
        for index in range(len(self.hyperparameter_settings)):
            start_time = datetime.now()

            if self.method_name == "DecisionTree":
                clf = DecisionTreeClassifier()
            elif self.method_name == "AdaBoost":
                clf = AdaBoostClassifier()
            elif self.method_name == "NaiveBayes":
                clf = CategoricalNB()
            elif self.method_name == "DecisionTree":
                clf = DecisionTreeClassifier()
            elif self.method_name == "KNN":
                clf = KNeighborsClassifier()
            elif self.method_name == "LASSO":
                clf = LogisticRegression(penalty='l1')
            elif self.method_name == "LR":
                clf = LogisticRegression()
            elif self.method_name == "RandomForest":
                clf = RandomForestClassifier()
            elif self.method_name == "SVC":
                clf = SVC(probability=True)
            elif self.method_name == "XGBoost":
                clf = XGBClassifier()
            # elif self.method_name == "DFNN":
            #     clf = KerasClassifier(build_fn=self.create_model)
            g_search = GridSearchCV(clf, param_grid=self.hyperparameter_settings[index], cv=cur_cv, refit='AUC',
                                scoring=scores, return_train_score=True, n_jobs=-1)
            gs = g_search.fit(X=self.X_train, y= self.Y_train)
            test_auc = self.test(gs)
            end_time = datetime.now()
            if len(result_path) != '':
                write_table(
                        tablename=result_path,
                        grid_result=gs,
                        start_time=start_time,
                        end_time=end_time,
                        seed=seed,
                        cpu_state=cpuinformation.record_cpu_information(),
                        ml_classifier_name=self.method_name,
                        experiment_iden="",
                        table="",
                        test_auc = test_auc
                )
        print("*************successfully store all in table****************")



    def test(self,gs):
        pred_grid = gs.predict_proba(self.X_test)[:, 1]
        pred_grid = pred_grid.reshape(-1)
        FP, TP, thresholds = roc_curve(self.Y_test.astype(float), pred_grid.astype(float))
        test_auc_grid = auc(FP, TP)
        return test_auc_grid

    def create_model(self, mstruct, idim, drate, kinit, iacti, hacti, oacti, opti, lrate, momen, dec, ls, L1, L2,
                     ltype):
        # create a model that KerasClassifier needs as an input for parameter build_fn
        model = Sequential()
        if ltype == 0:
            model.add(Dense(mstruct[0], input_dim=idim, kernel_initializer=kinit, activation=iacti))
        elif ltype == 1:
            model.add(Dense(mstruct[0], input_dim=idim, kernel_initializer=kinit, activation=iacti,
                            kernel_regularizer=regularizers.l1(L1)))
        elif ltype == 2:
            model.add(Dense(mstruct[0], input_dim=idim, kernel_initializer=kinit, activation=iacti,
                            kernel_regularizer=regularizers.l2(L2)))
        elif ltype == 3:
            model.add(Dense(mstruct[0], input_dim=idim, kernel_initializer=kinit, activation=iacti,
                            kernel_regularizer=regularizers.l1_l2(l1=L1, l2=L2)))

        model.add(Dropout(drate))
        nlayers = len(mstruct)
        nhiddenlayers = nlayers - 2
        for i in range(nhiddenlayers):
            model.add(Dense(mstruct[i + 1], activation=hacti))
            model.add(Dropout(drate))
        model.add(Dense(mstruct[nlayers - 1], activation=oacti))
        # Using 'softmax' as the activation function for the output layer will return all 0.5s when class is binary

        for layer in model.layers:
            print(layer.weights)
        cur_opt = opti
        if opti == 'Adagrad':
            cur_opt = opt.Adagrad(lr=lrate, decay=dec)
        elif opti == 'SGD':
            cur_opt = opt.SGD(lr=lrate, momentum=momen, decay=dec)
        elif opti == 'adam':
            cur_opt = opt.Adam(lr=lrate, decay=dec)
        elif opti == 'Nadam':
            cur_opt = opt.Nadam(lr=lrate, decay=dec)
        elif opti == 'Adamax':
            cur_opt = opt.Adamax(lr=lrate, decay=dec)
        model.compile(optimizer=cur_opt, loss=ls, metrics="accuracy")
        return model





