def telegram(text="тест",endpoints="getUpdates",timeout = 3,token = None, chat_id = None):
    if token is None:
        from private import token
    if chat_id is None:
        from private import chat_id
    from time import time
    import requests
    if endpoints=="getUpdates":
        url = f'https://api.telegram.org/bot{token}/getUpdates'
    elif endpoints=="sendMessage":
        url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}'
    else:
        url = f'https://api.telegram.org/bot{token}/getMe'
    try:
        req = requests.get(url,timeout=timeout).text
    except requests.exceptions.ConnectTimeout:
        print('[ERROR] mod_telegram.telegram(): telegram.org - недоступен, пробуем через Tor.(для этого он должен быть установлен\запущен)')
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