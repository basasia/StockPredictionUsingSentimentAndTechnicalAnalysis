"""
* Author: Asia Benyadilok

* Created: 01/04/2021

* Revised: 09/05/2021

* Description: Random Forest

* User advice: None
"""

#import libraries
import os
import sys
import requests

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import plot_roc_curve
from sklearn.metrics import accuracy_score, classification_report

from sklearn.preprocessing import MinMaxScaler
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from tscv import GapWalkForward
import pickle
import joblib

#import dataset from local machine
mainData = pd.read_csv("C:/Users/basas/Desktop/AAPL stock news/AAPL_training_set.csv",index_col=[0])

#drop Nan from the list
mainData = mainData[mainData['Prediction'].notna()]

#define columns
x_cols = mainData[['Close','sent','pos','neg','neu','RSI','MACD','K_percent','R_percent','Price_Rate_Change','On_Balance_Volume']]
y_cols = mainData['Prediction']

#using min max to convert the input to range [0,1]
to_scale = [col for col in x_cols.columns if x_cols[col].max() > 1 or x_cols[col].min() < 0]
mms = MinMaxScaler()
scaled = mms.fit_transform(x_cols[to_scale])
scaled = pd.DataFrame(scaled, columns=to_scale)

# Replace original columns with scaled ones
for col in scaled:
    x_cols[col] = scaled[col]

#transfromdataset
oversample = SMOTE()
x_cols, y_cols = oversample.fit_resample(x_cols, y_cols)

#train and test split
x_train, x_test, y_train, y_test = train_test_split(x_cols, y_cols,  random_state=42, test_size = 0.2,stratify = y_cols)

#define model parameters
rf_model = RandomForestClassifier(n_estimators = 500, criterion = 'gini', random_state = 42,max_depth=8,max_features='auto')

#fit the data to the model
rf_model.fit(x_train, y_train)

# make predictions
y_pred = rf_model.predict(x_test)

#print accuracy_score
print('Correct prediction (%):', accuracy_score(y_test, y_pred, normalize = True) * 100.0)

#print report
target_names = ['Downward', 'Upward']

#build a classifier report
report = classification_report(y_true = y_test, y_pred = y_pred, target_names = target_names, output_dict =True)

# add it to a data frame, transpose it for readability.
report_df = pd.DataFrame(report).transpose()
print(report_df)

#10 fold cross validation
score = cross_val_score(rf_model, x_train, y_train, cv = 10, scoring = "accuracy")
print(score)
print(sum(score)/len(score))


'''
#fine tune the model
# Number of trees in random forest
# Number of trees is not a parameter that should be tuned, but just set large enough usually. There is no risk of overfitting in random forest with growing number of # trees, as they are trained independently from each other.
n_estimators = list(range(1,100))

# Number of features to consider at every split
max_features = ['auto', 'sqrt', None, 'log2']

# Maximum number of levels in tree
# Max depth is a parameter that most of the times should be set as high as possible, but possibly better performance can be achieved by setting it lower.
max_depth = list(range(10,100))
max_depth.append(None)

# Minimum number of samples required to split a node
# Higher values prevent a model from learning relations which might be highly specific to the particular sample selected for a tree. Too high values can also lead to # under-fitting hence depending on the level of underfitting or overfitting, you can tune the values for min_samples_split.
min_samples_split = [2, 5, 10, 20, 30, 40]

# Minimum number of samples required at each leaf node
min_samples_leaf = [1, 2, 7, 12, 14, 16 ,20]

# Method of selecting samples for training each tree
bootstrap = [True, False]

# Create the random grid
random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}
#grid model
rf_model = RandomForestClassifier(random_state=42)
grid = GridSearchCV(estimator = rf_model, param_grid = random_grid, cv = 10,verbose=2)

grid.fit(x_train, y_train)
print("*********",grid.best_params_)
print("*********",grid.best_estimator_)
'''