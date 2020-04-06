#!/usr/bin/python
# -*- coding: utf8 -*-
from binance.client import Client as Clibin
from private import api_key, secret_key
from datetime import datetime as dt
from mod_txt import text_write,json_write_item,json_write,json_read,file_exists
from mod_ticker import cbr

if __name__ == '__main1__':
    global bc, debug
    elments = ['BTC','ETH','LTC','USDT']
    client = Clibin(api_key, secret_key)
    debug = True
    bd = {}                                                                    # Создаём элемент БД.
    now_date = dt.utcnow().date()                                               # Создаем день.
    bd.update({str(now_date):{}})                                               # Создаем день.
    for el in elments:                                                           # Добавляем остаток на начало дня.
        asset_balance = client.get_asset_balance(asset=el)                       # Добавляем остаток на начало дня.
        print(asset_balance)                                                     # Добавляем остаток на начало дня.
        bd[str(now_date)].update({el:{'asset_free0':asset_balance['free']}})     # Добавляем остаток на начало дня.
    print(bd)

#qwe = {}
#qwe.update({'a':{}})
#qwe['a'].update({'b':2})
#qwe['a'].update({'c':3})
#
#print(qwe)

def create_blank(elements):
    # Создать бланк.
    now_date = dt.utcnow().date()
    bdl = {str(now_date):{}}
    blank = {
            'incoming': {
            },
            'deposit': {
            },
            'order': {
            },
            'cbr': {
            },
            'outgoing':{
            }
        }
    for el in elements:
        bdl[str(now_date)].update({el:blank})
    return bdl

def show_db(bdl):
    # прочитать БД
    for el0 in bdl:
        print(el0)
        for el1 in bdl[el0]:
            print('\t',el1)
            for el2 in bdl[el0][el1]:
                print('\t\t',el2,bdl[el0][el1][el2])

def show_csv(bdl):
    # прочитать БД
    for el0 in bdl:
        print(el0)
        for el1 in bdl[el0]:
            print('\t',el1)
            for el2 in bdl[el0][el1]:
                print('\t\t',el2,bdl[el0][el1][el2])

def check_db(settings):
    elements = []
    for el in settings:
        elements.append(el.upper())
    now_date = str(dt.utcnow().date())
    y,d,m = now_date.split('-')
    db_name = y+'-'+d+'.txt'
    if file_exists(db_name): # [Есть год-месяц.txt файл ] ДА
        print('[Есть год-месяц.txt файл ] ДА')
        db = json_read(db_name)
        dbl = db.get(now_date)
        if dbl is None:
            dbl = create_blank(elements)  # Создать год-месяц-день + Создать активы + blank
            json_write_item(db_name, dbl, el=None)
            print('\tдобавлена запись',now_date)
        else:
            print('\tзапись', now_date, 'существует')
    else:   # [Есть год-месяц.txt файл ] НЕТ
        print('[Есть год-месяц.txt файл ] НЕТ')
        db = {}                                     # Создать год-месяц
        dbl = create_blank(elements)                # Создать год-месяц-день + Создать активы + blank
        db.update(dbl)                              # Добавляем строку созданную ывыше в db
        json_write(db_name,db)                      # Записываем db.txt
        print('\tсоздан файл',db_name, 'со структурой')

