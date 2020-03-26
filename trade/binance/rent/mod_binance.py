class cls_binance():
    def __init__(self, api_key=None,secret_key=None, debug=False, asset='BTC', symbol = 'BTCUSDT'):
        if debug: print('[DEBUG]',f'binance_class().__init__(debug={debug},api_key={api_key},secret_key={secret_key})', )
        from binance.client import Client as Clibin
        self.api_key = api_key
        self.secret_key = secret_key
        self.debug = debug
        self.asset = asset.upper()
        self.symbol = symbol
        self.client = Clibin(api_key, secret_key)
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
    def get_deposit_history(self):
        '''
        Запрос списка входящих транзакций.
        :param self:
        :return:
        '''
        self.depositList = self.client.get_deposit_history(asset=self.asset.upper())['depositList']
        if self.debug: print('[DEBUG]','self.depositList:',self.depositList)
        if self.depositList == []:
            self.depositList = {'asset': self.asset.upper(), 'amount': 'None','insertTime': 1000}
        else:
            self.depositList = self.depositList[-1]
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
        Продажа всего актива.
        :param self:
        :param symbol: тикер (например: BTCUSDT, продаём BTC - покупаем USDT)
        :return:
        '''
        if symbol is None: symbol = self.symbol
        free = self.balance['free']
        self.order_market = self.client.order_market_sell(symbol=symbol,quantity=quantity)
        return self.order_market