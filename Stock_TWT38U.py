#!/usr/bin/env python3
#coding=utf-8
#Install in Windows shell
# pip install requests
# pip install 
#外資及陸資買賣超彙總表
from datetime import datetime, timedelta, date
import time
import requests
import pandas as pd
from io import StringIO     #使用內存
import os
import random
import os.path

#取得當前工作路徑加存檔路徑
#workpath = os.path.split(os.path.realpath(__file__))[0] + '\Stocks'   #windows path

def get_buy(date):    
    try:
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        headers={"User-Agent":user_agent}
        #r=requests.get('http://www.twse.com.tw/fund/TWT38U?response=html&date='+date, headers=headers)
        r=requests.get('http://www.twse.com.tw/fund/TWT38U?response=csv&date='+date, headers=headers)
        if len(r.text)<5000:
            print(date+' holiday')
            time.sleep(0.5)
            return None
        else:
            print(date)     #normally
    except:
        print(date +' error')
        time.sleep(0.5)
        return None
 
    r = r.text.replace('=', '')
    r = r.replace('*', ' ')
    lines = r.split(',\r\n" ",')
    k=lines[0].split('\r\n,,,')  #第一筆資料有日期 要消除掉
    lines[0]=k[1]
    k=lines[0].split(',,,\r\n"",')  
    lines[0]=k[1]
    m=lines[-1].split(',\r\n')
    lines[-1]=m[0]   #最後一筆資料有一堆說明
    #lines
    my_list=[]
    for line in lines:
        if len(line.split('","')) == 11:
            line="".join(line.split())      #有太多空格導致後面要設置index出錯
            my_list.append(line) 
            s='\n'.join(my_list)

    df = pd.read_csv(StringIO(s))
    df = df.astype(str)
    #df = df.set_index(['證券代號'])    #索引開始欄位
    df = df.apply(lambda s: s.str.replace(',', ''))  #原本的數字有逗號
    df.sort_index(inplace=True)  #依照號碼順序排列
    df=df.iloc[:,:4]
    df.to_pickle(date)   
    print(df)
    print('sussess')
    time.sleep(3 + random.uniform(1,3))

def daterange(start, end):
    for n in range(int ((end - start).days)+1):
        yield start + timedelta(n)
'''
def datelist(beginDate, endDate): 
    return [datetime.strftime(x,'%Y%m%d') for x in list(pd.date_range(start=beginDate, end=endDate))] 
'''

start_dt = date(2019, 5, 13)
end_dt = date(2019, 5, 15)
for dt in daterange(start_dt, end_dt):
    #week =dt.weekday()
    #if week < 5: #星期一是0 ~6  故小於五等於weekday 星期一~日
        dt=dt.strftime('%Y%m%d.csv')    #當地日期時間...格式
        if not os.path.isfile(dt):  #如果檔案尚未被讀取
            get_buy(dt)
        else:
            print(dt+' had ')



