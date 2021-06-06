"""
* Author: Asia Benyadilok

* Created: 01/04/2021

* Revised: 09/05/2021

* Description: Support Vector Machine

* User advice: None
"""

#libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score, classification_report

from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.preprocessing import MinMaxScaler
from imblearn.over_sampling import SMOTE

from sklearn.model_selection import cross_val_score
from tscv import GapWalkForward
import joblib
from sklearn import *

import pickle
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score


#define model parameters
svm_model = svm.SVC(kernel = 'sigmoid', gamma=0.1, C=100)

#import dataset from local machine
mainData = pd.read_csv("C:/Users/basas/Desktop/AAPL stock news/AAPL_training_set.csv",index_col=[0])
#drop nan
mainData = mainData[mainData['Prediction'].notna()]

#reset index
mainData = mainData.reset_index()

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

#transfrom dataset to balance the class
oversample = SMOTE()
x_cols, y_cols = oversample.fit_resample(x_cols, y_cols)

#train and test split
x_train, x_test, y_train, y_test = train_test_split(x_cols, y_cols, random_state = 42, test_size = 0.2,stratify = y_cols)

#fit the model
svm_model.fit(x_train,y_train)

#make prediction
y_pred = svm_model.predict(x_test)

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
score = cross_val_score(svm_model, x_train, y_train, cv = 10, scoring = 'accuracy')
print(score)
print(sum(score)/len(score))

'''
#fine tune the model
#svm_model = svm.SVC()
cv = GapWalkForward(n_splits=10, gap_size=1, test_size=2)
param_grid = {'C': [0.1,1, 10, 100], 'gamma': [1,0.1,0.01,0.001],'kernel': ['rbf', 'sigmoid','linear']}
grid = GridSearchCV(SVC(),param_grid,refit=True,verbose=2,cv = 10)
grid.fit(x_train,y_train)
print("*********",grid.best_params_)
print("*********",grid.best_estimator_)

'''