#!/usr/bin/python
# -*- coding: utf-8 -*-
    
import wx
import wx.lib.mixins.listctrl as listmix
from db_connection import *
from colours import *

class UserData(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        font = wx.Font(13, wx.MODERN, wx.NORMAL, wx.NORMAL)
        self.titol = wx.StaticText(self, -1, "Informació usuari/a")
        self.name = wx.StaticText(self, -1, "Nom:")
        self.info = wx.StaticText(self, -1, "Descripció:")
        self.wins = wx.StaticText(self, -1, "Victòries:")
        self.rank = wx.StaticText(self, -1, "Rànquing:")
        
        self.SetBackgroundColour(user_info_c)
        
        self.titol.SetFont(font)
        #self.name.SetFont(font)
        #self.info.SetFont(font)
        #self.wins.SetFont(font)
        #self.rank.SetFont(font)
        

        data = wx.BoxSizer(wx.VERTICAL)
        data.Add(self.titol, 0, wx.ALL, 5)
        data.Add(self.name, 0, wx.ALL, 5)
        data.Add(self.info, 0, wx.ALL, 5)
        data.Add(self.wins, 0, wx.ALL, 5)
        data.Add(self.rank, 0, wx.ALL, 5)

        self.SetSizer(data)


    def update(self, name, info, wins, rank):
        self.titol.SetLabel("Informació usuari/a")
        self.name.SetLabel("Nom: {}".format(name))
        self.info.SetLabel("Descripció: {}".format(info))
        self.wins.SetLabel("Victòries: {}".format(wins))
        self.rank.SetLabel("Rànquing: {} / {}".format(rank[0], rank[1]))



class Users(wx.Panel, listmix.ColumnSorterMixin):
    def __init__(self, parent, db):
        wx.Panel.__init__(self, parent)
        self.index = 0
        self.list_ctrl = wx.ListCtrl(self, style=wx.LC_REPORT | wx.BORDER_SUNKEN | wx.LC_SORT_ASCENDING | wx.LC_HRULES)
        self.list_ctrl.InsertColumn(0, 'Id', format = wx.LIST_FORMAT_CENTER, width=60)
        self.list_ctrl.InsertColumn(1, 'Nom', format = wx.LIST_FORMAT_CENTER, width=200)
        self.list_ctrl.InsertColumn(2, 'Username', format = wx.LIST_FORMAT_CENTER, width=200)
        self.list_ctrl.SetBackgroundColour(users_list_c)
        self.db = db

        items2, i = {}, 0
        for user in self.db.get_users():
            items2[i] = (str(user[0]), str(user[1]), str(user[2]))
            i += 1
        
        index = 0
        for key, data in items2.items():
            self.list_ctrl.InsertStringItem(index, data[0])
            self.list_ctrl.SetStringItem(index, 1, data[1])
            self.list_ctrl.SetStringItem(index, 2, data[2])
            self.list_ctrl.SetItemData(index, key)
            index += 1
            
        self.itemDataMap = items2
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.showUser, self.list_ctrl)
        listmix.ColumnSorterMixin.__init__(self, 4)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick, self.list_ctrl)
        
        self.user_info = UserData(self)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.list_ctrl, 5, wx.ALL|wx.EXPAND, 5)
        sizer.Add(self.user_info, 2, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(sizer)
        
    def update(self):
        self.list_ctrl.DeleteAllItems()
        items2, i = {}, 0
        for user in self.db.get_users():
            items2[i] = (str(user[0]), str(user[1]), str(user[2]))
            i += 1
        print "ITEMS ",items2
        index = 0
        for key, data in items2.items():
            self.list_ctrl.InsertStringItem(index, data[0])
            self.list_ctrl.SetStringItem(index, 1, data[1])
            self.list_ctrl.SetStringItem(index, 2, data[2])
            self.list_ctrl.SetItemData(index, key)
            index += 1
            
        self.itemDataMap = items2
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.showUser, self.list_ctrl)
        listmix.ColumnSorterMixin.__init__(self, 4)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick, self.list_ctrl)
        
    def GetListCtrl(self):
        return self.list_ctrl

    def OnColClick(self, event):
        print "column clicked"
        event.Skip()

    def showUser(self, event):
        event.Skip()
        user_id = event.GetItem().GetText()
        data = self.db.get_user_data(user_id)[0]
        rank = self.db.get_user_rank(user_id)
        self.user_info.update(data[1], data[3], data[4], rank) 
        
        
        """
        self.db.get_user_win_count(user_id)
        self.db.get_user_races(user_id)
        self.db.get_user_races(user_id)
        """
