from binance.client import Client
api_key = 'api_key'
api_secret = 'api_secret'
pair = 'BTC'
#ticker_list = ['BTT','ONG','ONT']
client = Client(api_key, api_secret)

def text_read(file_name):
    f = open(file_name)
    file = f.read()
    f.close()
    return file

if __name__ == '__main__':
    ticker_list_txt = text_read('ticker_list.txt').split()
    ticker_list = []
    for symbol in ticker_list_txt:
        ticker_list.append(symbol)
    print('список тикеров:',ticker_list,'\n')
    ticker = client.get_ticker()
    ticker_dict = {}
    for el in ticker:
        ticker_dict.update({el['symbol']:el['lastPrice']})
    for el in ticker_list:
        print(el.upper()+pair,ticker_dict.get(el.upper()+pair,'НЕТ ТАКОГО ТИКЕРА'))

