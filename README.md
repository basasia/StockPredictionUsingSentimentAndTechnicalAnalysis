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

The design of this application followed the basic pattern of regular application such that it has interface with clearly intructions on how to use, every buttons has it own label describes what is it and the application has an error handling functionality that display an pop-up error messages when the user raised some errors. 




##Run Locally

- Clone the folder UWEAccommodationSystem
- Make sure to install Netbeans
- Run the jar file \UWEAccommodationSystem\dist\UWEAccommodationSystem.jar
- You can login with username: warden, hallmanager or admin. Password: pass
- Optionally, the application can be run by using Netbeans then run the file \UWEAccommodationSystem\src\uweaccommodationsystem\guicontrollers\GUIRoot  

##Tech Stack

- Netbeans
- JAVA 
- SceneBuilder
