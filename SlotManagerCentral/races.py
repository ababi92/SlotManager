#!/usr/bin/python
# -*- coding: utf-8 -*-
    
import wx
import wx.lib.mixins.listctrl as listmix
from db_connection import *

class RaceData(wx.ListCtrl):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, size=(-1,100), style=wx.LC_REPORT | wx.BORDER_SUNKEN |wx.LC_SORT_ASCENDING)

    def update(self, laps):
        self.ClearAll()
        self.InsertColumn(0, "")
        self.InsertStringItem(0, "U1")
        self.InsertStringItem(1, "U2")                        
        print laps
        index = 1
        for i in laps:
            self.InsertColumn(index, str(i[2])) 
            self.SetStringItem(0, index, str(i[3]))
            self.SetStringItem(1, index, str(i[4]))
            index += 1
        
class Races(wx.Panel):
    def __init__(self, parent, db):
        wx.Panel.__init__(self, parent)
        self.index = 0
        self.list_ctrl = wx.ListCtrl(self, size=(-1,100), style=wx.LC_REPORT | wx.BORDER_SUNKEN |wx.LC_SORT_ASCENDING)
        self.list_ctrl.InsertColumn(0, 'Id')
        self.list_ctrl.InsertColumn(1, 'Nom')
        self.list_ctrl.InsertColumn(2, 'Username')
                        
        self.db = db
        items2, i = {}, 0
        for user in self.db.get_races():
            self.list_ctrl.InsertStringItem(i, str(user[0]))
            self.list_ctrl.SetStringItem(i, 1, str(user[1]))
            self.list_ctrl.SetStringItem(i, 2, str(user[2]))
            i +=1
            
    def update(self):
        self.list_ctrl.DeleteAllItems()
        items2, i = {}, 0
        for user in self.db.get_races():
            self.list_ctrl.InsertStringItem(i, str(user[0]))
            self.list_ctrl.SetStringItem(i, 1, str(user[1]))
            self.list_ctrl.SetStringItem(i, 2, str(user[2]))
            i +=1
                
        self.race_info = RaceData(self)

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.showRace, self.list_ctrl)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.list_ctrl, 5, wx.ALL|wx.EXPAND, 5)
        sizer.Add(self.race_info, 2, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(sizer)

    def GetListCtrl(self):
        return self.list_ctrl

    def OnColClick(self, event):
        print "column clicked"
        event.Skip()

    def showRace(self, event):
        event.Skip()
        race_id = event.GetItem().GetText()
        laps = self.db.get_race_laps(race_id)
        
        self.race_info.update(laps)
