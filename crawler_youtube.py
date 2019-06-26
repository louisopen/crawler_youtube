

import os
import requests
from bs4 import BeautifulSoup

url="https://www.youtube.com/feed/trending/"

request=requests.get(url)
content=request.content
soup=BeautifulSoup(content,"html.parser")

container = soup.select("h3 a")
"""
res = os.popen('arp -a').readlines()
for I in res:
 if "00:00:5e:00:xx:xx" in I:
   print(I[:20])
"""
file = open('result.text','w')
for item in container:
    if item:
        #print(type(item))
        value = item.get_text()
        print(value)
        file.write(value+'\n')
    
file.close()