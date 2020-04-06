
import requests
import xmltodict

def cbr(ticket, data=None):
    '''
    Запрос курса валюты.
    :param ticket: тикер, пример: "USD"
    :param data: [НЕ ОБЯЗАТЕЛЬНО] дата курса,  пример: data = "02/02/2020"
    :return:
    '''
    if data is None:
        url =  "http://www.cbr.ru/scripts/XML_daily.asp?"
    else:
        url = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={data}"
    req = requests.get(url).text
    result = xmltodict.parse(req)
    cbr_dict = {}
    for el in result['ValCurs']['Valute']:
        cbr_dict.update({el['CharCode']: float(el['Value'].replace(',', '.'))})
    return {'USD': cbr_dict[ticket],'Date': result['ValCurs']['@Date']}

if __name__ == '__main__':
    for i in range(1,31+1):
        d = str(i).rjust(2,"0")
        print(f"{d}.03.2020",cbr('USD',data = f"{d}/03/2020"))
    for i in range(1,2+1):
        d = str(i).rjust(2,"0")
        print(f"{d}.04.2020",cbr('USD',data = f"{d}/04/2020"))