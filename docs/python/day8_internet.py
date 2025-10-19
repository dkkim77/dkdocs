# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 15:16:37 2018

@author: KDK
"""

import webbrowser as wb
import urllib.parse as ulibp

# %ED%8C%8C%EC%9D%B4%EC%8D%AC
url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query='
keyword = input('검색어:')

urlencodestr = ulibp.quote(keyword) # quote : URL Encoding
print(urlencodestr)

wb.open_new_tab(url+urlencodestr)

# OpenAPI
pass

# web page crawling 
import urllib.request as ulibreq
resp = ulibreq.urlopen('http://www.hanbit.co.kr/store/books/full_book_list.html')

encoding = resp.info().get_content_charset(failobj="utf-8") # HTTP Header 를 기반으로 인코딩 조사
text = resp.read().decode(encoding) # read() 의 리턴값이 byte 배열이므로 문자열로 변환 

print('페이지내용:', text)