# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 16:36:32 2018

@author: KDK

precondition : install lxml XML parser
usage>>> pip install lxml
"""

# 기상청 RSS Scrapping
from bs4 import BeautifulSoup as bs

import urllib.request as ulibreq
resp = ulibreq.urlopen('http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=4128162200')

encoding = resp.info().get_content_charset(failobj="utf-8") # HTTP Header 를 기반으로 인코딩 조사
markup = resp.read().decode(encoding) # read() 의 리턴값이 byte 배열이므로 문자열로 변환 

#print('페이지내용:', text)

soup = bs(markup, 'xml') # lxml XML parser. 
# BeautifulSoup(markup, "lxml") <-- lxml's HTML parser

title = soup.select('rss > channel > title')[0].text # CSS selector
dtime = soup.select('rss > channel > pubDate')[0].text

print(title, dtime)

data = soup.select('rss > channel > item > description > body > data')
                   
for item in data:
    
    day    = item.select('day')[0].text
    hour   = item.select('hour')[0].text
    temp   = item.select('temp')[0].text                  
    wfKor  = item.select('wfKor')[0].text
    
    print(day, hour, temp, wfKor)
