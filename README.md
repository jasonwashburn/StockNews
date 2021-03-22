# Stock News
A python script to check the last trading day's closing price of a requested stock and compare it to the previous day's 
closing price. If the change is greater than 5%, it will send you an SMS message to alert you along with the top three 
news articles about that stock from that time period. 

Uses the [Alphavantage Vantage](https://www.alphavantage.co/) API, documented 
[here](https://www.alphavantage.co/documentation/), for stock prices, and the [newsapi.org](https://newsapi.org) API, 
documented [here](https://newsapi.org/docs), for news items.

SMS Text Messages are sent using the [Twilio](https://www.twilio.com/docs/usage/api) API.