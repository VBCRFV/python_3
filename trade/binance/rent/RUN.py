'''
ОПИСАНИЕ.
Скрипт для обмена актива(BTC,LTC,ETH) в USDT.

НАСТРОКА осуществляется изменением файлов:
1) private.py
    api_key - api_key биржи binance.com
    secret_key - secret_key биржи www.binance.com
    token - token telegram бота для отправки сервисных сообщений.
    chat_id - chat_id telegram пользователя\группы для отправки сервисных сообщений.
2) settings.txt
    формат записи: "btc": {"time": "12:00", "rnd": 4}
    "btc" - актив подлежащий обмену в USDT
    "time" - время обмена.
    "rnd" - округление в низ до <rnd> знака после запятой.

ЛОГИКА РАБОТЫ
./doc/rent.drawio

ИСТОРИЯ ИЗМЕНЕНИЙ.
26.03.2020 v0.1
    Стартовая версия. (схема в ./doc/rent.drawio)
27.03.2020 v0.2
    Переделанная версия. (схема в ./doc/rent.drawio)

GIT
    не используется.
'''


from time import time as t, sleep
from datetime import datetime as dt, timedelta as td

from mod_telegram import telegram
from mod_ticker import cbr
from mod_binance import cls_binance
from mod_txt import json_read,json_write,json_write_item,text_write,file_exists

global debug

#def get(settings=None,element=None):
#    if settings is None or element is None:
#        print('ERROR: get(None)')
#        return None
#    arr = {}
#    for el in settings['tickers']:
#        if debug: print("[DEBUG]",el,settings[el][element])
#        arr.update({el:settings[el][element]})
#    return arr

def now_time():
    '''
    Возвращает текущее время в строчном формате HH:MM.
    :return:
    '''
    hour, minute, second_micro = dt.now().time().isoformat().split(':')
    return hour+":"+minute

def compare(time):
    '''
    возвращает разницу в секундах до времени <time>
    :param time: время (в простой текстовой форме, см.пример) до которого нужно выяснить количество оставшихся секунд. Пример: "12:00"
    :return: возвращает разницу в секундах до времени <time>
    '''
    from datetime import datetime as dt
    now = dt.now()
    hour, minute = time.split(":")
    time = dt(now.year, now.month, now.day, hour=int(hour), minute=int(minute), second=0, microsecond=0, tzinfo=None)
    if now > time:
        return [True,-1]
    else:
        return [False,(time-now).seconds]

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
    today = dati.date() == now_t.date() - td(days=5)
    if today:
        deposit_history_text = "Сегодня " + deposit_history_text
    else:
        deposit_history_text = "Последнее " + deposit_history_text
    if debug: print("TELEGRAM =>\n\t",deposit_history_text)
    telegram(text=deposit_history_text, endpoints='sendMessage')
    return [today, deposit_history]
    ### deposit end ### deposit end ### deposit end ### deposit end ### deposit end ### deposit end ###

def plus1h(settings,el):
    '''
    Добавляет 1 час (атрибут 'time') в настройке <settings> в элемент <el>
    :param settings: Словарь настроек загруженный из файла 'settings.txt'
    :param el: Элемент из словаря. Пример: "btc"
    :return: Изменённый словарь настроек.
    '''
    h,m = settings[el]['time'].split(":")
    h = dt.now().hour
    if int(h) < 23:
        settings[el]['time'] = str(int(h)+1).rjust(2,"0")+":"+str(int(m)+1).rjust(2,"0")
    return settings

def wait(settings):
    '''
    Функция возвращает время ожидания до следующего <time> или нового для.
    :param settings: Словарь настроек загруженный из файла 'settings.txt'
    :return: Функция возвращает время в секундах.
    '''
    compare_list = []
    if len(settings) > 0:
        for el in settings:
            compare0 = compare(settings[el]['time'])
            if not compare0[0]:
                compare_list.append(compare0[1])
    if compare_list == []:
        seconds = compare("23:59")[1] + 62
        print(f"Ждём полночь, через {seconds} секунд, будет {dt.now()+td(seconds=seconds)}")
    else:
        seconds = min(compare_list)+1
        print(f"Ждём, через {seconds} секунд, будет {dt.now()+td(seconds=seconds)}")
    return seconds

