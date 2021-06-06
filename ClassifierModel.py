"""
* Author: Asia Benyadilok

* Created: 30/03/2021

* Revised: 09/05/2021

* Description: Classifier Models

* User advice: None
"""

#libraries
import numpy as np
import pandas as pd
import pickle
import joblib
from DataCollectingModule import * #import all function from Data Collecting Module
from SentimentAnalysisModule import * #import all function from Sentiment Analysis Module
from TechnicalAnalysisModule import * #import all function from Technical Analysis Module

"""
* Function:  preProData

* Description: method for pre-processing data for the classifier models 

* Parameters: newsHeadlines and hisPrices

* Returns: features - features for the classifier models

* Warnings: none
"""
def preProData(newsHeadlines,hisPrices):

    #convert news headlines and historical prices to dataframe
    hisPrices = pd.DataFrame(hisPrices)
    newsHeadlines = pd.DataFrame(newsHeadlines)

    #convert date on the newsheadline to date object
    newsHeadlines['Date'] = pd.to_datetime(newsHeadlines['Date'])

    # merge news dataframe and financial dataframe together
    mergeData = newsHeadlines.merge(hisPrices, how='inner', on='Date', left_index=True)

    # reset index
    mergeData = mergeData.reset_index(drop=True)

    # remove unwanted columns
    del mergeData['headline']

    #extract features
    features = mergeData[['Close', 'sent', 'pos', 'neg', 'neu', 'RSI', 'MACD', 'K_percent', 'R_percent', 'Price_Rate_Change','On_Balance_Volume']]

    return features

"""
* Function:  predict

* Description: method for predicting the stock trend 

* Parameters: features

* Returns: pred - prediction output

* Warnings: none
"""
def predict(features):

    # load trained model from local machine
    # edit this file path to where you saved the model
    with open('C:/svm_trained_model', 'rb') as f:
        svm_model = pickle.load(f)

    #use the trained model to predict
    pred = svm_model.predict(features)

    #return prediction
    return pred[0]

