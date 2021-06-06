"""
* Author: Asia Benyadilok

* Created: 30/03/2021

* Revised: 09/05/2021

* Description: Technical Analysis Module

* User advice: None
"""

#libraries
import pandas as pd
import numpy as np
from DataCollectingModule import * #import all function from Data Collecting Module

"""
* Function:  calRSI

* Description: method for calculating RSI

* Parameters: hisPrices

* Returns: hisPrices - historical prices with RSI

* Warnings: none
"""
def calRSI(hisPrices):

    #convert to dataframe
    hisPrices = pd.DataFrame(hisPrices)

    #Get the difference in price from the previous day
    delta = hisPrices['Adj Close'].diff(1)

    #Get rid of NaN
    delta = delta.dropna()

    #Get the positive gains (up) and the negative gains(down)
    up = delta.copy()
    down = delta.copy()

    up[up < 0] = 0
    down[down > 0] = 0

    #Get the time period
    period = 14

    #Calculate the average gain and average loss
    AVG_Gain = up.rolling(window=period).mean()
    AVG_Loss = abs(down.rolling(window=period).mean())

    #Calculate the Relative Strength (RSI)
    RS = AVG_Gain / AVG_Loss

    #Calculate the Relative Strength Index (RSI)
    RSI = 100.0 - (100.0 / (1.0 + RS))

    # set results back  to main dataframe
    hisPrices['RSI'] = RSI

    return hisPrices


"""
* Function:  calMACD

* Description: method for calculating MACD

* Parameters: hisPrices

* Returns: hisPrices - historical prices with MACD

* Warnings: none
"""
def calMACD(hisPrices):

    #convert to dataframe
    hisPrices = pd.DataFrame(hisPrices)

    #Calculate the MACD and signal line indicators
    #Calculate the short term exponential moving average (EMA)
    shortEMA = hisPrices.Close.ewm(span=12,adjust=False).mean()

    #Calculate the long term exponential moving average (EMA)
    longEMA = hisPrices.Close.ewm(span=26,adjust=False).mean()

    #Calculate the MACD line
    MACD = shortEMA - longEMA

    #calculate the signal line
    signal = MACD.ewm(span=9, adjust=False).mean()

    #set results back  to main dataframe
    hisPrices['MACD'] = MACD
    hisPrices['Signal Line'] = signal

    return hisPrices


"""
* Function:  calSO

* Description: method for calculating stochastic oscillator 

* Parameters: hisPrices

* Returns: hisPrices - historical prices with stochastic oscillator

* Warnings: none
"""
def calSO(hisPrices):

    # convert to dataframe
    hisPrices = pd.DataFrame(hisPrices)

    # calculate the stochastic oscillator
    #define period for calculation
    n=14

    low_14 = hisPrices['Low'].copy()
    high_14 = hisPrices['High'].copy()

    low_14 = low_14.transform(lambda x: x.rolling(window = n).min())
    high_14 = high_14.transform(lambda x: x.rolling(window = n).max())

    #calculate the stochastic oscillator
    k_percent = 100 * ((hisPrices['Close'] - low_14) / (high_14 - low_14))

    # add the info to the data frame
    hisPrices['K_percent'] = k_percent

    return hisPrices


"""
* Function:  calWilLR

* Description: method for calculating William percent R

* Parameters: hisPrices

* Returns: hisPrices - historical prices with William percent R

* Warnings: none
"""
def calWilLR(hisPrices):

    #convert to dataframe
    hisPrices = pd.DataFrame(hisPrices)

    #define period for calculation
    n = 14

    #calculate high low
    low_14 = hisPrices['Low'].copy()
    high_14 = hisPrices['High'].copy()

    low_14 = low_14.transform(lambda x: x.rolling(window = n).min())
    high_14 = high_14.transform(lambda x: x.rolling(window = n).max())

    #calculate william %R
    r_percent = ((high_14 - hisPrices['Close']) / (high_14 - low_14)) * -100

    # add the info to the data frame
    hisPrices['R_percent'] = r_percent

    return hisPrices


"""
* Function:  calPRC

* Description: method for calculating Price Rate Change

* Parameters: hisPrices

* Returns: hisPrices - historical prices with Price Rate Change

* Warnings: none
"""
def calPRC(hisPrices):

    #convert to dataframe
    hisPrices = pd.DataFrame(hisPrices)

    # calculate price rate change
    hisPrices['Price_Rate_Change'] = hisPrices['Close'].transform(lambda x: x.pct_change(periods = 9))

    return hisPrices


"""
* Function:  calOBV

* Description: method for calculating On Balance Volume

* Parameters: hisPrices

* Returns: hisPrices - historical prices with On Balance Volume

* Warnings: none
"""
def calOBV(hisPrices):

    #convert to dataframe
    hisPrices = pd.DataFrame(hisPrices)

    #calculate on balance volume
    volume = hisPrices['Volume'].copy()
    change = hisPrices['Close'].diff().copy()

    prev_obv = 0
    obv_values = []

    for i,j in zip(change,volume):

        if i > 0:
            current_obv = prev_obv + j
        elif i < 0:
            current_obv = prev_obv - j
        else:
            current_obv = prev_obv

        prev_obv = current_obv
        obv_values.append(current_obv)

    obv_values = pd.Series(obv_values, index = hisPrices.index)

    #add it to the data frame
    hisPrices['On_Balance_Volume'] = obv_values

    return hisPrices


"""
* Function:  caltechIndicators

* Description: method for calculating all the technical indicators

* Parameters: hisPrices

* Returns: hisPrices - historical prices with all of the technical indicators computed on it

* Warnings: none
"""
def caltechIndicators(hisPrices):

    #calculate all technical indicators
    hisPrices = calRSI(hisPrices)
    hisPrices = calMACD(hisPrices)
    hisPrices = calSO(hisPrices)
    hisPrices = calWilLR(hisPrices)
    hisPrices = calPRC(hisPrices)
    hisPrices = calOBV(hisPrices)

    return hisPrices
