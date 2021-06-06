"""
* Author: Asia Benyadilok

* Created: 30/03/2021

* Revised: 09/05/2021

* Description: Data Collecting Module

* User advice: None
"""

#libraries
import pandas as pd
import numpy as np
import re
from datetime import datetime
import pandas_datareader as web
import finnhub #library for fetch financial data


#initialize finnhub API with API key
finnhub_client = finnhub.Client(api_key="c1a93gv48v6q8l0k8ur0")

"""
* Function:  getCompanyNews

* Description: method for retrieving news articles from finnhub API   

* Parameters: date and ticker

* Returns: dataF - news dataframe

* Warnings: none
"""
# free version of finnhub limit up to only month month per request and maximum of 1 year past data
def getCompanyNews(date,ticker):

    data = finnhub_client.company_news(ticker, _from= date, to= date)

    #convert data from finnhub to dataframe
    dataF = pd.DataFrame(data)

    #sort rows by date and time
    dataF = dataF.sort_values(by="datetime")

    #date list
    dateList = []
    current_date = date
    #convert timestamp to readable date
    for j in dataF['datetime']:
        date = datetime.fromtimestamp(j)
        date = str(date).split(sep=' ', maxsplit=2)
        dateList.append(date[0])

    #insert string date column
    dataF.insert(0, "Date", dateList, True)


    #remove rows that does not have summary
    dataF = dataF.drop(dataF[dataF["summary"].map(len) < 10].index)

    #remove rows that have an incorrect date
    dataF = dataF.drop(dataF[dataF["Date"] != current_date].index)

    #remove duplicate rows that have the same headline
    dataF.drop_duplicates(subset ="headline",
                         keep = 'first', inplace = True)


    #reset index
    dataF = dataF.reset_index(drop=True)

    #return news articles dataframe
    return dataF


"""
* Function:  getCompanyHisPrices

* Description: method for retrieving historical price from Yahoo API   

* Parameters: date and ticker

* Returns: dataF - historical prices dataframe

* Warnings: none
"""
def getCompanyHisPrices(date,ticker):

    # getting historical prices data  from yahoo api
    data = web.DataReader(ticker, data_source='yahoo', start="2021-01-01", end= date)

    #convert data to dataframe
    dataF = pd.DataFrame(data)

    #return historical prices dataframe
    return dataF


"""
* Function:  newsPrePro

* Description: method for pre-processing the news articles 

* Parameters: newsArt

* Returns: newsArt - pre-processed news articles

* Warnings: none
"""
def newsPrePro(newsArt):

    # remove unwanted columns
    del newsArt['id']
    del newsArt['image']
    del newsArt['related']
    del newsArt['source']
    del newsArt['url']
    del newsArt['category']
    del newsArt['datetime']
    del newsArt['summary']

    # convert headline and summary to lower case
    newsArt["headline"] = newsArt["headline"].str.lower()

    # remove special character and non-english words from headline and summary of news
    newsArt["headline"] = newsArt["headline"].str.replace(r"[^-_,A-Za-z0-9]+", " ").str.strip()

    # remove duplicate rows that have the same headline
    newsArt.drop_duplicates(subset="headline",
                            keep='first', inplace=True)

    #filter relevant news if the number of news is enough
    if (len(newsArt.index) > 100):

        #filter news headlines by using key words
        newsArt = newsArt[newsArt["headline"].str.contains("apple", case=False, na=False) |
                          newsArt["headline"].str.contains("aapl", case=False, na=False) |
                          newsArt["headline"].str.contains("stock", case=False, na=False)]

    # combine headline by date
    newsArt = newsArt.groupby(["Date"], axis=0, as_index=False).agg({"headline": ', '.join})

    # reset index
    newsArt = newsArt.reset_index(drop=True)

    #return pre-processed news articles
    return newsArt
