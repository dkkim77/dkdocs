# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 09:11:15 2018

@author: KDK

www.wxpython.org 

Frame(Parent, -- 최상위 윈도이므로 parent 를 None 으로 설정 
       id=ID_ANY, title="", 
       pos=DefaultPosition, 
       size=DefaultSize, 
       style=DEFAULT_FRAME_STYLE, 
       name=FrameNameStr)
"""
import wx

app = wx.App()
frame = wx.Frame(None)  

frame.Show(True)
app.MainLoop()

# 윈도우 제대로 만들기 
app2 = wx.App()
frame2 = wx.Frame(None)

# 스타일 설정 
title = 'first window'
pos = wx.Point(100, 100)
size = wx.Size(600, 400)
color = wx.Colour(130,50,30, 0) 
style = wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER

frame2.SetTitle(title)
frame2.SetPosition(pos)
frame2.SetSize(size)
frame2.SetBackgroundColour(color)
frame2.SetWindowStyle(style)

'''
이벤트 핸들러
Bind(이벤트상수, 핸들러)
'''

def OnLeftDown(event):
    msg = 'x좌표:%d, y좌표:%d' % (event.x, event.y)
    wx.MessageBox(msg, "알림", wx.OK)
    
def OnKeyDown(event):
    msg = '%c 키' % event.KeyCode
    wx.MessageBox(msg, "알림", wx.OK)    

frame2.Bind(wx.EVT_LEFT_DOWN, OnLeftDown)
frame2.Bind(wx.EVT_KEY_DOWN, OnKeyDown)

frame2.Show(True)
app2.MainLoop()
