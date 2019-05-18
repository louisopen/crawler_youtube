#!/usr/bin/env python3
#coding=utf-8
#三大法人買賣超(2018以後欄位)
# Install in Windows shell
# pip install pandas
# pip install scrapy
import json
import time
from datetime import datetime
import pandas as pd
import scrapy

TWSE_URL = 'http://www.twse.com.tw/fund/T86?response=json&date={y}{m:02d}{d:02d}&selectType=ALL'
TPEX_URL = 'http://www.tpex.org.tw/web/stock/3insti/daily_trade/3itrade_hedge_result.php?l=zh-tw&se=AL&t=D&d={y}/{m:02d}/{d:02d}'

columns = ["_id",
           "外陸資買進",
           "外陸資賣出",
           "外陸資買賣超",
           "外資自營商買進",
           "外資自營商賣出",
           "外資自營商買賣超",
           "投信買進",
           "投信賣出",
           "投信買賣超",
           "自營商買進",
           "自營商賣出",
           "自營商買賣超",
           "自營商買進避險",
           "自營商賣出避險",
           "自營商買賣超避險",
           "三大法人買賣超"]


def parse_info(d, m):
    _id = m['date'] + '_' + d[0]
    if m['市場別'] == '上市':
        d.pop(11)
        d = d[2:]
        d = [int(x.replace(',', '')) / 1000 for x in d]
    else:
        del d[8:11]
        d = d[2:-1]
        d = [int(x.replace(',', '')) / 1000 for x in d]

    return dict(zip(columns, [_id, *d]))


class StockDaySpider(scrapy.Spider):
    name = 'stock_investor'

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'CONCURRENT_REQUESTS': 1,
        'MONGODB_COLLECTION': 'stock_day',
        'MONGODB_ITEM_CACHE': 1,
        'MONGODB_HAS_ID_FIELD': True,
        'COOKIES_ENABLED': False
    }

    def __init__(self, beginDate=None, endDate=None, *args, **kwargs):
        super(StockDaySpider, self).__init__(beginDate=beginDate, endDate=endDate, *args, **kwargs)

    def start_requests(self):
        if self.beginDate and self.endDate:
            start = self.beginDate
            end = self.endDate
        else:
            date = datetime.today().strftime("%Y-%m-%d")
            start = date
            end = date

        for date in pd.date_range(start, end)[::-1]:
            today = '{}/{:02d}/{:02d}'.format(date.year, date.month, date.day)
            y = date.year
            m = date.month
            d = date.day

            url = TWSE_URL.format(y=y, m=m, d=d)
            time.sleep(8)
            yield scrapy.Request(url, meta={'date': today, '市場別': '上市'})
            y = y - 1911
            url = TPEX_URL.format(y=y, m=m, d=d)
            yield scrapy.Request(url, meta={'date': today, '市場別': '上櫃'})

    def parse(self, response):
        m = response.meta
        json_data = json.loads(response.text)

        if m['市場別'] == '上市':
            try:
                data = json_data['data']
                for d in data:
                    yield parse_info(d, m)
            except KeyError:
                pass
        else:
            try:
                data = json_data['aaData']
                for d in data:
                    yield parse_info(d, m)
            except KeyError:
                pass

