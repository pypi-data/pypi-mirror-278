#  -*- coding: utf-8 -*-
# @author: zhangping

import json
import datetime as dt
import numpy as np
import pandas as pd
from urllib import parse
from .utils import HttpUtil, LoggerUtil


class ApiClient():
    '''
    指标数据接口客户类
    '''

    def __init__(self, token='', host='api.shducheng.net', port=80, log_level='INFO', logs_dir='./logs', api_urls=None):
        '''
        ApiClient构造函数
        :param token: token字符串
        :param host: 接口服务地址，默认：api.shducheng.net
        :param port: 接口服务端口，默认：80
        :param log_level: 日志级别，默认：INFO
        :param api_urls: 接口地址服务路径
        :return:
        '''
        api_urls = api_urls if api_urls is not None else {
            'api_query': '/updatemonitor/dict-index/exportData',  # query
            'api_import': '/updatemonitor/dict-index/importJson',  # insert
            'api_delete': '/updatemonitor/dict-index/deleteDictIndexData',  # delete
            'api_dict': '/updatemonitor/dict-index/queryDictIndex',  # index dict
            'api_dict_list': '/updatemonitor/dict-index/queryIndexList',  # index list
            'api_msg_sms': '/sendAlert',  # send sms
            'api_msg_wx': '/dcwechat/message/sendMessage'  # send weixin
        }
        self.token = token
        self.host = 'http://' + host + ':' + str(port)
        self.api_query = self.host + api_urls['api_query']
        self.api_import = self.host + api_urls['api_import']
        self.api_delete = self.host + api_urls['api_delete']
        self.api_dict = self.host + api_urls['api_dict']
        self.api_dict_list = self.host + api_urls['api_dict_list']
        self.api_msg_sms = self.host + api_urls['api_msg_sms']
        self.api_msg_wx = self.host + api_urls['api_msg_wx']
        self.logger = LoggerUtil.get_logger(name='dqapi', level=log_level, logs_dir=logs_dir)

    def get_idx_dict(self, idx):
        '''
        获取指标信息
        :param idx: 指标id
        :return:
        '''
        if idx is None or type(idx) != int: raise Exception('指标id不可为空且为int类型')

        url = self.api_dict + f'?indexId={str(idx)}'
        self.logger.debug('request: ' + url)
        result = HttpUtil.request_post(url, None, headers={'token': self.token}, raw=False)
        result = json.loads(result.decode('utf-8'))
        self.logger.debug('result: ' + str(result))

        if 'code' not in result or result['code'] != 200:
            self.logger.error(result['msg'])
            raise Exception(result['msg'])
        self.logger.info(result['msg'])
        return result['info']

    def get_dict_list(self, source_type):
        '''
        根据类型获取指标列表
        :param source_type: 指标来源类型
        :return:
        '''
        source_type = '' if source_type is None else str(source_type)
        url = self.api_dict_list + f'?sourceType={source_type}'
        self.logger.debug('request: ' + url)
        result = HttpUtil.request_post(url, None, headers={'token': self.token}, raw=False)
        result = json.loads(result.decode('utf-8'))
        self.logger.debug('result: ' + str(result))

        if 'code' not in result or result['code'] != 200:
            self.logger.error(result['msg'])
            raise Exception(result['msg'])
        self.logger.info(result['msg'])
        return pd.DataFrame(result['info'])

    def get_series(self, ids, start_dt='2015-01-01', end_dt=None, column='id'):
        '''
        获取日期序列
        :param ids: 指标id或id列表
        :param start_dt: 开始日期，默认：2015年1月1日
        :param end_dt: 截至日期，默认：当日日期
        :param column: 列名字段：id/name
        :return:
        '''
        # ids = list(set(ids)) if type(ids) == list else [ids]
        if column not in ['id', 'name']: raise Exception('列名仅支持id和name')
        if ids is None or len(ids) == 0: raise Exception('指标id列表不可为空')

        ids = ids if type(ids) == list else [int(ids)]
        params = {'rows': [{'id': _id} for _id in ids],
                  'startDate': start_dt if start_dt is not None else '2021-01-01',
                  'endDate': end_dt if end_dt is not None else dt.datetime.today().strftime('%Y-%m-%d')}

        self.logger.debug('request: ' + self.api_query)
        self.logger.debug('params: ' + str(params))
        result = HttpUtil.request_post(self.api_query, params, headers={'token': self.token}, raw=True)
        result = json.loads(result.decode('utf-8'))
        self.logger.debug('result: ' + str(result))
        if 'code' not in result or result['code'] != 200:
            self.logger.error(result['msg'])
            raise Exception(result['msg'])

        df = pd.DataFrame({'date': []})
        for i, idx in enumerate(result['info']):
            _df = pd.DataFrame(
                {'date': [dt.datetime(1970, 1, 1) + dt.timedelta(seconds=a[0] / 1000) for a in idx['data']],
                 idx[column]: [a[1] for a in idx['data']]}
            )
            if _df is None or len(_df) == 0:
                df[idx[column]] = np.nan
            else:
                df = pd.merge(df, _df, on='date', how='outer')

        df = df.set_index(['date']).sort_index()
        return df.groupby(df.index).last()

    def formula_series(self, formulas, start_dt='2015-01-01', end_dt=None):
        '''
        获取日期序列
        :param formulas: 公式或公式列表
        :param start_dt: 开始日期，默认：2015年1月1日
        :param end_dt: 截至日期，默认：当日日期
        :return:
        '''
        if formulas is None or len(formulas) == 0: raise Exception('formulas参数不可为空')
        formulas = formulas if type(formulas) == list else [str(formulas)]
        params = {'rows': [{'sourceType': 'formula', 'sourceCode': f} for f in formulas],
                  'startDate': start_dt if start_dt is not None else '2021-01-01',
                  'endDate': end_dt if end_dt is not None else dt.datetime.today().strftime('%Y-%m-%d')}

        self.logger.debug('request: ' + self.api_query)
        self.logger.debug('params: ' + str(params))
        result = HttpUtil.request_post(self.api_query, params, headers={'token': self.token}, raw=True)
        result = json.loads(result.decode('utf-8'))
        self.logger.debug('result: ' + str(result))
        if 'code' not in result or result['code'] != 200:
            self.logger.error(result['msg'])
            raise Exception(result['msg'])

        df = pd.DataFrame({'date': []})
        for i, idx in enumerate(result['info']):
            _df = pd.DataFrame({'date': [dt.datetime.utcfromtimestamp(a[0] / 1000) for a in idx['data']],
                                formulas[i]: [a[1] for a in idx['data']]})
            if _df is None or len(_df) == 0:
                df[formulas[i]] = np.nan
            else:
                df = pd.merge(df, _df, on='date', how='outer')

        df = df.set_index(['date']).sort_index()
        return df.groupby(df.index).last()

    def save_series(self, items, overwrite=False):
        '''
        保存指标数据
        :param items: 指标数据列表，格式：[{'idx': 100001, 'date': datetime.datetime.today(), 'value': 100.05 }]
        :param overwrite: 是否覆盖已有相同日期值，默认False
        :return:
        '''
        if items is None or len(items) == 0:
            return False

        rows_dict = {}
        for item in items:
            if item['idx'] is None or item['date'] is None or item['value'] is None: continue
            if item['idx'] not in rows_dict: rows_dict[item['idx']] = []
            rows = rows_dict[item['idx']]
            rows.append([item['date'].strftime('%Y-%m-%d'), item['value']])

        series = [{'ID': key, 'ROWS': rows_dict[key]} for key in rows_dict]
        params = {'jsonObj': series, 'importPara': 0 if overwrite else 1}

        self.logger.debug('request: ' + self.api_import)
        self.logger.debug('params: ' + str(params))
        result = HttpUtil.request_post(self.api_import, params, headers={'token': self.token}, raw=False)
        result = json.loads(result.decode('utf-8'))
        self.logger.debug('result: ' + str(result))

        if 'code' not in result or result['code'] != 200:
            self.logger.error(result['msg'])
            raise Exception(result['msg'])

        self.logger.info(result['msg'])
        return True

    def del_series(self, ids, start_dt='1900-01-01', end_dt='2999-01-01'):
        '''
        删除指标数据
        :param ids: 指标id或id列表
        :param start_dt: 开始日期，默认：1900-01-01
        :param end_dt: 截至日期，默认：2999-01-01
        :return:
        '''
        ids = ids if type(ids) == list else [int(ids)]
        for idx in ids:
            url = self.api_delete + f'?indexId={str(idx)}&startDate={start_dt}&endDate={end_dt}'
            # params = {'indexId': idx_id, 'startDate': start_dt, 'endDate': end_dt}
            self.logger.debug('request: ' + url)
            result = HttpUtil.request_post(url, None, headers={'token': self.token}, raw=False)
            result = json.loads(result.decode('utf-8'))
            self.logger.debug('result: ' + str(result))
            if 'code' not in result or result['code'] != 200:
                self.logger.error(result['msg'])
                raise Exception(result['msg'])
            self.logger.info(result['msg'])
        return True

    def send_sms(self, number, text, name=''):
        '''
        发送短信息
        :param number: 手机号码
        :param text: 消息文本
        :param name: 通知名称
        :return:
        '''
        params = {'phoneNum': number, 'msg': name, 'status': text}
        url = self.api_msg_sms + '?' + str(parse.urlencode(params).encode('utf-8'), 'utf-8')
        result = HttpUtil.request_post(url, None, headers={'token': self.token})
        self.logger.info('result: ' + str(json.loads(result.decode('utf-8'))))

    def send_wx(self, email, text):
        '''
        发送微信信息(企业微信)
        :param email: 邮箱账号
        :param text: 消息文本
        :return:
        '''
        params = {'userName': email, 'msg': text}
        url = self.api_msg_wx + '?' + str(parse.urlencode(params).encode('utf-8'), 'utf-8')
        result = HttpUtil.request_post(url, None, headers={'token': self.token})
        self.logger.info('result: ' + str(json.loads(result.decode('utf-8'))))
