# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 16:19:27 2018

@author: KDK

1. URL 기본
크롤러는 웹페이지에 존재하는 하이퍼링크를 따라 돌아야 합니다
링크를 돌아다니려면 href 속성의 URL 을 추출하고 상대 URL이면 절대 URL 로 변환해야 합니다.

http :// example.com /main/index ? q=python #lead
----     ----------- ------------  -------- -----
schema   authority    path          query   flagment

2. 재실행을 고려한 데이터 설계

"""
# 대상 웹싸이트에서 PermaLink 목록 추출

def main():
    
#    basic()
    useSelenium()

def basic():    
    import requests
    import lxml.html as lx
    
    # resp = requests.get('http://www.hanbit.co.kr/store/books/new_book_list.html')
    session = requests.Session()
    resp = session.get('http://www.hanbit.co.kr/store/books/new_book_list.html')
    
    root = lx.fromstring(resp.content)
    # 상대 URL 을 절대URL 로 변환 : urljoin(base, 상대경로)
    root.make_links_absolute(resp.url) # 인자로 base 를 설정
    
    for atag in root.cssselect('.view_box .book_tit a'):
        url = atag.get('href')
        print(url, '-'+atag.text)
        # next depth page 
        dtlresp = session.get(url)
        dtlroot = lx.fromstring(dtlresp.content)
        dtlroot.make_links_absolute(dtlresp.url)
        
        for dtlatag in dtlroot.cssselect('a'):
            dtlurl = dtlatag.get('href')
            print('\t', dtlurl)

'''
웹크롤러의 분류

1. Stateful 크롤러(세션, Referer 설정 등)
2. 자바스크립트 실행 가능 크롤러 
   데이터 출력을 자바스크립트로 처리하는 웹싸이트를 크롤링하기 위함. Selenium 을 사용
   Selenium : 프로그램에서 브라우저를 조작할 수 있게 해주는 도구
3. 불특정 다수의 싸이트를 대상으로 하는 크롤러(Googlebot)
   병렬 처리를 통해 처리 속도 향상을 도모해야 함 
   
'''

'''
크롤러 만들때 고려할 것

1. 캐시를 사용
HTTP 서버는 응답에 아래처럼 캐시 관련 헤더를 붙임
Last-Modified  컨텐츠의 최종 변경일
ETag           컨텐츠의 식별자를 나타냄. 컨텐츠가 변경되면 이 값이 변경됨
Cache-Control  컨텐츠를 캐시해도 되는지 방침을 기술
Pragma         Cache-Control 과 비슷. 하위 호환성 때문에 유지
Expires        컨텐츠의 유효 기간

2. 변화에 대응하기
변화를 감지하여 관리자에게 통지해야 함
참고: 유효성 검사 라이브러리-Voluptuous
'''
def loadCache():
    
    import requests
    from cachecontrol import CacheControl
    
    session = requests.Session()
    csession = CacheControl(session)
#    처음 시도 때 캐시되어 있지 않으므로 서버에서 추출
    resp = csession.get('https://docs.python.org/3/') 
    print(resp.fromstring_cache)
#    캐시에서 가져옴
    resp = csession.get('https://docs.python.org/3/') 
    print(resp.fromstring_cache)

# 사이트 변경으로 가격 정보 추출에 문제가 생기는 것을 감지
def checkChange(price):
    
    import re
    if not re.search(r'^[0-9,]+$', price):
        raise ValueError('Invalid Price')

# 변경 감지를 메일로 전송
def sendEmail():
    
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header
    
    msg = MIMEText('메일 내용 blabla')
    
    msg['Subject'] = Header('메일제목', 'utf-8')
    msg['From'] = 'me@example.com'
    msg['To'] = 'you@example.com'
    
#    with smtplib.SMTP('localhost') as smtp:
#         smtp.send_message(msg)
#    GMail smtp 서버 사용. gmail 의 OAuth2.0 인증을 사용하지 않고 간편 인증방식
#    => 구글계정 > 로그인 및 보안 > 계정 액셋스 권한을 가진 앱 > '보안수준이 낮은 앱 허용:사용 안함' 을 활성화해야 함
    with smtplib.SMTP_SSL('smtp.gmail.com') as smtp:
        smtp.login('사용자이름', '비밀번호')
        smtp.send_message(msg)

'''
3. 웹페이지 자동 조작
: 단순 링크를 돌아다니는 무상태 크롤링이 아닌 입력 양식을 입력하는 등의 조작이 필요한 크롤링에서 사용
'''
# RoboBrowser 를 사용해 구글 검색
# 1. 구글 메인 페이지 접근
# 2. 검색 키워드 입력
# 3. 검색 버튼을 클릭
# 4. 검색 결과 확인
def handleBrowser():
    
    from robobrowser import RoboBrowser
    browser = RoboBrowser(parser='html.parser')

    browser.open('https://www.google.co.kr/')

    form = browser.get_form(action='/search')
    form['q'] = 'Python'
    browser.submit_form(form, list(form.submit_fields.values())[0])
    
    for atag in browser.select('h3 > a'):
        print(atag.get('href'))

'''
4. 자바스크립트를 이용한 페이지 스크래핑
처음 싸이트 접근시 필요한 리소스를 모두 로드하고 이후부터 자바스크립트로 운용하는
어플리케이션을 SPA(single page application)이라고 합니다
SPA 는 링크 클릭시 HTML5 API 를 활용해서 데이터를 읽어 화면에 바로 출력.
예를 들면 구글지도, 지메일 등입니다.
Selenium 은 다양한 브라우저를 자동 조작하는 도구. 웹 어플 테스트 자동화 도구 --> 스크래핑 도구로 사용
Selnium + PhantomJS 조합은 RoboBrowser 보다 다양한 장점이 있음

설치 
pip install selenium
http://phantomjs.org/download.html(윈도우용 zip 다운): 압축 해제 후 python.exe 경로에 복사

'''        
def useSelenium():
    
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    
    driver = webdriver.PhantomJS()  # 헤드리스 브라우저 객체 생성
    driver.get('https://www.google.co.kr/')
    
#    검색어를 입력
    input_element = driver.find_element_by_name('q')
    input_element.send_keys('Python') # 입력항목에 python 입력
    input_element.send_keys(Keys.RETURN) # 입력항목에 [enter] 입력
    
#    검색 결과를 캡쳐
    driver.save_screenshot('googlesearch.png')
    print(driver.page_source)
#    검색 결과 출력
    for atag in driver.find_element_by_css_selector('h3 > a'):
        print(atag.text, ':', atag.get_attribute('href'))
    
#    반응형 웹 등의 동작을 확인 시 화면 사이즈 조정 가능
    driver.set_window_size(320, 600)
    driver.save_screenshot('google-320X600.png')
'''
    화면 요소 선택 
    e = driver.find_element_by_id('id')
    e.clear()
    e.send_keys('firest')
    pwe = driver.find_element_by_id('pw')
    pwe.send_keys('aaaaa')
    form = driver.find_element_by_css_selector('input.btn_global[type=submit]')
    form.submit()
    
    자바스크립트 실행
    driver.execute_script('scroll(0, document.body.scrollHeight)')
'''
    
if __name__ == '__main__':
    main()