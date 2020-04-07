def telegram(text="тест",endpoints="getUpdates",timeout = 3,bot = None,chat_id = None):
    from time import time
    import requests
    if endpoints=="getUpdates":
        url = f'https://api.telegram.org/bot{bot}/getUpdates'
    elif endpoints=="sendMessage":
        url = f'https://api.telegram.org/bot{bot}/sendMessage?chat_id={chat_id}&text={text}'
    else:
        url = f'https://api.telegram.org/bot{bot}/getMe'
    not_sent = True
    try:
        req = requests.get(url,timeout=timeout).text
        not_sent = False
    except requests.exceptions.ConnectTimeout:
        print('[ERROR] telegram(): telegram.org - недоступен, пробуем через Tor.(для этого он должен быть запущен)')
        #import os
        #os.system('cmd /c "C:\\Users\\AT-BC-D1\\Desktop\\Tor Browser\\Browser\\firefox.exe"')
        import socket
        import socks
        ip = '127.0.0.1'
        port = 9150
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, ip, port)
        socket.socket = socks.socksocket
        try:
            req = requests.get(url, timeout=timeout).text
            not_sent = False
        except requests.exceptions.ConnectionError:
            req = 'ConnectionError'
            print('[ERROR] telegram():\t\t'+req)
    except:
        req = '[ERROR] telegram(): Что то пошло не так.'
        print(req)
    if req == '{"ok":false,"error_code":404,"description":"Not Found"}': not_sent = True
    if not_sent: print(' [ ↓↓  ↓↓ ]','[ ↓↓ ] '*20 ,'\n','[TELEGRAM]',text,'\n','[ ↑↑  ↑↑ ]','[ ↑↑ ] '*20)
    return req

