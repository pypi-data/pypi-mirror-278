# -*- coding: utf-8 -*-
'''
@Time ： 2022/9/22
@Auth ： zhangping
'''

import requests
from .utils import LoggerUtil


class Order:
    '''
    订单常量定义
    '''
    Buy, Sell = 1, 2  # 买, 卖
    Open, Close, CloseToday, CloseYesterday = 1, 2, 3, 4  # 开仓, 平仓, 平今仓, 平昨仓
    PriceLimit, PriceMarket = 1, 2  # 限价委托,市价委托
    PositionLong, PositionShort = 1, 2  # 多仓, 空仓
    ByVolume, ByValue, ByPercent, ByTargetVolume, ByTargetValue, ByTargetPercent = 1, 2, 3, 4, 5, 6  # 按...下单


ex_position_fields = ['account_id', 'account_name', 'change_event_id', 'change_reason', 'has_dividend',
                      'last_inout', 'last_price', 'last_volume']
ex_order_fields = ['account_id', 'account_name', 'ex_ord_id', 'order_id', 'order_duration', 'order_qualifier',
                   'target_percent', 'target_value', 'target_volume', 'percent', 'value', 'order_src',
                   'stop_price', 'strategy_id']


class SimTrader():
    '''
    指标数据接口客户类
    '''

    def __init__(self, token: str, account_id: int, host='http://sim.shducheng.net', port=8087, log_level='INFO',
                 logs_dir='./logs', api_urls=None):
        '''
        ApiClient构造函数
        :param token: token字符串
        :param account_id: 账户id
        :param host: 接口服务地址，默认：
        :param port: 接口服务端口，默认：
        :param log_level: 日志级别，默认：INFO
        :param api_urls: 自定义接口地址服务路径
        :return:
        '''
        api_urls = api_urls if api_urls is not None else {
            'account_cash': '/trade/sim/account_cash',  # 资金查询
            'account_performance': '/trade/sim/account_performance',  # 资金查询
            'account_positions': '/trade/sim/account_positions',  # 持仓查询
            'account_orders': '/trade/sim/account_orders',  # 当日订单查询
            'account_history_orders': '/trade/sim/account_history_orders',  # 历史订单查询
            'account_unfinished_orders': '/trade/sim/account_unfinished_orders',  # 当日未接订单查询
            'order_volume': '/trade/sim/order_volume',  # 订单委托
            'order_batch': '/trade/sim/order_batch',  # 批量订单委托
            'order_cancel': '/trade/sim/order_cancel',  # 撤单委托
            'order_cancel_all': '/trade/sim/order_cancel_all',  # 撤单委托(全撤)
            'order_close_all': '/trade/sim/order_close_all',  # 全部平仓
            'account_sync': '/trade/sim/account_sync'  # 账户同步
        }

        self.token = token
        self.account_id = account_id
        self.host = (host if host.startswith('http://') else ('http://' + host)) + ':' + str(port)
        self.api_cash = self.host + api_urls['account_cash']
        self.api_performance = self.host + api_urls['account_performance']
        self.api_positions = self.host + api_urls['account_positions']
        self.api_orders = self.host + api_urls['account_orders']
        self.api_account_history_orders = self.host + api_urls['account_history_orders']
        self.api_unfinished_orders = self.host + api_urls['account_unfinished_orders']
        self.api_order_volume = self.host + api_urls['order_volume']
        self.api_order_batch = self.host + api_urls['order_batch']
        self.api_cancel = self.host + api_urls['order_cancel']
        self.api_cancel_all = self.host + api_urls['order_cancel_all']
        self.api_close_all = self.host + api_urls['order_close_all']
        self.api_account_sync = self.host + api_urls['account_sync']
        self.logger = LoggerUtil.get_logger(name='simtrader', level=log_level, logs_dir=logs_dir)

    def _post(self, url, json):
        self.logger.debug('request: ' + self.api_cash)
        r = requests.post(url, None, json, headers={'token': self.token})
        r = r.json()
        if r.get('code') != 200:
            self.logger.error(r)
            return None
        else:
            return r.get('data')

    def query_cash(self):
        '''
        账户资金查询
        @return:
        '''
        result = self._post(self.api_cash, {'account_id': self.account_id})
        return {k: result.get(k) for k in result if k not in ['created_at', 'updated_at']}

    def query_positions(self):
        '''
        账户持仓查询
        @return:
        '''
        result = self._post(self.api_positions, {'account_id': self.account_id})
        return [{k: p.get(k) for k in p if k not in ex_position_fields} for p in result]

    def query_orders(self):
        '''
        当日订单查询
        @return:
        '''
        result = self._post(self.api_orders, {'account_id': self.account_id})
        return [{k: p.get(k) for k in p if k not in ex_order_fields} for p in result]

    def query_unfinished_orders(self):
        '''
        未完成订单查询
        @return:
        '''
        result = self._post(self.api_unfinished_orders, {'account_id': self.account_id})
        return [{k: p.get(k) for k in p if k not in ex_order_fields} for p in result]

    def query_history_orders(self):
        '''
        账户历史查询
        @return:
        '''
        result = self._post(self.api_account_history_orders, {'account_id': self.account_id})
        return [{k: p.get(k) for k in p if k not in ex_order_fields} for p in result]

    def query_performance(self, with_detail: bool = False):
        '''
        账户业绩查询
        @param with_detail: 详情信息标识，值为True时，返回每日资金、持仓及订单信息
        @return:
        '''
        param = {
            'account_id': self.account_id,
            'with_detail': with_detail
        }
        result = self._post(self.api_performance, param)
        if 'positions' in result:
            result['positions'] = [{k: p.get(k) for k in p if k not in ex_position_fields} for p in result['positions']]
        if 'orders' in result:
            result['orders'] = [{k: p.get(k) for k in p if k not in ex_order_fields} for p in result['orders']]
        return result

    def send_order(self, symbol, volume, price=0, buy_sell=Order.Buy, open_lose=Order.Open,
                   order_type=Order.PriceLimit):
        '''
        委托下单
        @param symbol: 合约代码
        @param volume: 委托数量
        @param price: 委托价格，市价单可不填，默认0
        @param buy_sell: 买卖方向: Order.Buy | Order.Sell
        @param open_lose: 开平方向: Order.Open | Order.Close | Order.CloseToday | Order.CloseYesterday
        @param order_type: 价格类型: Order.PriceLimit | Order.PriceMarket
        @return:
        '''
        param = {
            'account_id': self.account_id,
            'symbol': symbol,
            'volume': volume,
            'price': price,
            'side': buy_sell,
            'position_effect': open_lose,
            'order_type': order_type if price > 0 else Order.PriceMarket,
        }
        result = self._post(self.api_order_volume, param)
        return result and result[0] and {k: result[0].get(k) for k in result[0] if k in ['cl_ord_id']}

    def batch_order(self, orders: list):
        '''
        批量下单
        @param orders: 订单列表
        @return:
        '''
        param = {
            'account_id': self.account_id,
            'orders': orders
        }
        result = self._post(self.api_order_batch, param)
        return result and [{'cl_ord_id': o['cl_ord_id']} for o in result if 'cl_ord_id' in o]

    def cancal_order(self, ids: list):
        '''
        撤单委托
        @param ids: 订单号列表
        @return:
        '''
        param = {
            'account_id': self.account_id,
            'orders': [{'cl_ord_id': id} for id in ids]
        }
        return self._post(self.api_cancel, param)

    def cancel_all(self):
        '''
        全部撤单
        @return:
        '''
        return self._post(self.api_cancel_all, {'account_id': self.account_id})

    def close_all(self):
        '''
        全部平仓
        @return:
        '''
        return self._post(self.api_close_all, {'account_id': self.account_id})

    def account_sync(self):
        '''
        账户数据同步
        @return:
        '''
        return self._post(self.api_account_sync, {'account_id': self.account_id})