if __name__ == '__main__':
    now_date = str(dt.utcnow().date())
    y, d, m = now_date.split('-')
    db_name = y + '-' + d + '.txt'
    db = json_read(db_name)
    show_db(db)
    print('\n\n\n')
    ####################################################
    ### Создание переменных ###
    const = {'BTC': {'b': 'Antminer S9', 'c': 10, 'l': 1.5,'n': 2.5,'s': 1.1},
             'ETH': {'b': 'GPU', 'c': 10, 'l': 1.4,'n': 2.5,'s': 1.1},
             'LTC': {'b': 'Antminer L3', 'c': 10, 'l': 1,'n': 2.5,'s': 1.1}}
    txt_a = ""              # Дата
    txt_b = "Antminer S9"   # Тип оборудования
    txt_c = 100             # Количество оборудования
    txt_d = 0               # Актив
    txt_e = 0               # Количество вх.
    txt_f = 0               # Штамп времени продажи
    txt_g = 0               # Количество проданного
    txt_h = 0               # Курс продажи
    txt_i = 0               # Получено USDT
    txt_j = 0               # Комиссия от продажи USDT
    txt_k = 0               # Прибыль от продажи
    txt_l = 1.00            # Коэфф. Потребления
    txt_m = 0               # Общее кВт за сутки
    txt_n = 2.5             # Ставка, тариф в руб.
    txt_o = 80              # Курс ЦБ # TODO вносить при запуске.
    txt_p = 0               # Ставка, тариф в USD
    txt_q = 0               # Расходы за э/э
    txt_r = 0               # Валовая прибыль
    txt_s = 1.1             # Комиссия за вывод
    txt_t = 0               # Прибыль
    txt_u = 0               # Выведено USDT
    txt_v = 0               # Уровень розетки
    txt_w = 0               # Остаток USDT
    txt_x = 0               # Остаток актива

    txt_o = cbr('USD')
    ######################################################
    ### Заполнение строк ###
    #txt = ""
    txt = str("Дата;Тип оборудования;Количество оборудования;Актив;Количество вх;Штамп времени продажи;Количество проданного;Курс продажи;Получено USDT;Комиссия от продажи USDT;Прибыль от продажи;Коэфф Потребления;Общее кВт за сутки;Ставка тариф в руб;Курс ЦБ;Ставка тариф в USD;Расходы за э/э;Валовая прибыль;Комиссия за вывод;Прибыль;Выведено USDT;Уровень розетки;Остаток USDT;Остаток актива\n") #
    for el0 in db:
        txt_a = el0
        print(el0)
        for el1 in db[el0]:
            txt_d = el1
            print('\t',el1)
            if el1 != 'USDT':
                txt_b = const[el1]['b']
                txt_c = const[el1]['c']
                txt_n = round(const[el1]['n'],3)
                txt_l = round(const[el1]['l'],3)
                txt_s = round(const[el1]['s'],3)
                txt_m = round(txt_c * txt_l * 24,2)                     # Общее кВт за сутки
                txt_p = round(txt_n / txt_o,4)                                   # Ставка, тариф в USD
                txt_e = round(float(db[el0][el1]['deposit'].get('amount',1)),8)
                #txt_f = db[el0][el1]['order'].get('transactTime','000')
                txt_f =dt.fromtimestamp(int(db[el0][el1]['order'].get('transactTime',1000)/1000)).isoformat()
                txt_g = round(float(db[el0][el1]['order'].get('origQty',0)),4)
                if txt_g != 0:
                    txt_h = round(float(db[el0][el1]['order'].get('cummulativeQuoteQty',None))/float(db[el0][el1]['order'].get('executedQty',None)),3)
                    txt_i = round(float(db[el0][el1]['order'].get('cummulativeQuoteQty',0)),3)
                    fills = db[el0][el1]['order'].get('fills',[{'commission':'0.0'},{'commission':'0.0'}])
                    commission = 0
                    for el in fills:
                        commission = commission + float(el['commission'])
                    txt_j = round(commission,4)
                    txt_k = round(float(txt_i) - float(txt_j),3)
                    txt_q = round(txt_m * txt_p,3)
                    txt_r = round(txt_k - txt_q,3)
                    txt_t = round(txt_r - txt_s,3)
                    txt_u = round(txt_t,3)
                    txt_v = round(txt_q / txt_e,3)
                    txt_w = round(txt_t - txt_u,3)
                    txt_x = round(txt_e - txt_g,8)
                # incoming
                # deposit
                # order
                # cbr
                # outgoing
                #for el2 in db[el0][el1]:
                #    print('\t\t',el2,db[el0][el1][el2])
                ####################################################
                ### Создание строк ###
                csv_line =  str(txt_a) + "," + \
                            str(txt_b) + "," + \
                            str(txt_c) + "," + \
                            str(txt_d) + "," + \
                            str(txt_e) + "," + \
                            str(txt_f) + "," + \
                            str(txt_g) + "," + \
                            str(txt_h) + "," + \
                            str(txt_i) + "," + \
                            str(txt_j) + "," + \
                            str(txt_k) + "," + \
                            str(txt_l) + "," + \
                            str(txt_m) + "," + \
                            str(txt_n) + "," + \
                            str(txt_o) + "," + \
                            str(txt_p) + "," + \
                            str(txt_q) + "," + \
                            str(txt_r) + "," + \
                            str(txt_s) + "," + \
                            str(txt_t) + "," + \
                            str(txt_u) + "," + \
                            str(txt_v) + "," + \
                            str(txt_w) + "," + \
                            str(txt_x) + "\n"
                print('\t\t',csv_line)
                csv_line = csv_line.replace(",", ";").replace(".", ",").replace("1970-01-01T08:00:01", "0000-00-00 00:00:00")
                #csv_line = csv_line.replace(".", ",") #.replace("1970-01-01T08:00:01", "0000-00-00 00:00:00")
                text_write(db_name.split('.')[0]+'_export_'+str(txt_d)+'.csv', csv_line, mode='a', encoding='utf8')
            txt = txt + csv_line
            csv_line = ""
    print(txt)
    #txt = txt.replace(".", ",").replace("1970-01-01T08:00:01", "0000-00-00 00:00:00")
    text_write('export.csv', txt, mode='w', encoding='utf8')
#hour, minute, second_micro = dt.now().time().isoformat().split(':')
# dt.fromtimestamp(1585213622).isoformat()
    #settings = json_read("settings.txt")
    #check_db(settings)
    #now_date = str(dt.utcnow().date())
    #y, d, m = now_date.split('-')
    #db_name = y + '-' + d + '.txt'
    #dbl = json_read(db_name)[now_date]
    #incoming(dbl)
#line = {el:{'asset_free0':None,'asset_free1':None,}}

# 'asset_free0' - Остаток на начало дня.
# 'asset_free1' - Остаток на конец дня.

# Баланс(balance): {'asset': 'BTC', 'free': '0.00000453', 'locked': '0.00000000'}
# Пополнение(deposit): {'insertTime': 1585213622000, 'amount': 0.00170356, 'creator': None, 'address': '12xM4yTjgHVyzD1KRbAHv8Gt1oZa3A6iQ2', 'addressTag': '', 'txId': 'Internal transfer 7457405220', 'asset': 'BTC', 'status': 1}
# Продажа(order): {'symbol': 'LTCUSDT', 'orderId': 479024287, 'orderListId': -1, 'clientOrderId': 'UmbOdl9cYhonfmZUDRV9QQ', 'transactTime': 1585544747747, 'price': '0.00000000', 'origQty': '10.00000000', 'executedQty': '10.00000000', 'cummulativeQuoteQty': '381.26123510', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'MARKET', 'side': 'SELL', 'fills': [{'price': '38.13000000', 'qty': '6.12351000', 'commission': '0.23348944', 'commissionAsset': 'USDT', 'tradeId': 45796033}, {'price': '38.12000000', 'qty': '0.52424000', 'commission': '0.01998403', 'commissionAsset': 'USDT', 'tradeId': 45796034}, {'price': '38.12000000', 'qty': '3.35225000', 'commission': '0.12778777', 'commissionAsset': 'USDT', 'tradeId': 45796035}]}