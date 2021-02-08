![alt text](https://imgur.com/OdgqpZL.jpg)

Ensemble model that utilizes news headlines and S&P 500 (SPX) stock data to predict closing prices.

## Summary

With deep learning, I learned my way up on understanding by how well time series data can be used to somehow predict closing stock price. I chose to add news headlines to the mix as a determining factor whether or not the price is more likely to go up or down through sentiment analysis.

## Rationale

Admittedly, its naivete is a rather welcome factor to properly assess the data more considering that the news headlines data can be a lot more pronounced. SPX data can be somewhat overwhelmed purely by itself, so I initially thought of adding in news headlines that would assist ARIMA modeling.

## Process

After 'graduating' from using my 3DMark data, I made a new scraper that would collect news data from 4 sources, namely:
* FXempire.com
* DailyFX.com
* CNBC
* Investing.com

My stock data was initially collected by using yfinance but I am currently learning how to effectively use Alpaca for more granularity.

Initially, an LSTM model was used for the stock data alone and a CNN made for sentiment analysis for the news headlines.
Both of them was later on used for an ensemble model as a proof of concept.

## Changelogs

02.07.21 - Finally added a proper readme.

## Stack

Research is in Python on Jupyter Notebook.
Data was collected in Python with BS4.
Techniques used: Random Forest Classifier, XGBoost Classifier, Long Short-Term Memory Neural Network, Convolutional Neural Network, Wordcloud, TF-IDF, Padding, Encoding
