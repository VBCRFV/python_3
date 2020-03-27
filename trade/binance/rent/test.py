from time import time, sleep
from datetime import datetime as dt, timedelta as td

from mod_telegram import telegram
from mod_ticker import cbr
from mod_binance import cls_binance
from mod_txt import json_read,json_write_item,text_write

global debug

def get_deposit_history(asset=None):
    '''
    Возвращает обём последней транзакции по активу <asset>
    :param asset: актив(в простой текстовой форме, см.пример). Пример: "BTC"
    :return: Возвращает обём последней транзакции по активу <asset>
    '''
    ### deposit ### deposit ### deposit ### deposit ### deposit ### deposit ### deposit ### deposit
    deposit_history = bc.get_deposit_history(asset=asset)
    dati = dt.fromtimestamp(deposit_history['insertTime'] / 1000)
    deposit_history_text = 'пополнение:   ' + \
                           str(deposit_history['amount']) + \
                           " " +str(deposit_history['asset']) + \
                           '   ' + str(dati)
    now_t = dt.now()
    today = dati.date() == now_t.date() #- td(days=1)
    if today:
        deposit_history_text = "Сегодня " + deposit_history_text
    else:
        deposit_history_text = "Последнее " + deposit_history_text
    if debug: print("TELEGRAM =>\n\t",deposit_history_text)
    telegram(text=deposit_history_text, endpoints='sendMessage')
    return [today, deposit_history['amount']]
    ### deposit end ### deposit end ### deposit end ### deposit end ### deposit end ### deposit end ###

if __name__ == '__main1__':
    global bc, debug
    debug = True
    from private import api_key, secret_key
    bc = cls_binance(api_key=api_key, secret_key=secret_key, debug=False)  # Грузим API.
    settings = json_read("settings.txt")
    el = 'btc'
    btc = bc.get_asset_balance(asset=el)
    print("Баланс")
    print("\t", bc.get_asset_balance(asset='usdt'))
    print("\t", bc.get_asset_balance(asset='btc'))
    print("\t", bc.get_asset_balance(asset='eth'))
    print("\t", bc.get_asset_balance(asset='ltc'))
    print("Пополнения")
    el = 'btc'
    print(el)
    for el in bc.get_deposit_history(asset=el,last=False):
        print(el)
        print("\t",dt.fromtimestamp(el['insertTime'] / 1000),el['amount'],el['asset'],el['address'],el['txId'])
    el = 'eth'
    print(el)
    for el in bc.get_deposit_history(asset=el, last=False):
        print(el)
        print("\t",dt.fromtimestamp(el['insertTime'] / 1000),el['amount'],el['asset'],el['address'],el['txId'])
    el = 'ltc'
    print(el)
    for el in bc.get_deposit_history(asset=el, last=False):
        print(el)
        print("\t",dt.fromtimestamp(el['insertTime'] / 1000),el['amount'],el['asset'],el['address'],el['txId'])
    #deposit = str(get_deposit_history(asset=el)[1])
    #print(el.upper())
    #print('Транзакция',deposit)
    #print('Округление',deposit[:int(settings[el]['rnd'])+2])
    #print('Отношение',str(float(deposit)*float(settings[el]['ratio']))[:int(settings[el]['rnd'])+2])
    #el = 'eth'
    #deposit = str(get_deposit_history(asset=el)[1])
    #print(el.upper())
    #print('Транзакция',deposit)
    #print('Округление',deposit[:int(settings[el]['rnd'])+2])
    #print('Отношение',str(float(deposit)*float(settings[el]['ratio']))[:int(settings[el]['rnd'])+2])
    #el = 'ltc'
    #deposit = str(get_deposit_history(asset=el)[1])
    #print(el.upper())
    #print('Транзакция',deposit)
    #print('Округление',deposit[:int(settings[el]['rnd'])+2])
    #print('Отношение',str(float(deposit)*float(settings[el]['ratio']))[:int(settings[el]['rnd'])+2])

if __name__ == '__main__':
    txt = "Дата,Тип оборудования,Количество оборудования,Актив,Количество вх.,Штамп времени продажи,Количество проданного,Курс продажи,Получено USDT,Комиссия от продажи USDT,Прибыль от продажи,Коэфф. Потребления,Общее кВт за сутки,Ставка. тариф в руб.,Курс ЦБ,Ставка. тариф в USD,Расходы за ээ,Валовая прибыль,Комиссия за вывод,Выведено USDT,Прибыль,Уровень розетки,Остаток актива\n"
