from time import time, sleep
from datetime import datetime as dt

from mod_telegram import telegram
from mod_ticker import cbr
from mod_binance import cls_binance
from mod_txt import json_read,json_write_item

global debug

def get(settings=None,element=None):
    if settings is None or element is None:
        print('ERROR: get(None)')
        return None
    arr = {}
    for el in settings['tickers']:
        if debug: print("DEBUG:",el,settings[el][element])
        arr.update({el:settings[el][element]})
    return arr

def now():
    hour, minute, second_micro = dt.now().time().isoformat().split(':')
    return hour+":"+minute

def get_deposit_history():
    ### deposit ### deposit ### deposit ### deposit ### deposit ### deposit ### deposit ### deposit
    deposit_history = bc.get_deposit_history()
    dati = dt.fromtimestamp(deposit_history['insertTime'] / 1000)
    #print(dati.year == now.year,dati.month == now.month,dati.day == now.day)
    deposit_history_text = 'пополнение:   ' + \
                           str(deposit_history['amount']) + \
                           " " +str(deposit_history['asset']) + \
                           '   ' + str(dati)
    now = dt.now()
    today = dati.date() == now.date()
    if today:
        deposit_history_text = "Сегодня " + deposit_history_text
    else:
        deposit_history_text = "Последнее " + deposit_history_text
    print("TELEGRAM =>\n\t",deposit_history_text)
    telegram(text=deposit_history_text, endpoints='sendMessage')
    return [today, deposit_history['amount']]
    ### deposit end ### deposit end ### deposit end ### deposit end ### deposit end ### deposit end ###

if __name__ == '__main__':
    from private import api_key, secret_key
    global bc
    bc = cls_binance(api_key=api_key, secret_key=secret_key, debug=False)
    debug = True                                                # Дебажим.
    from private import api_key, secret_key                     # Грузим API.
    settings=json_read("settings.txt")                          # Грузим настройки.
    if debug: print("DEBUG:","settings ==",settings)            #
    time_dict = get(settings=settings,element='time')           # Получить словарь времени обмена.
    now = now()                                                 # Текущее время.
    for el in time_dict:                                        # [есть совпадение по времени]
        if time_dict[el]==now:                                  # [ДА] (есть совпадение по времени)
            bc.asset = el                                       # заполняем актив.
            deposit_history = get_deposit_history()
            if deposit_history[0]:                        # [Есть входящая транзакция]
                print('\t\t[Есть входящая транзакция]','ДА')
                print('\t\t',deposit_history[1])
            else:
                print('\t\t[Есть входящая транзакция]','НЕТ')
                settings.
        print()
