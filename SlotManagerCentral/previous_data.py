#!/usr/bin/python
# -*- coding: utf-8 -*-
    
import wx
import wx.lib.mixins.listctrl as listmix
from db_connection import *
from races import *
from users import *
from colours import *

class PreviousResults(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.SetBackgroundColour(background_c)
        db = DatabaseCon('localhost', 'slot', '123123123', 'slot_db')        
        nb = wx.Notebook(self)
        self.users = Users(nb, db)
        self.races = Races(nb, db)
        nb.AddPage(self.users, "Usuaris")
        nb.AddPage(self.races, "Curses")
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        #sizer.Add(button1, 1, wx.ALIGN_RIGHT)
        sizer.Add(nb, 10, wx.EXPAND)
        self.SetSizer(sizer)

    def update(self):
        self.users.update()
        self.races.update()
