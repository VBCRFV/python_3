from private import private_dict
from time import time, sleep
import json
from mod_txt import *
access_list = []
for el in private_dict:
    access_list.append(int(el))
global whait,settings_fn
settings_fn = 'settings.txt'
settings = json_read(settings_fn)
whait = settings['whait']
print('access_list:',access_list)

def telegram(text="тест",endpoints="getUpdates",timeout = 3,bot = "1234567890:ABCDEFGHIKLMNOPQRSTVXYZ",chat_id = "-1234567890"):
    from time import time
    import requests
    if endpoints=="getUpdates":
        url = f'https://api.telegram.org/bot{bot}/getUpdates'
    elif endpoints=="sendMessage":
        url = f'https://api.telegram.org/bot{bot}/sendMessage?chat_id={chat_id}&text={text}'
    else:
        url = f'https://api.telegram.org/bot{bot}/getMe'
    try:
        req = requests.get(url,timeout=timeout).text
    except requests.exceptions.ConnectTimeout:
        print('telegram.org - недоступен, пробуем через Tor.(для этого он должен быть запущен)\n')
        #import os
        #os.system('cmd /c "C:\\Users\\AT-BC-D1\\Desktop\\Tor Browser\\Browser\\firefox.exe"')
        import socket
        import socks
        ip = '127.0.0.1'
        port = 9150
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, ip, port)
        socket.socket = socks.socksocket
        req = requests.get(url, timeout=timeout).text
    except:
        print('Что то пошло не так.')
    return req

def instruction(inst):
    global whait,settings_fn
    inst0 = inst.split("&")
    print('inst0:',inst0)
    if inst0[0] == '0':
        if len(inst0) == 1:
            print('whait ==',whait)
            telegram(text='whait =='+str(whait), endpoints='sendMessage')
        elif len(inst0) == 2:
            if inst0[1] == '0':
                json_write_item(settings_fn, {'whait':10})
                whait = 10
                print('whait =', 10)
                telegram(text='whait = 10', endpoints='sendMessage')
        elif len(inst0) == 3:
            if inst0[1] == '0':
                json_write_item(settings_fn, {'whait':int(inst0[2])})
                whait = int(inst0[2])
                print('whait =', whait)
                telegram(text='whait = '+str(whait), endpoints='sendMessage')
    elif inst0[0] == '1':
        pass
    else:
        text = '0 - узнать интервал ожидания \n0%260 - установить интервал по умолчанию (10) \n0%260%26int - установить интервал раный <int>'
        print("\n"+text+"\n")
        telegram(text=text, endpoints='sendMessage')
if __name__ == '__main__':
    while True: #Вечный цикл.
        if True: # Время обмена ещё не пришло.
            import json
            update_id = int(text_read("update_id.txt"))     # Получаем последнее прочитаное обновление.
            result = json.loads(telegram())                 # Делаем запрос
            mass = result['result']
            #print('result:',mass)               # Результат запроса, для отладки # (todo: позже задебажить)
            mass_list = []
            for el in mass:
                el_update_id = el['update_id']
                if el_update_id > update_id:     # это новое сообщение?
                    mass_list.append(el['message'])  # Запиываем в список.
            text_write("update_id.txt",el_update_id)
            #print('len_mass_list',len(mass_list)) # (todo: позже задебажить)
            if len(mass_list) > 0: # Есть новые сообщения?
                for el in mass_list: # Перебор всех сообщений.
                    if access_list.count(el['chat']['id']) > 0: # Проверка по access_list.
                        print('id:',el['chat']['id'],'text:',el['text'])
                        instruction(el['text'])
            else:
                print("Нет новых сообщений.")
        print('sleep:',whait, "   el_update_id:",el_update_id)
        sleep(whait)
