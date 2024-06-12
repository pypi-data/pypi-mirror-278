# -*- coding: utf-8 -*-
"""
@Time ： 2022/11/3
@Auth ： zhangping
"""
import os, traceback, schedule
import pandas as pd
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from .sim_trader import Order, SimTrader

order = lambda s, p, v: {'symbol': s, 'order_type': Order.PriceMarket, 'order_style': Order.ByTargetVolume,
                         'position_side': p, 'target_volume': v}


class FileOrder(FileSystemEventHandler):
    def __init__(self, trade_api: SimTrader, file_path: str, file_ext: str = '.csv', timers: list = None,
                 init_run: bool = True, merge_flag=False):
        '''
        @param trade_api: 交易/仿真交易API
        @param file_path: 文件目录
        @param file_ext: 文件后缀，默认：.csv
        @param timers: 定时运行时间(文件变动外的定时执行)，如：['09:15', '21:15']
        @param init_run: 是否初始运行，默认：True
        @param merge_flag: 是否监控变化每次合并所有文件，默认：False
        '''
        FileSystemEventHandler.__init__(self)
        self.file_path = file_path
        self.file_ext = file_ext
        self.init_run = init_run
        self.merge_flag = merge_flag
        self.timers = timers
        self.cache = dict()
        self.trade_api = trade_api
        self.logger = trade_api.logger

    def on_modified(self, event):
        self.logger.info("file modified: {0}".format(event.src_path))
        if not event.is_directory: self.process_file(event.src_path)

    def on_deleted(self, event):
        self.logger.info("file deleted: {0}".format(event.src_path))
        if event.src_path in self.cache.keys(): self.cache.pop(event.src_path)

    def process_file(self, path):
        if not path.lower().endswith(self.file_ext.lower()): return
        self.logger.info("process file: {0}".format(path))
        try:
            b = open(path).read()
            if b == self.cache.get(path): return

            self.cache[path] = b
            if self.merge_flag:
                self.scan_files()
            else:
                df: pd.DataFrame = pd.read_csv(path)
                df = df.dropna(axis=0)[[df.columns[0], df.columns[1], df.columns[-1]]]
                self.process_order(df)
        except Exception as e:
            self.logger.error(traceback.format_exc())

    def scan_files(self):
        self.logger.info('scan folder:', self.file_path)
        df: pd.DataFrame = None
        for f in os.listdir(self.file_path):
            path = os.path.join(self.file_path, f)
            if os.path.isdir(path): continue
            _df = pd.read_csv(path)
            _df = _df.dropna(axis=0)[[_df.columns[0], _df.columns[1], _df.columns[-1]]]
            df = _df if df is None else df.append(_df)
        df = df.groupby([df.columns[0], df.columns[1]]).sum().reset_index()
        self.process_order(df)

    def process_order(self, df: pd.DataFrame):
        try:
            if df is None or len(df) == 0: return
            self.logger.info('\n' + str(df))

            orders = []
            for i, r in df.iterrows():
                # long_short = [Order.PositionLong, Order.PositionShort] if r[df.columns[2]] == 0 else [
                #     Order.PositionShort if r[df.columns[2]] < 0 else Order.PositionLong]
                # orders += [order(f'{r[df.columns[0]]}.{r[df.columns[1]]}', side, abs(r[df.columns[2]])) for side in
                #            long_short]
                s, n = f'{r[df.columns[0]]}.{r[df.columns[1]]}', r[df.columns[2]]
                orders.append(order(s, Order.PositionLong, n > 0 and n or 0))
                orders.append(order(s, Order.PositionShort, n < 0 and -n or 0))
            # print(orders)
            orders = self.trade_api.batch_order(orders)
            self.logger.info('\n' + str(pd.DataFrame(orders)))
        except Exception as e:
            self.logger.error(traceback.format_exc())

    def start(self):

        observer = Observer()
        observer.schedule(self, self.file_path)
        observer.start()

        if self.init_run: self.scan_files()

        if self.timers and len(self.timers) > 0:
            [schedule.every().day.at(t).do(self.scan_files) for t in self.timers]
            while True: schedule.run_pending()

        observer.join()
