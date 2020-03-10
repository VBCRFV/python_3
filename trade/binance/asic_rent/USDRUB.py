from yfinance import download
price = download(tickers='RUB=X',period = "1d",interval='60m') # period - диапазон за который берутся свечи, interval - таймфрейм (если написать 1h вместо 60m придут те же данные, но без часовых timestamp-ов)
print(price) # последняя свеча присылается не закрытой!