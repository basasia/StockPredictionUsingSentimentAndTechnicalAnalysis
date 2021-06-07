# StockPredictionUsingSentimentAndTechnicalAnalysis
Web application for stock prediction develop by using Python

###Stock prediction app using sentiment and technical analysis

##Task

Build an web application that allows the users to view stock details, view stock prediction, choose stock symbol and a period to be viewed.

##Summary 

This project is about predicting the trend of the stock market based on the sentiment analysis combining with the stock technical indicators which are RSI, MACD and more. The main idea is to getting information of people comments toward the target stock from available sources then perform the sentiment analysis to determine that if it is positive, negative or neutral. Once the sentiment is analysed, it will then be combining with the results of RSI, MACD and more of the target stock which will make it more efficient in term of consistency as the comments from people are various depends on their perspective, but with the technical indicators that use mathematical methods to calculate will give more accurate results. Once those three results are combined, it will be passed to the classifier model to predict whether the trend is going up or down.

##Functionality

This web application fetches the news articles from finnhub API and retrieves the historical prices based on the selected stock by the users. It then pre-processes the new articles and calculates the sentiment on each headlines to determine whether it is negative, positive or neutral. After that, it computes the technical indicators based on the historical prices retrieved. Once both results from sentiment and technical analysis are obtained, it will be passed on to the classifier model that were trained to predict the stock trends using this results as the features input. Lastly, the result of the prediction are then displayed on the web application.   

##Design

For the system:

![image](https://user-images.githubusercontent.com/60352487/120921896-55457c80-c6f0-11eb-8ce9-13164fbf58b3.png)

For the interface:

The design of this application followed the basic pattern of regular application such that it has interface with clearly intructions on how to use, every buttons has it own label describes what is it and the application has an error handling functionality that display an pop-up error messages when the user raised some errors. 


##Run Locally

- Clone the folder StockPredictionUsingSentimentAndTechnicalAnalysis
- Make sure to install Python 
- Change the file path in \StockPredictionUsingSentimentAndTechnicalAnalysis\ClassifierModel.py to where you store the model

 ![image](https://user-images.githubusercontent.com/60352487/120923534-41524880-c6f9-11eb-9c98-0ad4adb4958e.png)
 
- Optionally, you can change the classifier model to evaluate the performance. There are two trained classifier models available which are Random Forest (RF) and Support Vector Machine (SVM). They are located in \StockPredictionUsingSentimentAndTechnicalAnalysis\Trained models  
- Open the command prompt and use command "streamlit run C:/StockPredictionUsingSentimentAndTechnicalAnalysis/TradingWebApp.py" to run the web application.


##Tech Stack

- Python
- Web browser

Libraries required: 

- datetime 
- streamlit 
- yfinance 
- pandas 
- pandas_datareader 
- PIL 
- plotly 
- pickle
- nltk.sentiment.vader


User-interface:

![image](https://user-images.githubusercontent.com/60352487/120924395-cdff0580-c6fd-11eb-8905-72b58b4b8351.png)

![image](https://user-images.githubusercontent.com/60352487/120924646-c7bd5900-c6fe-11eb-98e3-c4cb2eb4db37.png)

![image](https://user-images.githubusercontent.com/60352487/120924671-f0dde980-c6fe-11eb-8919-427a09232174.png)

![image](https://user-images.githubusercontent.com/60352487/120924681-fdfad880-c6fe-11eb-93c3-004abd4240a0.png)

note: the prediction section only available for AAPL stock as all the models have been trained only on the apple stock. Feel free to modify or extend this project for further study.



