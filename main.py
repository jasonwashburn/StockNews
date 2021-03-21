import os
import requests
import datetime as dt

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = os.getenv("STOCK_API")
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


def get_last_two_closes(symbol):
    parameters = {"function": "TIME_SERIES_DAILY", "symbol": symbol, "apikey": STOCK_API_KEY}
    response = requests.get(STOCK_ENDPOINT, params=parameters)
    test_list = [value for key, value in response.json()['Time Series (Daily)'].items()]
    last_close_value = (test_list[0]['4. close'])
    prev_close_value = (test_list[1]['4. close'])
    return last_close_value, prev_close_value

close_prices = get_last_two_closes(STOCK_NAME)
last_close = float(close_prices[0])
prev_close = float(close_prices[1])
price_diff = last_close - prev_close
percent_change = abs(price_diff) / prev_close * 100
print(f"Last Close: {last_close}")
print(f"Previous Close: {prev_close}")
print(f"Difference: {price_diff:0.2f}, Percent Change: {percent_change:0.2f}%")

if percent_change >= 5:
    print('Get News')

# STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").




#TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").





    ## STEP 2: https://newsapi.org/ 
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.





#TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.

#TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation


    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 

#TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.

#TODO 9. - Send each article as a separate message via Twilio. 



#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

