import os
import unicodedata
from twilio.rest import Client
import requests
import datetime as dt

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = os.getenv("STOCK_API_KEY")
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_KEY = os.getenv("TWILIO_KEY")
FROM_NUMBER = os.getenv("FROM_NUMBER")
TO_NUMBER = os.getenv("TO_NUMBER")


def get_last_two_closes(symbol):
    parameters = {"function": "TIME_SERIES_DAILY", "symbol": symbol, "apikey": STOCK_API_KEY}
    response = requests.get(STOCK_ENDPOINT, params=parameters)
    data = response.json()["Time Series (Daily)"]
    date_list = [date for date in data]  # List of dates available in returned data
    # Create a tuples for last two trading days available format: (date, closing value)
    last_day = (date_list[0], float(data[date_list[0]]['4. close']))
    prev_day = (date_list[1], float(data[date_list[1]]['4. close']))
    return last_day, prev_day


def get_news(company_name, from_date, to_date):
    parameters = {'q': company_name, 'from': from_date, 'to': to_date, 'sortBy': 'popularity', 'apiKey': NEWS_API_KEY}
    response = requests.get(NEWS_ENDPOINT, params=parameters)
    data = response.json()
    results = []
    for i in range(len(data['articles'][:3])):
        title = data['articles'][i]["title"]
        description = unicodedata.normalize("NFKD", data['articles'][i]["description"])
        results.append((title, description))
    return results


def send_sms(message, from_number, to_number):
    account_sid = TWILIO_SID
    auth_token = TWILIO_KEY
    client = Client(account_sid, auth_token)
    sms_text = client.messages.create(body=message, from_=from_number, to=to_number)
    print(sms_text.status)


close_prices = get_last_two_closes(STOCK_NAME)
last_close, prev_close = get_last_two_closes(STOCK_NAME)
print(close_prices)
price_diff = last_close[1] - prev_close[1]
percent_change = abs(price_diff) / prev_close[1] * 100
print(f"Last Close: {last_close[1]}")
print(f"Previous Close: {prev_close[1]}")
print(f"Difference: {price_diff:0.2f}, Percent Change: {percent_change:0.2f}%")

if percent_change >= 5:
    print('Get News')

print(get_news(COMPANY_NAME, from_date=last_close[1], to_date=last_close[0]))

for article in get_news(COMPANY_NAME, from_date=last_close[1], to_date=last_close[0]):
    next_message = f"{STOCK_NAME}: {'🔺' if price_diff > 0 else '🔻'}{percent_change:0.2f}\n" \
                   f"Headline: {article[0]}\n" \
                   f"Brief: {article[1]}"
    send_sms(message=next_message, from_number=FROM_NUMBER, to_number=TO_NUMBER)



# Optional TODO: Format the message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
