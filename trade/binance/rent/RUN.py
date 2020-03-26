from mod_telegram import telegram
from mod_ticker import cbr

def wait(run_hour):
    now = dt.now()
    td0 = dt(now.year, now.month, now.day, run_hour, 0, 0).timestamp() - now.timestamp()  # + td(days=1)
    if td0 > 0:
        next_run = now + td(seconds=td0)
        wait_sec = td0
    else:
        next_run = dt(now.year, now.month, now.day, run_hour, 0, 0) + td(days=1)
        wait_sec = (next_run - now).seconds
    print(next_run, wait_sec)
    return(int(wait_sec))

if __name__ == '__main__':
    run_hour = 12
    from private import api_key, secret_key
    bc = binance_class(api_key=api_key,secret_key=secret_key,debug=False)
    while True:
        from time import time, sleep
        from datetime import datetime as dt, timedelta as td
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
        ### deposit end ### deposit end ### deposit end ### deposit end ### deposit end ### deposit end ###

        ### balance ### balance ### balance ### balance ### balance ### balance ### balance ### balance
        asset_balance = bc.get_asset_balance(asset='BTC')
        asset_balance_text = 'Баланс:   ' + \
                             str(asset_balance['asset']) + \
                             ' ' + str(asset_balance['free']) + \
                             ' (locked:' + str(asset_balance['locked']) + ')'
        print("TELEGRAM =>\n\t",asset_balance_text)
        telegram(text=asset_balance_text, endpoints='sendMessage')
        ### balance end ### balance end ### balance end ### balance end ### balance end ### balance end ###
        if float(asset_balance['free']) > 0.000001:
            print('Покупаем USDT')
            order = bc.order_market_sell_all()
            order_text = "id-ордера - " + str(order['orderId']) + \
                         ",\nПродано - " + str(order['origQty']) + order['symbol'][:3] + \
                         ",\nКуплено - " + str(order['cummulativeQuoteQty']) + order['symbol'][3:] + \
                         ",\nцена обмена - " + str(order['fills'][0]['price']) + \
                         ",\nкомиссия - " + str(order['fills'][0]['commission']) + order['fills'][0]['commissionAsset'] + \
                         ",\nid-транзакции - " + str(order['fills'][0]['tradeId'])
        else:
            order_text = "не на что покупать"
        print("TELEGRAM =>\n",order_text)
        telegram(text=order_text, endpoints='sendMessage')
        usdrub = cbr('USD')                         # Цена доллара США.
        power = 1.35                                # Мощьность.
        hour = 24                                   # Расчётный период в часах.
        cost = 3.35                                  # Цена обслуживания (приведенная к цене за киловат)
        opex = round((power*hour*cost)/usdrub,2)    # затраты на обслуживание.
        telegram(text=f'Счет за эл.энергию {opex} $', endpoints='sendMessage')
        sleep(wait(run_hour)) # запускать раз в сутки в <run_hour> часов.
        #sleep(10)             # запускать раз в <столько то> секунд.
