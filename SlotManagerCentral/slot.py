#!/usr/bin/python
# -*- coding: utf-8 -*-
    
import wx
import wx.media
import time
from previous_data import *
from race import *      
import RPi.GPIO as GPIO
from colours import *

class MainMenu(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.training_b = wx.Button(self, label = "Entrenamen", pos=(200, 100))
        self.race_b = wx.Button(self, label = "Cursa", pos=(200, 200))
        self.previous_b = wx.Button(self, label = "Històric", pos=(200, 300))
        self.exit_b = wx.Button(self, label = "Surt", pos=(200, 400))

        self.training_b.Bind(wx.EVT_BUTTON, parent.onSwitchPanels)
        self.race_b.Bind(wx.EVT_BUTTON, parent.onSwitchPanels)
        self.previous_b.Bind(wx.EVT_BUTTON, parent.onSwitchPanels)
        self.exit_b.Bind(wx.EVT_BUTTON, parent.exitApp)


class ConfMenu(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        font2 = wx.Font(20, wx.MODERN, wx.NORMAL, wx.NORMAL)
        self.SetBackgroundColour(background_c)
        
        user1 = wx.StaticText(self, label="Jugador/a 1", name="name1")
        user2 = wx.StaticText(self, label="Jugador/a 2", name="name2")
        user1.SetFont(font2)
        user2.SetFont(font2)
        name = wx.StaticText(self, label="Nom", name="name")
        self.name1 = wx.TextCtrl(self, -1, "", size=(175, -1))
        self.name2 = wx.TextCtrl(self, -1, "", size=(175, -1))

        user = wx.StaticText(self, label="Username", name="user")
        self.user1 = wx.TextCtrl(self, -1, "", size=(175, -1))
        self.user2 = wx.TextCtrl(self, -1, "", size=(175, -1))
        
        info = wx.StaticText(self, label="Informació", name="info")
        self.info1 = wx.TextCtrl(self, -1, "", size=(175, 50))
        self.info2 = wx.TextCtrl(self, -1, "", size=(175, 50))

        race = wx.StaticText(self, label="Cursa", name="race")
        race.SetFont(font2)
        laps = wx.StaticText(self, label="Nº voltes", name="laps")
        self.laps = wx.TextCtrl(self, -1, "5", size=(175, -1))
        circuit = wx.StaticText(self, label="Circuit", name="circuit")
        self.circuit = wx.TextCtrl(self, -1, "", size=(175, -1))
        desc_circuit = wx.StaticText(self, label="Descripció", name="desc_circ")
        self.desc_circuit = wx.TextCtrl(self, -1, "", size=(300, 50))
        dif = wx.StaticText(self, label="Dificultat", name="dif")
        self.dif = wx.TextCtrl(self, -1, "", size=(175, -1))

        self.conf_done_b = wx.Button(self, label = "Comença cursa")
        self.conf_done_b.Bind(wx.EVT_BUTTON, parent.onSwitchPanels)

        grid = wx.GridBagSizer(vgap=10, hgap=70)
        
        grid.Add(user1, pos=(0,2), flag = wx.EXPAND | wx.ALL)
        grid.Add(user2, pos=(0,3), flag = wx.EXPAND | wx.ALL)
        grid.Add(name, pos=(1,1), flag = wx.EXPAND | wx.ALL)
        grid.Add(self.name1, pos=(1,2), flag = wx.EXPAND | wx.ALL)
        grid.Add(self.name2, pos=(1,3), flag = wx.EXPAND | wx.ALL)
        grid.Add(user, pos=(2,1), flag = wx.EXPAND | wx.ALL)
        grid.Add(self.user1, pos=(2,2), flag = wx.EXPAND | wx.ALL)
        grid.Add(self.user2, pos=(2,3), flag = wx.EXPAND | wx.ALL)
        grid.Add(info, pos=(3,1), flag = wx.EXPAND | wx.ALL)
        grid.Add(self.info1, pos=(3,2), flag = wx.EXPAND | wx.ALL)
        grid.Add(self.info2, pos=(3,3), flag = wx.EXPAND | wx.ALL)

        grid.Add(race, pos=(4,2), flag = wx.EXPAND | wx.ALL)
        grid.Add(laps, pos=(5,1), flag = wx.EXPAND | wx.ALL)
        grid.Add(self.laps, pos=(5,2), flag = wx.EXPAND | wx.ALL)
        grid.Add(circuit, pos=(6,1), flag = wx.EXPAND | wx.ALL)
        grid.Add(self.circuit, pos=(6,2), flag = wx.EXPAND | wx.ALL)
        grid.Add(desc_circuit, pos=(7,1), flag = wx.EXPAND | wx.ALL)
        grid.Add(self.desc_circuit, pos=(7,2), span=(1,2), flag = wx.EXPAND | wx.ALL)
        grid.Add(dif, pos=(8,1), flag = wx.EXPAND | wx.ALL)
        grid.Add(self.dif, pos=(8,2), flag = wx.EXPAND | wx.ALL)
        grid.Add(self.conf_done_b, pos=(9,1), span=(1,3), flag = wx.EXPAND | wx.ALL)
        
        self.SetSizer(grid)

    def get_user1(self):
        return self.name1.GetValue(), self.user1.GetValue(), self.info1.GetValue()

    def get_user2(self):
        return self.name2.GetValue(), self.user2.GetValue(), self.info2.GetValue()
    
    def get_circuit(self):
        return self.circuit.GetValue(), self.desc_circuit.GetValue(), self.dif.GetValue()
    
    def get_laps(self):
        return self.laps.GetValue()
    

    
        
class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "SLOT",size=wx.DisplaySize())#(800,600))

        self.SetBackgroundColour(background_c)
        self.main_menu = MainMenu(self)
        self.main_menu.SetBackgroundColour(background_c)
        self.race_panel = RacePanel(self)
        self.race_panel.Hide()
        self.previous_results = PreviousResults(self)
        self.previous_results.Hide()
        self.conf_menu = ConfMenu(self)
        self.conf_menu.Hide()
        
        self.back = wx.Button(self, label = "Menú principal")
        self.back.Bind(wx.EVT_BUTTON, self.onSwitchPanels)
        self.conf = wx.Button(self, label = "Configuració")
        self.conf.Bind(wx.EVT_BUTTON, self.onSwitchPanels)
        self.conf.Hide()
        self.back.Hide()

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.back, 1, wx.ALIGN_RIGHT)
        self.sizer.Add(self.conf, 1, wx.ALIGN_RIGHT)
        self.sizer.Add(self.main_menu, 10, wx.EXPAND)
        self.sizer.Add(self.race_panel, 10, wx.EXPAND)
        self.sizer.Add(self.previous_results, 10, wx.EXPAND)
        self.sizer.Add(self.conf_menu, 10, wx.EXPAND)
        self.SetSizer(self.sizer)
        
        #sound = wx.Sound("ping.wav")
        #sound.Play(wx.SOUND_ASYNC)

    def onSwitchPanels(self, event):
        if event.GetId() == self.main_menu.training_b.GetId():
            self.back.Hide()
            self.main_menu.Hide()
            self.previous_results.Hide()
            self.race_panel.Show()
            self.conf_menu.Hide()
            self.conf.Hide()
        elif event.GetId() == self.main_menu.race_b.GetId():
            self.main_menu.Hide()
            self.previous_results.Hide()
            self.race_panel.Hide()
            self.conf_menu.Show()
            self.conf.Hide()
            self.back.Show()
        elif event.GetId() == self.main_menu.previous_b.GetId():
            self.previous_results.update()
            self.main_menu.Hide()
            self.previous_results.Show()
            self.race_panel.Hide()
            self.conf_menu.Hide()
            self.conf.Hide()
            self.back.Show()
        elif event.GetId() == self.back.GetId():
            self.main_menu.Show()
            self.previous_results.Hide()
            self.race_panel.Hide()
            self.conf_menu.Hide()
            self.conf.Hide()
            self.back.Hide()
        elif event.GetId() == self.conf_menu.conf_done_b.GetId():
            self.race_panel.set_circuit(self.conf_menu.get_circuit())
            self.race_panel.set_user1(self.conf_menu.get_user1())
            self.race_panel.set_user2(self.conf_menu.get_user2())
            self.race_panel.set_laps(self.conf_menu.get_laps())
            self.main_menu.Hide()
            self.previous_results.Hide()
            self.race_panel.Show()
            self.race_panel.Layout()
            self.conf_menu.Hide()
            self.conf.Hide()
            self.back.Show()
        else:
            self.main_menu.Show()
            self.race_panel.Hide()
            self.conf.Hide()    
        self.Layout()
                
    def exitApp(self, event):
        GPIO.cleanup()
        exit(0)
        
    def updateClock(self, event):
        print self.race_panel.watch.Time()
    
    def update(self, event):
        global i
        print time.time()
        self.race_panel.pwr1.SetValue(i)
        self.race_panel.pwr2.SetValue(i)
        print "helo"


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    frame.Show()
    #frame.Maximize()
    app.MainLoop()
