"""
* Author: Asia Benyadilok

* Created: 30/03/2021

* Revised: 09/05/2021

* Description:  Web Application

* User advice: None
"""

#import the libraries
from datetime import date
import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_datareader as web
from PIL import Image
from plotly import graph_objects as go
import pickle
from DataCollectingModule import * #import all function from Data Collecting Module
from SentimentAnalysisModule import * #import all function from Sentiment Analysis Module
from TechnicalAnalysisModule import * #import all function from Technical Analysis Module
from ClassifierModel import * #import all function from Classifier Model

#get current date
today = date.today().strftime("%Y-%m-%d")

#Add a title and an image
st.write("""
 # Stock market Web Application    
Visually show data on a stock and trend prediction! 
""")

#import image from local machine
image = Image.open("C:/Users/basas/Desktop/download.jpg")
st.image(image, use_column_width=True)

#create a sidebar header
st.sidebar.header('User Input')
st.sidebar.write('Please input the period and stock symbol below')


#* Function:  get_input

#* Description: method for getting input from user

#* Parameters: none

#* Returns: start_date, end_date, stock_symbol

#* Warnings: none

def get_input():
  #set initial input
  start_date = st.sidebar.text_input("Start Date","2020-01-02")
  end_date = st.sidebar.text_input("End Date", "2020-08-04")
  stock_symbol = st.sidebar.selectbox("Stock Symbol", ['AAPL','AMZN','GOOG','FB','TSLA'])
  return start_date, end_date, stock_symbol


#* Function:  get_company_name

#* Description: method for getting the real company name

#* Parameters: symbol

#* Returns: cn.info['shortName']

#* Warnings: none

def get_company_name(symbol):

  cn = yf.Ticker(symbol.upper())

  if cn.info['shortName'] != '':
    return cn.info['shortName']

  else:
    return 'none'

#* Function:  plot_data

#* Description: method for plotting graph

#* Parameters: date,column,name,title

#* Returns: none

#* Warnings: none
#plot the graph
def plot_data(date,column,name,title):
  fig = go.Figure()
  fig.add_trace(go.Scatter(x=date,y=column,name=name))
  fig.layout.update(title_text = title,xaxis_rangeslider_visible=True)
  st.plotly_chart(fig)

# Get the initial users input
start, end, symbol = get_input()

#validate the user input
try:

  #call Yahoo api to retrieve historical prices
  df = web.DataReader(symbol, data_source='yahoo', start = start, end = end)

  #Get the Company name
  company_name = get_company_name(symbol.upper())

  #display overview data from yahoo
  st.header(company_name+" (Overview)\n")
  df_with_tech = caltechIndicators(df)
  df_with_tech = df.replace({np.nan: '-'})
  df_with_tech = df_with_tech.replace({0: '-'})

  #converting time stamp to date
  date = []
  for i in df_with_tech.index:
    date.append(pd.to_datetime(i).date())

  df_with_tech.index = date

  #display raw data
  st.write(df_with_tech)


  #Allow user to choose what graph to be displayed
  graph = st.selectbox("Graph to be shown", ['Close','Adj Close','Open','High','Low','Volume','RSI','MACD','K_percent','R_percent','Price_Rate_Change','On_Balance_Volume'])
  st.header(company_name+' ('+graph+')')

  #Display the details of the stock
  st.line_chart(df[graph])

  #Get statistics on the data
  st.header(company_name+' (Data Statistics)')
  st.write(df.describe())

  #display the prediction section only for AAPL
  if symbol == 'AAPL':
    print('yes')

    #get lastest trade day from yahoo
    current_df = web.DataReader(symbol, data_source='yahoo', start = '2021-01-01', end = today)
    latest_date = current_df.index[-1]
    current_date = pd.to_datetime(latest_date).date()

    #show current date
    st.header('Prediction section')
    st.write('Current Prediction Date: '+str(current_date))
    print(current_date)
    #make prediction
    #retrieve data from Data Collecting Module
    news = getCompanyNews(str(current_date),"AAPL")

    #preprocess the news article
    news = newsPrePro(news)

    #collect the historical price
    price = getCompanyHisPrices(str(current_date),"AAPL")

    #calculate sentiment score
    news = calSentScore(news)

    #calculate technical indicators
    price = caltechIndicators(price)

    #extract features
    feature = preProData(news,price)

    #make prediction
    pred = predict(feature)
    print(pred)
    #prediction conditions
    if pred == 1:
      df_pred = [['Rise','Sell']]
    elif pred == 0:
      df_pred = [['Fall','Buy']]

    #display prediction
    df_pred = pd.DataFrame(df_pred, columns = ['Trend Prediction','Decision suggest'])
    st.header('Prediction Description\n ')
    st.write('Future trend prediction after the current prediction date')
    st.write(df_pred)

    #plot close price for prediction
    plot_data(current_df.index,current_df['Close'],'stock_close','Close Price from 2021-01-01 to '+ str(current_date))
    st.write('note: the prediction section currently only available for AAPL stock')

except:
  #display an error message
  st.header('An Error occur! - please check the start and end date input')
