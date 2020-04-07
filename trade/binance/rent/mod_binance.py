class cls_binance():
    def __init__(self, api_key=None,secret_key=None, debug=False, asset='BTC', symbol = 'BTCUSDT'):
        if debug: print('[DEBUG]',f'binance_class().__init__(debug={debug},api_key={api_key},secret_key={secret_key})', )
        from binance.client import Client as Clibin
        self.api_key = api_key
        self.secret_key = secret_key
        self.debug = debug
        self.asset = asset.upper()
        self.symbol = symbol
        try:
            self.client = Clibin(api_key, secret_key)
        except binance.exceptions.BinanceAPIException:
            self.client = Clibin(api_key, secret_key)
        except:
            print('Что то пошло не так.')
        self.time()
    def time(self):
        '''
        проверка синхронности времени сервера и локального времени.
        (если у Вас высокая латентность сети, будут возникать ошибка "Необходима синхронизация времени.")
        :return:
        '''
        from time import time, sleep
        server_time = self.client.get_server_time()
        local = int(time())
        binance = int(server_time['serverTime'] / 1000)
        residual = binance - local
        if abs(residual) > 1:
            print('residual:',residual)
            print('Выполните комманды: (в cmd.exe с правами администратора)')
            print('net start w32time')
            print('w32tm /resync')
            raise Exception("Необходима синхронизация времени.")
        else:
            if self.debug: print('Время сервера и локальное время синхронны. \n')
    def get_deposit_history(self,asset=None,last=True):
        '''
        Запрос списка входящих транзакций.
        :param self:
        :return:
        '''
        if asset is None:
            asset = self.asset.upper()
        self.depositList = self.client.get_deposit_history(asset=asset.upper())['depositList']
        if self.debug: print('[DEBUG]','self.depositList:',self.depositList)
        if self.depositList == []:
            self.depositList = {'asset': self.asset.upper(), 'amount': 'None','insertTime': 1000}
        else:
            if last:
                self.depositList = self.depositList[0]
            else:
                pass
        return self.depositList
    def get_asset_balance(self, asset=None):
        '''
        Запрос баланса актива <asset>
        :param self:
        :param asset: код актива (например "BTC")
        :return:
        '''
        if asset is None: asset = self.asset
        if self.debug: print('[DEBUG]','self.depositList:', self.depositList)
        self.balance = self.client.get_asset_balance(asset=asset)
        if self.balance is None:
            self.balance = {'free': 'None','locked': 'None'}
        return self.balance
    def order_market_sell_all(self, symbol=None):
        '''
        Продажа всего актива.
        :param self:
        :param symbol: тикер (например: BTCUSDT, продаём BTC - покупаем USDT)
        :return:
        '''
        if symbol is None: symbol = self.symbol
        free = self.balance['free']
        self.order_market = self.client.order_market_sell(symbol=symbol,quantity=float(str(free)[:8]))
        return self.order_market
    def order_market_sell(self, symbol=None,quantity=None):
        '''
        Продажа quantity актива.
        :param self:
        :param symbol: тикер (например: BTCUSDT, продаём BTC - покупаем USDT)
        :return:
        '''
        if symbol is None: symbol = self.symbol
        try:
            self.order_market = self.client.order_market_sell(symbol=symbol,quantity=quantity)
            return [True,self.order_market]
        except:
            print(f"[ERROR] mod_binance.cls_binance().order_market_sell(symbol={symbol},quantity={quantity}).except:")
            self.balance = self.client.get_asset_balance(asset=symbol[:3])
            return [False,self.balance]
    def incoming(self,dbl):
        from time import time as t
        for el in dbl:
            if dbl[el]['incoming'] == {}:
                dbl[el]['incoming'].update({'requestTime': int(t())})
                dbl[el]['incoming'].update(self.client.get_asset_balance(asset=el))
        if dbl.get('USDT') is None:
            dbl.update({'USDT':{'incoming':self.client.get_asset_balance(asset='USDT')}})
            dbl['USDT']['incoming'].update({'requestTime': int(t())})
        return dbl
    def outgoing(self,dbl):
        from time import time as t
        for el in dbl:
            if dbl[el]['outgoing'] == {}:
                dbl[el]['outgoing'].update({'requestTime': int(t())})
                dbl[el]['outgoing'].update(self.client.get_asset_balance(asset=el))
        if dbl.get('USDT') is None:
            dbl.update({'USDT':{'outgoing':self.client.get_asset_balance(asset='USDT')}})
            dbl['USDT']['outgoing'].update({'requestTime': int(t())})
        return dbl

if __name__ == '__main__':
    pass