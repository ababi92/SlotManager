#!/usr/bin/python
# -*- coding: utf-8 -*-
    
import wx
import wx.media
import time
from previous_data import *
import RPi.GPIO as GPIO
from colours import *

class Semaphore(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.SetBackgroundColour(semaphore_c)

        size_sem = (80, 80)
        
        light = wx.Image("./red.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        grey = wx.Image("./grey.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        
        self.light1 = wx.StaticBitmap(self, -1, light, pos=(50, 0), size=size_sem)
        self.light2 = wx.StaticBitmap(self, -1, light, pos=(200, 0), size=size_sem)
        self.light3 = wx.StaticBitmap(self, -1, light, pos=(350, 0), size=size_sem)
        self.light4 = wx.StaticBitmap(self, -1, light, pos=(500, 0), size=size_sem)
        self.light5 = wx.StaticBitmap(self, -1, light, pos=(650, 0), size=size_sem)
               
        self.grey1 = wx.StaticBitmap(self, -1, grey, pos=(50, 0), size=size_sem)
        self.grey2 = wx.StaticBitmap(self, -1, grey, pos=(200, 0), size=size_sem)
        self.grey3 = wx.StaticBitmap(self, -1, grey, pos=(350, 0), size=size_sem)
        self.grey4 = wx.StaticBitmap(self, -1, grey, pos=(500, 0), size=size_sem)
        self.grey5 = wx.StaticBitmap(self, -1, grey, pos=(650, 0), size=size_sem)

    def lights_on(self):
        self.light1.Show()
        self.light2.Show()
        self.light3.Show()
        self.light4.Show()
        self.light5.Show()
        self.grey1.Hide()
        self.grey2.Hide()
        self.grey3.Hide()
        self.grey4.Hide()
        self.grey5.Hide()

        
    def lights_off(self):

        self.light1.Hide()
        self.light2.Hide()
        self.light3.Hide()
        self.light4.Hide()
        self.light5.Hide()

        self.grey1.Show()
        self.grey2.Show()
        self.grey3.Show()
        self.grey4.Show()
        self.grey5.Show()
        
                
        
    def countdown(self):
        self.n += 1

    def turn_light_on(self, light_n):
        if light_n == 1:
            self.light1.Show()
            self.grey1.Hide()
        elif light_n == 2:
            self.light2.Show()
            self.grey2.Hide()
        elif light_n == 3:
            self.light3.Show()
            self.grey3.Hide()
        elif light_n == 4:
            self.light4.Show()
            self.grey4.Hide()
        elif light_n == 5:
            self.light5.Show()
            self.grey5.Hide()
      
        
        
