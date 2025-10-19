# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 10:31:26 2018

@author: KDK
"""

def main():

    header, title, dtime, data = crawling()    
    if len(data) <= 0:
        print('Data not found...')
        exit(0)
    
    savCSV(header, title, dtime, data)
    savJSON(header, title, dtime, data)
    savSqlLite3(data)
    
    
def crawling():
    
    from bs4 import BeautifulSoup as bs
    
    import urllib.request as ulibreq
    resp = ulibreq.urlopen('http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=4128162200')
    
    encoding = resp.info().get_content_charset(failobj="utf-8") # HTTP Header 를 기반으로 인코딩 조사
    markup = resp.read().decode(encoding) # read() 의 리턴값이 byte 배열이므로 문자열로 변환 
    
    #print('페이지내용:', text)
    
    soup = bs(markup, 'xml') # lxml XML parser. 
    # BeautifulSoup(markup, "lxml") <-- lxml's HTML parser
    header = ['일자', '시각', '온도', '날씨']
    title = soup.select('rss > channel > title')[0].text # CSS selector
    dtime = soup.select('rss > channel > pubDate')[0].text
    
    data = soup.select('rss > channel > item > description > body > data')
    return header, title, dtime, data

def savCSV(header, title, dtime, data):
    
    import csv
    # unix 계열에서는 open() 시 줄바꿈코드(CRLF)를 LF 로 자동변환
    # 자동 변환되지 않게 newline='' 로 설정 
    with open('weather.csv', 'w', newline='', encoding='cp949') as f:
    
        writer = csv.writer(f)
        # title 기록 
        writer.writerow([title])
        writer.writerow([dtime])
        writer.writerow(header)
    
        for item in data:
            
            day    = item.select('day')[0].text
            hour   = item.select('hour')[0].text
            temp   = item.select('temp')[0].text                  
            wfKor  = item.select('wfKor')[0].text
            
            writer.writerow([day, hour, temp, wfKor])        
    
    print('%s 파일이 저장되었습니다' % f.name)

def savJSON(header, title, dtime, data):
    
    import json
    
    tempList = []
    for item in data:
        
        day    = item.select('day')[0].text
        hour   = item.select('hour')[0].text
        temp   = item.select('temp')[0].text                  
        wfKor  = item.select('wfKor')[0].text
        # 데이터 리스트 + 헤더문자열을 zip 으로 병합하여 tuple 을 만든 후 dict 로 변환 
        hashmap = dict(zip(header, [day, hour, temp, wfKor]))
        tempList.append(hashmap)
        
    with open('weather.json','w', encoding='utf-8') as jf:
        json.dump(tempList, jf, ensure_ascii=False, indent=2)   
        
    print('%s 파일이 저장되었습니다' % jf.name)

def savSqlLite3(data):
    
    import sqlite3
    from datetime import datetime as dt
    
    con = sqlite3.connect('weather.db')
    cur = con.cursor()
    
    cur.execute('DROP TABLE IF EXISTS WEATHER;')
    cur.execute('CREATE TABLE WEATHER(REG_DT, DAY, HOUR, TEMP, WF_KOR);')
    
    sql = "INSERT INTO WEATHER VALUES(?, ?, ?, ?, ?);"
    now = dt.today().strftime('%y%m%d_%H%M%S')
    tempList = []
    for item in data:
        
        day    = item.select('day')[0].text
        hour   = item.select('hour')[0].text
        temp   = item.select('temp')[0].text                  
        wfKor  = item.select('wfKor')[0].text
    
        tempList.append((now, day, hour, temp, wfKor))
        
    cur.executemany(sql, tempList)
    con.commit()   
    
    cur.close()
    con.close()
    
    print('데이터베이스에 저장되었습니다')

'''
데이터베이스 조회
import sqlite3

con = sqlite3.connect('weather.db')
cur = con.cursor()
cur.execute("SELECT * FROM WEATHER;")
for row in cur:
    print(row)
'''

if __name__ == '__main__':
    main()