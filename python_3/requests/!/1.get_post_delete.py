def get_position(apiKey, apiSecret, symbol):
    import time, json, hmac, hashlib, requests
    verb = 'GET'
    path = '/api/v1/position?filter=%7B%22symbol%22%3A%22' + symbol + '%22%2C%22isOpen%22%3Atrue%7D'
    expires = int(round(time.time()) + 5)
    data = ''
    message = verb + path + str(expires) + data  # json.dumps(data)
    signature = hmac.new(bytes(apiSecret, 'utf8'), bytes(message, 'utf8'), digestmod=hashlib.sha256).hexdigest()
    headers = {}
    headers['api-expires'] = str(expires)
    headers['api-key'] = apiKey
    headers['api-signature'] = signature
    q = requests.get("https://www.bitmex.com" + path, headers=headers)  #
    while str(q) != "<Response [200]>":
        from time import sleep
        sleep(1)
        q = requests.get("https://www.bitmex.com" + path, headers=headers) # todo не обратимый цикл.
    text = q.text
    ret = json.loads(text)
    return ret

def post_stop(apiKey, apiSecret, stopPx=None, orderQty=0, symbol=None, execInst="Close,LastPrice",pegOffsetValue=None, pegPriceType=''):
    import time, json, hmac, hashlib, requests
    base_url = 'https://www.bitmex.com'
    verb = 'POST'
    data = {"orderQty": orderQty, "ordType": "Stop", "stopPx": stopPx, "symbol": symbol, "execInst": execInst,"pegOffsetValue": pegOffsetValue, "pegPriceType": pegPriceType}
    f_url = '/api/v1/order'
    url = base_url + f_url
    expires = int(round(time.time()) + 5)
    message = verb + f_url + str(expires) + json.dumps(data)
    signature = hmac.new(bytes(apiSecret, 'utf8'), bytes(message, 'utf8'), digestmod=hashlib.sha256).hexdigest()
    headers = {'api-expires': str(expires), 'api-key': apiKey, 'api-signature': signature}
    r = requests.post(url, headers=headers, json=data)
    return r.text

def delete_stop(apiKey, apiSecret, orderID=None):
    import time, json, hmac, hashlib, requests
    base_url = 'https://www.bitmex.com'
    verb = 'DELETE'
    data = {"orderID": orderID}
    f_url = '/api/v1/order'
    url = base_url + f_url
    expires = int(round(time.time()) + 5)
    message = verb + f_url + str(expires) + json.dumps(data)
    signature = hmac.new(bytes(apiSecret, 'utf8'), bytes(message, 'utf8'), digestmod=hashlib.sha256).hexdigest()
    headers = {'api-expires': str(expires), 'api-key': apiKey, 'api-signature': signature}
    r = requests.delete(url, headers=headers, json=data)
    return r.text