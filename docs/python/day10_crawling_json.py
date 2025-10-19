# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 13:30:30 2018

@author: KDK
"""

import requests as reqlib
from bs4 import BeautifulSoup as bs

def header():    
    print('고양시 도서관센터입니다')
    
def inputloginInfo():    
    userId = input('사용자 아이디를 입력해주세요:').strip()
    pwd = input('비밀번호를 입력하세요:').strip()
    return userId, pwd

def requestLogin(loginInfo):
    loginUrl = 'https://www.goyanglib.or.kr/center/ux/loginIdPwUX.asp'
    userId, pwd = loginInfo
    loginFormData = {"uid":userId, "upwd":pwd}
    session = reqlib.Session()
    #request = session.get(url, formData)
    loginResp = session.post(loginUrl, loginFormData)

    if loginResp.status_code != 200:
        raise Exception('로그인 실패')
    else:
        print('로그인 성공')
        print(loginResp.text)
        return session
    
header()
loginInfo = inputloginInfo()
session = requestLogin(loginInfo)

keyword = input('검색어를 입력하세요:').strip()

url = 'https://www.goyanglib.or.kr/center/ux/dataSearch_imsi.asp'
formData = {"a_q":keyword, "a_vp":"30", "a_sort":"E", "a_lib":"MI"}

response = session.post(url, formData)        
html = response.text
print('HTML 내용:', html)

soup = bs(html, 'html.parser') 
#print('페이지 내용:', soup)
'''
titleEmts = soup.select('#div_content > div.post-title > div.title-subject > div') # CSS selector
cntnEmts = soup.select('#div_content > div.post.box > div.post-content > div.post-article.fr-view') # CSS selector

print(titleEmts[0].text)
print(cntnEmts[0].text)
'''

'''
a_qf: T
a_q: searchkeyword
a_qf1: T
a_q1: 
a_qf2: T
a_q2: 
a_rf: T
a_rq: 
a_sort: E
a_vp: 30
a_lib: MI
a_cp: 1
a_mt: 
a_loan: 
    
시립도서관 코드 
    
'''

import json
# json 문자열 --> json 객체   : loads 함수 이용 
# json 객체   --> json 문자열 : dumps 함수 이용 
# json 파일   --> json 객체   : load  함수 이용 
# json 객체   --> json 파일   : dump  함수 이용 
def parseJson():

    json_string = '''{
        "id": 1,
        "username": "Bret",
        "email": "Sincere@april.biz",
        "address": {
            "street": "Kulas Light",
            "suite": "Apt. 556",
            "city": "Gwenborough",
            "zipcode": "92998-3874"
        },
        "admin": false,
        "hobbies": null
    }'''

    json_object = json.loads(json_string)
    
    assert json_object['id'] == 1
    assert json_object['email'] == 'Sincere@april.biz'
    assert json_object['address']['zipcode'] == '92998-3874'
    assert json_object['admin'] is False
    assert json_object['hobbies'] is None
    
    json_string = json.dumps(json_object, indent=2)
    print(json_string)
    
    with open('inputfile.json') as f:
    json_object = json.load(f)
    
    with open('outputfile.json', 'w') as f:
    json.dump(json_object, f, indent=2)