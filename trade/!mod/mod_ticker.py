import requests
import xmltodict

def cbr(ticket):
    url =  "http://www.cbr.ru/scripts/XML_daily.asp?"
    req = requests.get(url).text
    result = xmltodict.parse(req)
    cbr_dict = {}
    for el in result['ValCurs']['Valute']:
        cbr_dict.update({el['CharCode']:float(el['Value'].replace(',','.'))})
    return cbr_dict[ticket]

if __name__ == '__main__':
    print(cbr('USD'))