def check_db(settings):
    def create_blank(elements):
        # Создать бланк.
        now_date = dt.utcnow().date()
        bdl = {str(now_date): {}}
        blank = {
            'incoming': {
            },
            'deposit': {
            },
            'order': {
            },
            'cbr': {
            },
            'outgoing': {
            }
        }
        for el in elements:
            bdl[str(now_date)].update({el: blank})
        return bdl
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
    global bc,debug
    settings = []
    while True:
        if settings != []:
            text_write('log.txt', settings + "\n", mode='a', encoding='utf8')
        debug = False                                                                                               # Дебажим.
        from private import api_key, secret_key
        bc = cls_binance(api_key=api_key, secret_key=secret_key, debug=debug)                                                               # Грузим API.
        settings=json_read("settings.txt")                                                                          # Грузим настройки.
        check_db(settings)

        now_date = str(dt.utcnow().date())
        y, d, m = now_date.split('-')
        db_name = y + '-' + d + '.txt'
        dbl = json_read(db_name)[now_date]
        dbl = bc.incoming(dbl)
        item = {now_date:dbl}
        json_write_item(db_name, item)
        print('dbl:',dbl)
        today = dt.now().day
        while today == dt.now().day:
            bc = cls_binance(api_key=api_key, secret_key=secret_key, debug=False)                                                               # Грузим API.
            if debug:
                print("[DEBUG]",f"len({len(settings)})","settings ==",settings)                                     #
            if len(settings) > 0:                                                                                  # [есть строки] ДА
                now_t = now_time()                                                                                  # Текущее время.
                settings_pop = []                                                                                   #
                for el in settings:                                                                                 # ПЕРЕБОР ВСЕХ ПАР.
                    print("Актив",el.upper(),", Обмен в",settings[el]['time'],", Сейчас",now_t)                     #
                    compare_time = compare(settings[el]['time'])                                                    #
                    if compare_time[0]:                                                                             # [есть совпадение по времени] ДА
                        deposit_history = get_deposit_history(asset=el)                                             #
                        if debug: print("[DEBUG]",f"get_deposit_history(asset={el}):",deposit_history)              #
                        if deposit_history[0]:                                                                      # [Есть входящая транзакция] ДА
                            dbl[el.upper()]['deposit'].update(deposit_history[1])
                            print("\tВходящая транзакция",deposit_history[1])                            #
                            if float(deposit_history[1]['amount']) > float("0.".ljust(int(settings[el]['rnd'])+1,"0")+"1"):   # [выше минимума] ДА
                                print("\t\tПокупка USDT")
                                symbol = el.upper()+"USDT"
                                #quantity = float(str(deposit_history[1])[:int(settings[el]['rnd'])+2]) # Продаём всё (4 знака)
                                quantity = float(str(float(deposit_history[1]['amount']) * float(settings[el]['ratio']))[:int(settings[el]['rnd']) + 2])
                                order = bc.order_market_sell(symbol=symbol, quantity=quantity)
                                if order[0]:
                                    dbl[el.upper()]['order'].update(order[1])
                                    print("\t\tUSDT куплен.")
                                    print("\t\torder:", order)
                                else:
                                    print("\t\tUSDT НЕ куплен(скорее всего недостаточный баланс).")
                                    print("\t\tbalance:", order)
                                text_write('log.txt', str(order) + "\n", mode='a', encoding='utf8')
                                settings_pop.append(el)
                            else:                                                                                   # [выше минимума] НЕТ
                                pass
                        else:                                                                                       # [Есть входящая транзакция] НЕТ
                            print("\tНЕТ входящей транзакции, ждём час.")
                            settings = plus1h(settings,el)
                    else:                                                                                           # [есть совпадение по времени] НЕТ (по сути бесполезное ветвление)
                        pass                                                                                        # по сути бесполезное ветвление
                item = {now_date: dbl}
                json_write_item(db_name, item)
                for el in settings_pop:
                    settings.pop(el)
                if debug: print("[DEBUG]",'len(settings) ==',len(settings))
                if debug: print("[DEBUG]","settings:", settings)
                sleep(wait(settings))
            else:                                                                                                   # [есть строки] НЕТ
                if debug: print("[DEBUG]","[есть строки] НЕТ")
                dbl = outgoing(dbl)
                item = {now_date: dbl}
                json_write_item(db_name, item)
                sleep(wait(settings))
            today = dt.now().day
            print()
