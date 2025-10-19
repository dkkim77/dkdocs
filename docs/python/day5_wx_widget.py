# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 11:21:33 2018

@author: KDK

www.wxpython.org 

"""

import wx
import winsound as ws

app = wx.App()
frame = wx.Frame(None)

# 스타일 설정 
title = 'first window'
pos = wx.Point(100, 100)
size = wx.Size(600, 400)
color = wx.Colour(130,50,30, 0) 
style = wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER

frame.SetTitle(title)
frame.SetPosition(pos)
frame.SetSize(size)
frame.SetBackgroundColour(color)
frame.SetWindowStyle(style)
# 버튼 사용 알아보기 
btnDo = wx.Button(frame, id=1, label="Do") 
btnRe = wx.Button(frame, id=2, label="Re")
btnMi = wx.Button(frame, id=3, label="Mi")
btnPa = wx.Button(frame, id=4, label="Pa")
btnSol = wx.Button(frame, id=5, label="Sol")

def OnClick(event):

    print('event ID:', event.GetId())
    
    scale = {'do':261,'re':293,'mi':329,'pa':349,'sol':391,'ra':440,'si':493}
    btnid = event.GetId()
    if btnid == 1:
        ws.Beep(scale['do'],1000)
    elif btnid == 2:
        ws.Beep(scale['re'],1000)
    elif btnid == 3:
        ws.Beep(scale['mi'],1000)
    elif btnid == 4:
        ws.Beep(scale['pa'],1000)
    elif btnid == 5:
        ws.Beep(scale['sol'],1000)
    else:
        pass
    
btnDo.Bind(wx.EVT_BUTTON, OnClick) 
btnRe.Bind(wx.EVT_BUTTON, OnClick)
btnMi.Bind(wx.EVT_BUTTON, OnClick)
btnPa.Bind(wx.EVT_BUTTON, OnClick)
btnSol.Bind(wx.EVT_BUTTON, OnClick)

#   배치관리자 사이저 
#   Add(window, proportion=0, flag=0,border=0, userData=None)
#   proportion : 컴포넌트들의 크기 비율, 0이면 본래 크기만큼만 차지
box = wx.BoxSizer(wx.HORIZONTAL)
box.Add(btnDo, proportion=1)
box.Add(btnRe, proportion=1)
box.Add(btnMi, proportion=1)
box.Add(btnPa, proportion=1)
box.Add(btnSol, proportion=1)

frame.SetSizer(box)

frame.Show(True)
app.MainLoop()