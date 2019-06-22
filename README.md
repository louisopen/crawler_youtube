## Python Crawler
爬蟲方法及工具很多,Windows的環境還是方便一些,先抓一些來測試功能及行為,同時記錄一下免得又忘了
* 本文參考 http://tw.gitbook.net/python/python_environment.html

### ./Python 及./Python/Scripts 的在Windows的環境變數最好設定在windows系統參數內
* 爬蟲在Windows 10 install Python3.6 運行
* Setup Python path in windows 在命令提示下: C>path %path%;C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python36_64\  或是在系統環境變數path 加入C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python36_64\ 

* Setup PIP path in windows 在命令提示下: C>path %path%;C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python36_64\Scripts  或是在系統環境變數path 加入C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python36_64\Scripts

### 本例debug運行時,注意有些庫文件要預先裝的
* pip install setuptools
* pip install requests
* pip install beautifulsoup4
* pip install bs4
* pip install lxml
* pip install pandas

#### 根據證劵交易TSE的資訊代碼
PythonCrawler.py never test 


#### 根據證劵交易TSE的資訊爬出 每日的三大法人買賣資訊
Stock_TWT38U.py
* r=requests.get('http://www.twse.com.tw/fund/TWT38U?response=html&date='+date, headers=headers)
* r=requests.get('http://www.twse.com.tw/fund/TWT38U?response=csv&date='+date, headers=headers)


#### 根據證劵交易TSE的資訊代碼爬出 成交股數	成交金額	開盤價	最高價	最低價	收盤價	漲跌價差	成交筆數
Stock_TWSE.py
* url_twse='http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date='+str(date)+'&stockNo='+str(stock_id)


#### 參考資訊
https://github.com/Asoul/tsec
https://github.com/nelsonchung/TaiwanStockMonitor
https://github.com/louisopen/PythonCrawler
https://louisopen.github.io