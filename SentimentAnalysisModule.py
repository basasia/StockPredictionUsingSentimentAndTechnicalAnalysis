"""
* Author: Asia Benyadilok

* Created: 30/03/2021

* Revised: 09/05/2021

* Description: Sentiment Analysis Module

* User advice: None
"""

#libraries
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer #library for sentiment analysis model
from DataCollectingModule import * #import all function from Data Collecting Module

#initialize the vader model
sentModel = SentimentIntensityAnalyzer()

"""
* Function:  calSentScore

* Description: method for calculating the sentiment scores   

* Parameters: newsHeadlines

* Returns: newsHeadlines - newsHeadlines with the sentiment scores

* Warnings: none
"""
def calSentScore(newsHeadlines):

    #initializ lists for collecting the sentiment score
    compound = []
    positive = []
    negative = []
    neutral = []
    senlist = []

    #convert newsHeadlines to dataframe
    newsHeadlines = pd.DataFrame(newsHeadlines)

    #convert each headline to sentiment scores
    for news in newsHeadlines["headline"]:

        #using vader for calculating sentiment score
        sentence_sentiment = sentModel.polarity_scores(news)
        compound.append(sentence_sentiment['compound'])
        positive.append(sentence_sentiment['pos'])
        negative.append(sentence_sentiment['neg'])
        neutral.append(sentence_sentiment['neu'])

    #classify sentiment polarity into three classes(positive, neutral and negative)(1,0,-1)
    for i in compound:

        if i >= 0.05:

            senlist.append(1)

        elif -0.05 < i < 0.05:

            senlist.append(0)

        else:
            senlist.append(-1)

    # add new column to the existing dataframe
    newsHeadlines["sent"] = senlist
    newsHeadlines["pos"] = positive
    newsHeadlines["neg"] = negative
    newsHeadlines["neu"] = neutral

    #return newsHeadlines with the sentiment scores
    return newsHeadlines
