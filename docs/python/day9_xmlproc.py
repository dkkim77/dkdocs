# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 15:26:21 2018

@author: KDK

파이썬이 지원하는 xml 라이브러리
-------------------------------------------
 패키지                           이름공간
-------------------------------------------
1)Fast XML parsing using Expat    xml.parsers.expat
2)DOM API                         xml.dom
3)SAX                             xml.sax
4)The ElementTree XML API         xml.etree.ElementTree
------------------------------------------- 

1) DOM 의 1/6 처리속도, 1/5 메모리 사용. 문서의 유효성을 검사하지 않음
2) DOM 은 모든 객체를 메모리에 저장. XML 접근 시 바로 접근 가능
3) SAX 는 문서 파싱할 때 구성요소를 발견할 때마다 이벤트를 발생시켜 처리
   DOM 과 달리 XML 문서 내용을 변경할 수 없고(readonly) 문서의 처음에서 아래로 파싱
   사용자는 요소를 처리하기 위한 함수를 생성하여 SAX 이벤트 핸들러에 연결

"""
import sys
# xml 파싱
xml = '''<?xml version="1.0"?>
         <book ISBN="1111">
             <title>Loving Python</title>
         </book>
'''
# expat
print('==============  expat ==============')
import xml.parsers.expat as ept
def selement(name, attrs):
    print('start element:','name:',name, 'attrs:',attrs)
    
def chardata(data):
    print('Character:', repr(data))

parser = ept.ParserCreate()
parser.StartElementHandler = selement
parser.CharacterDataHandler = chardata

parser.Parse(xml)

# minidom
print('==============  minidom ==============')
import xml.dom.minidom as mdom
# xml문자열 파싱
doc = mdom.parseString(xml)
print(doc.toxml())

# xml 파일 파싱
try:
    xmlfile = open('')
    print('파일 있을 경우')
    doc = mdom.parse(xmlfile)
    print(doc.toxml())
except IOError:
    print('IOError예외:',sys.exc_info())
except Exception:
    print('Exception예외:',sys.exc_info())
finally:    
    print('finally 수행')
    doc.unlink() # minidom 메모리 해제    
    
# The ElementTree XML API 는 Element 의 생성,변경, 검색 등을 쉽게 처리
# 생성 : ElementTree.Element(tag[,attr][,**extra]), 
#        ElementTree.SubElement(parent,tag[,attr][,**extra])
import xml.etree.ElementTree as et

searchkeyword = 'Python'
retlist = []
try:
    tree = et.fromstring(xml)    
    books = tree.getiterator("book") # 모든 하위 엘리먼트 리턴 
    for book in books:
        title = book.find("title")  # find(path) : path 에 매칭되는 엘리먼트 리턴. None 리턴
        if title.text.find(searchkeyword) >= 0:
            retlist.append((book.attrib["ISBN"], title.text))
except Exception:
    print(sys.exc_info())

print('검색결과:',retlist)