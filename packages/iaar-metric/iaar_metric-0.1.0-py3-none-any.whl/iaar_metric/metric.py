#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/6/12 下午7:34
@Author  : Gie
@File    : metric.py
@Desc    : 
"""
import json
import os
import socket
import traceback

from scrapy import signals
import datetime
from threading import Timer


# scrapy extension 打点记录当前爬虫运行情况

def get_one_min_later(step=1):
    """
     获取下一分钟的整点时间戳 按整点存进去
    :param step:
    :return:
    """
    dt = datetime.datetime.now()
    td = datetime.timedelta(
        days=0,
        seconds=dt.second,
        microseconds=dt.microsecond,
        milliseconds=0,
        minutes=-step,
        hours=0,
        weeks=0
    )
    new_dt = dt - td
    timestamp = int(new_dt.timestamp())  # 对于 python 3 可以直接使用 timestamp 获取时间戳
    return timestamp


def get_localhost_ip():
    """
    利用 UDP 协议来实现的，生成一个UDP包，把自己的 IP 放如到 UDP 协议头中，然后从UDP包中获取本机的IP。
    这个方法并不会真实的向外部发包，所以用抓包工具是看不到的
    :return:
    """
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        if s:
            s.close()
    return ip


def is_all_heart_beat_zero(doc):
    # 以下值全部是 0, 为无效心跳，不保存。
    # 只要有一个值不是 0 ，is_all_zero 就是 False， 会继续入库。
    for item in ['success_count', 'error_count', 'page_per_second', 'parse_fail_count', 'total_count']:
        # 有效时间内的心跳才算数
        if doc.get(item) != 0:
            return False
    return True


#  精简配置 读取spider自带redis server   读写入库
class MetricExtension:
    def __init__(self, crawler, interval):
        self.exit_code = False
        self.interval = interval
        self.crawler = crawler
        # 用来查redis的key的长度
        self.stats_keys = set()
        self.cur_d = {
            'total_count': 0,  # item
            'success_count': 0,  # success
            'max_reached': 0,  # err_ abandonded by self
            'log_err_count': 0,  # err_ logerror
            'res_ignore_count': 0,  # err_ingonre
            'error_count_byhand': 0,  # err_ byhand
            'abandoned_url': 0,  # 并发——手动丢弃
            'dupefilter': 0,  # 并发——   dup by redis
            'parse_fail_count': 0,  # 解析失败的量
            'mongo_success': 0,  # mong入库
            'retry_by_hand': 0,  # retry_by_hand
        }
        self.pid = os.getpid()

    @classmethod
    def from_crawler(cls, crawler):

        interval = crawler.settings.get('INTERVAL', 60)
        ext = cls(crawler, interval)
        crawler.signals.connect(ext.engine_started, signal=signals.engine_started)
        crawler.signals.connect(ext.engine_stopped, signal=signals.engine_stopped)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        return ext

    def engine_started(self):
        Timer(self.interval, self.handle_stat).start()

    def engine_stopped(self):
        self.exit_code = True

    def spider_closed(self, spider, reason):
        self.exit_code = True

    def spider_opened(self, spider):
        pass

    def handle_stat(self):
        tracker = self.crawler.spider.tracker
        identity = get_localhost_ip() + '_' + str(self.pid)

        stats = self.crawler.stats.get_stats()
        fail_count = 0
        for k, v in stats.items():
            if k.startswith('spider_exceptions'):
                fail_count += v
        d = {
            'total_count': stats.get('item_scraped_count', 0),  # item
            'success_count': stats.get('response_received_count', 0),  # success
            'max_reached': stats.get('retry/max_reached', 0),  # err_ abandoned by self
            'log_err_count': stats.get('log_count/ERROR', 0),  # err_ logerror
            'res_ignore_count': stats.get('httperror/response_ignored_count', 0),  # err_ignore
            'error_count_byhand': stats.get('error_count_byhand', 0),  # err_by_hand
            'retry_by_hand': stats.get('retry_by_hand', 0),  # err_ by_hand
            'abandoned_url': stats.get('abandoned_url', 0),  # 并发——手动丢弃
            'dupefilter': stats.get('dupefilter/filtered', 0),  # 并发——dup by redis
            'mongo_success': stats.get('mongo_success', 0),  # 入库数量
            'parse_fail_count': fail_count,  # 入库数量
        }

        for key in self.cur_d:
            d[key], self.cur_d[key] = d[key] - self.cur_d[key], d[key]

        redis_d = {
            "identity": identity,
            'name': self.crawler.spider.name,
            'type': 1,
            'state': 1,
            'total_count': d['mongo_success'],  # 入库成功量
            'success_count': d['success_count'],  # 下载成功数量
            'parse_fail_count': d['parse_fail_count'],  #
            'left_count': self.crawler.spider.count_size(self.crawler.spider.redis_key),  # 队列剩余量
            'error_count': d['max_reached'] + d['log_err_count'] + d['res_ignore_count'] + d['error_count_byhand'] + d['retry_by_hand'],  # 失败数量 （反爬以及非200 ）
            'page_per_second': d['abandoned_url'] + d['dupefilter'],  # dup_url url重复的数量
            "timestamp": get_one_min_later(),
        }

        is_all_zero = is_all_heart_beat_zero(redis_d)
        # 心跳值(关键指标)全部都是 0 是没有意义的，不推送
        if not is_all_zero:
            try:
                self.crawler.spider.check_redis()
                self.crawler.spider.server.lpush('metric:' + self.crawler.spider.name, json.dumps(redis_d, ensure_ascii=False))
                self.stats_keys.update(stats.keys())
            except Exception as e:
                self.crawler.spider.logger.error(f'persist_heart_beat_err, spider: {self.crawler.spider.name}, '
                                                 f'identity: {identity}, msg: {traceback.format_exc()}').tracker(tracker)
            finally:
                if not self.exit_code:
                    Timer(self.interval, self.handle_stat).start()
        else:
            Timer(self.interval, self.handle_stat).start()
            self.crawler.spider.logger.warning(f'all_heart_beat_zero, spider: {self.crawler.spider.name}, '
                                               f'identity: {identity}, check your spider').tracker(tracker)

