#!/usr/bin/python
# -*- coding: utf-8 -*-
    
import wx
import wx.media
import time
from previous_data import *
from semaphore import Semaphore
import RPi.GPIO as GPIO
from set_pins import *
from colours import *
import btle

pwm1_value = 0

class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        pass
    
    def handleNotification(self, cHandle, data):
        global pwm1_value
        dades = int(ord(data[0])) + int((ord(data[1])<<8))
        if dades > 300:
            dades = 0
        d = 280 - dades
        d2 = d*100.0/280
        if d2 < 15:
            d2 = 0
        pwm1_value = d2
        print pwm1_value
            


#addr1 = "CC:00:AA:84:34:E0"
#addr2 = "DB:0B:C0:B1:0D:38"
addr2 ="F5:8B:DF:1F:95:B0"

interrupts = 0

def my_callback(channel):
    global interrupts
    interrupts = channel

def par11_callback(channel):
    global par11_int
    par11_int = time.time()
            
def par12_callback(channel):
    global par12_int
    par12_int = time.time()

def par21_callback(channel):
    global par21_int
    par21_int = time.time()

def par22_callback(channel):
    global par22_int
    par22_int = time.time()

def sensor1_callback(channel):
    global sensor1_int
    sensor1_int = time.time()
       
def sensor2_callback(channel):
    global sensor2_int
    sensor2_int = time.time()
       
GPIO.setmode(GPIO.BCM)

GPIO.setup(pwm1_pin, GPIO.OUT)
GPIO.setup(pwm2_pin, GPIO.OUT)

GPIO.setup(start_pin, GPIO.OUT)
GPIO.setup(win1_pin, GPIO.OUT)
GPIO.setup(win2_pin, GPIO.OUT)

GPIO.setup(sensor1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(sensor2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(partial11_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(partial12_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(partial21_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(partial22_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(led1_pin, GPIO.OUT)
GPIO.setup(led2_pin, GPIO.OUT)
GPIO.setup(led3_pin, GPIO.OUT)
GPIO.setup(led4_pin, GPIO.OUT)
GPIO.setup(led5_pin, GPIO.OUT)

GPIO.output(led1_pin, GPIO.HIGH)
GPIO.output(win2_pin, GPIO.HIGH)

GPIO.setup(25, GPIO.OUT)
outputpwm = GPIO.PWM(25,100)

outputpwm.start(100)

def enable_interrupts():
    GPIO.add_event_detect(partial11_pin, GPIO.FALLING, callback=par11_callback, bouncetime=20)
    GPIO.add_event_detect(partial12_pin, GPIO.FALLING, callback=par12_callback, bouncetime=20)
    GPIO.add_event_detect(partial21_pin, GPIO.FALLING, callback=par21_callback, bouncetime=20)
    GPIO.add_event_detect(partial22_pin, GPIO.FALLING, callback=par22_callback, bouncetime=20)
    GPIO.add_event_detect(sensor1_pin, GPIO.FALLING, callback=sensor1_callback, bouncetime=20)
    GPIO.add_event_detect(sensor2_pin, GPIO.FALLING, callback=sensor2_callback, bouncetime=20)

def disable_interrupts():
    GPIO.remove_event_detect(partial11_pin)
    GPIO.remove_event_detect(partial12_pin)
    GPIO.remove_event_detect(partial21_pin)
    GPIO.remove_event_detect(partial22_pin)
    GPIO.remove_event_detect(sensor1_pin)
    GPIO.remove_event_detect(sensor2_pin)

def disable_user1_int():
    GPIO.remove_event_detect(partial11_pin)
    GPIO.remove_event_detect(partial21_pin)
    GPIO.remove_event_detect(sensor1_pin)

def disable_user2_int():
    GPIO.remove_event_detect(partial12_pin)
    GPIO.remove_event_detect(partial22_pin)
    GPIO.remove_event_detect(sensor2_pin)


def start():
    GPIO.output(startPin, GPIO.LOW)
    time.sleep(0.3)
    GPIO.output(startPin, GPIO.HIGH)

def win1():
    GPIO.output(win1Pin, GPIO.LOW)
    time.sleep(0.3)
    GPIO.output(win1Pin, GPIO.HIGH)

def win2():
    GPIO.output(win2Pin, GPIO.LOW)
    time.sleep(0.3)
    GPIO.output(win2Pin, GPIO.HIGH)

def lap():
    GPIO.output(lapPin, GPIO.LOW)
    time.sleep(0.3)
    GPIO.output(lapPin, GPIO.HIGH)
    
def cleanup():
    GPIO.cleanup()

class UserLaps(wx.ListCtrl):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, size=(-1,100), style=wx.LC_REPORT | wx.BORDER_SUNKEN |wx.LC_SORT_ASCENDING)
        self.InsertColumn(0, "")
        self.InsertColumn(1, "Parcial 1")
        self.InsertColumn(2, "Parcial 2")
        self.InsertColumn(3, "Volta")
        self.InsertColumn(4, "Total")
        self.set_laps(5)

        self.start = 0
        self.laps = []
        self.par1 = []
        self.par2 = []
        self.par3 = []
        self.last_lap = 0

    def reset_table(self, laps):
        self.DeleteAllItems()
        self.set_laps(laps)
        
        
    def set_start(self, time):
        self.start = time
    
    def add_par1(self, time):
        pass
        #self.par1.append(time - laps[-1])

    def add_par2(self, time):
        pass
        #self.par2.append(time - laps[-1])
    
    
    def add_sensor(self, time):
        #self.par3.append(time - laps[-1])
        self.laps.append(time - self.start)
        print self.laps
    
    def reset(self):
        self.laps = []
        self.par1 = []
        self.par2 = []
        self.par3 = []
        
    def set_laps(self, laps_n):
        for i in range(laps_n):
            self.InsertStringItem(i, str(i+1))
        
    def add_partial1(self, lap, time):
        self.SetStringItem(lap-1, 1, str(time))

    def add_partial2(self, lap, time):
        self.SetStringItem(lap-1, 2, str(time)) 

    def add_lap(self, lap, time):
        lap_time = time - self.last_lap
        self.last_lap = time
        m, s = divmod(time, 60)
        t = "{0:02.0f}'{1:05.2f}".format(m, s)
        self.SetStringItem(lap-1, 4, t)

        m, s = divmod(lap_time, 60)
        t2 = "{0:02.0f}'{1:05.2f}".format(m, s)
        self.SetStringItem(lap-1, 3, t2)

    def get_laps(self):
        count = self.GetItemCount()
        laps = []
        for row in range(count):
            item = self.GetItem(itemId=row, col=3)
            t = item.GetText()
            m, s = t.split("'")
            seconds = int(m)*60 + float(s)
            laps.append(seconds)
        return laps
            
    def get_total(self):
        count = self.GetItemCount()
        total = self.GetItem(itemId=count-1, col=4)
        t = total.GetText()
        print "t ", t
        m, s = t.split("'")
        seconds = int(m)*60 + float(s)
        return seconds
            
class RacePanel(wx.Panel):

    def __init__(self, parent):

        wx.Panel.__init__(self, parent=parent)
        self.SetBackgroundColour(raceColour)
        self.bstart = wx.Button(self, label = "Comença")
        self.bstop = wx.Button(self, label = "Atura")
        self.bsave = wx.Button(self, label = "Guarda")
        self.bstop.Disable()
        self.bsave.Disable()
        self.bstart.Bind(wx.EVT_BUTTON, self.on_race_button)
        self.bsave.Bind(wx.EVT_BUTTON, self.on_race_button)
        self.bstop.Bind(wx.EVT_BUTTON, self.on_race_button)
        boxCtrl = wx.BoxSizer(wx.HORIZONTAL)
        boxCtrl.Add(self.bstart, 2, wx.ALL, 10)
        boxCtrl.Add(self.bstop,  2, wx.ALL, 10)
        boxCtrl.Add(self.bsave, 2, wx.ALL, 10)

        # Timers
        self.countdown_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_countdown, self.countdown_timer)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_race, self.timer)

        self.pwm_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.pwm_update, self.pwm_timer)
        #self.pwm_timer.Start(100)
        
        self.start_time = 0
        self.total_laps = 5
        self.laps = []
        
        font = wx.Font(14, wx.MODERN, wx.NORMAL, wx.NORMAL)
        font2 = wx.Font(20, wx.MODERN, wx.NORMAL, wx.NORMAL)

        self.winner = 0

        self.circuit = ""
        self.desc_circuit = ""
        self.dif_circuit = ""
        
        self.name1 = ""
        self.username1 = ""
        self.info1 = ""

        self.name2 = ""
        self.username2 = ""
        self.info2 = ""

        # Race interface
        self.pos1_t = wx.StaticText(self, label="{} 1".format(self.name1), name="pos1")
        self.lap1_t = wx.StaticText(self, label="Lap: 1 / {}".format(self.total_laps), name="laps1")
        self.pwr1 = wx.Gauge(self, -1, 100, size=(400,20)) 
        self.pos2_t = wx.StaticText(self, label="{} 2".format(self.name2), name="pos2")
        self.lap2_t = wx.StaticText(self, label="Lap: 1 / {}".format(self.total_laps), name="laps2")
        self.pwr2 = wx.Gauge(self, -1, 100, size=(400,20))

        self.pos1_t.SetFont(font)
        self.lap1_t.SetFont(font)
        #self.pwr1_t.SetFont(font)
        self.pos2_t.SetFont(font)
        self.lap2_t.SetFont(font)
        #self.pwr2_t.SetFont(font)
                
        self.pos1, self.pos2, self.laps1, self.laps2 = 1, 2, 1, 1
        self.par11, self.par12, self.par21, self.par22 = 0, 0, 0, 0

        self.semaphore = Semaphore(self)
        self.n_countdown = 0

        self.countdown_time = 0

        self.user1_laps = UserLaps(self)
        self.user2_laps = UserLaps(self)
        
        user1 = wx.BoxSizer(wx.VERTICAL)
        user1.Add(self.pos1_t, 1, wx.ALL, 10)
        user1.Add(self.lap1_t, 1, wx.ALL, 10)
        user1.Add(self.pwr1, 1, wx.ALL, 10)
        user1.Add(self.user1_laps, 5, wx.ALL|wx.EXPAND, 10)

        user2 = wx.BoxSizer(wx.VERTICAL)
        user2.Add(self.pos2_t, 1, wx.ALL, 10)
        user2.Add(self.lap2_t, 1, wx.ALL, 10)
        user2.Add(self.pwr2, 1, wx.ALL, 10)
        user2.Add(self.user2_laps, 5, wx.ALL|wx.EXPAND, 10)

        users = wx.BoxSizer(wx.HORIZONTAL)
        users.Add(user1, 1, wx.EXPAND, 10)
        users.Add(user2, 1, wx.EXPAND, 10)
        
        self.total_time = wx.StaticText(self, label="Time: 0:00'00.0", name="labeltime")
        self.total_time.SetFont(font2)
        self.total_time.SetBackgroundColour('white')

        mainBox = wx.BoxSizer(wx.VERTICAL)
        mainBox.Add(self.semaphore, 2, wx.EXPAND, 100)
        mainBox.Add(boxCtrl, 1, wx.EXPAND, 10)
        mainBox.Add(users, 1, wx.EXPAND, 10)
        mainBox.Add(self.total_time, 5, wx.EXPAND , 10)
        
        self.SetSizer(mainBox)

        self.ble2 = btle.Peripheral()
        self.ble2.setDelegate(MyDelegate())

        print "Connecting with peripheral2..."
        self.ble2.connect(addr2, "random")

        try:
            self.ble2.writeCharacteristic(0x22, '\x01\x00')
        except:
            print "Activating notifications 2"

        print "Connections established, notifications on!"

        
    def set_circuit(self, circuit):
        self.circuit = circuit[0]
        self.desc_circuit = circuit[1]
        self.dif_circuit = circuit[2]
        
    def set_user1(self, user):
        self.name1 = user[0]
        self.username1 = user[1]
        self.info1 = user[2]
        self.pos1_t.SetLabel("{} 1".format(self.name1))
        
    def set_user2(self, user):
        self.name2 = user[0]
        self.username2 = user[1]
        self.info2 = user[2]
        self.pos2_t.SetLabel("{} 2".format(self.name2))
        
    def set_laps(self, n):
        self.total_laps = int(n)
        self.lap1_t.SetLabel("Lap: 1 / {}".format(self.total_laps))
        self.lap2_t.SetLabel("Lap: 1 / {}".format(self.total_laps))
        self.user1_laps.reset_table(self.total_laps)
        self.user2_laps.reset_table(self.total_laps)
        
    def reset_data(self):
        self.total_time.SetLabel("Time: 0:00'00.0")
        self.pos1_t.SetLabel("{} 1".format(self.name1))
        self.lap1_t.SetLabel("Lap: 1 / {}".format(self.total_laps))
        self.pos2_t.SetLabel("{} 2".format(self.name2))
        self.lap2_t.SetLabel("Lap: 1 / {}".format(self.total_laps))
        self.user1_laps.reset_table(self.total_laps)
        self.user2_laps.reset_table(self.total_laps)
        
    def start_countdown(self):
        self.countdown_timer.Start(100)
        #self.pwm_timer.Start(107)
        
        self.semaphore.lights_off()
        self.reset_data()
        self.start_time = 0
        self.pos1, self.pos2, self.laps1, self.laps2 = 1, 2, 1, 1
        self.par11, self.par12, self.par21, self.par22 = 0, 0, 0, 0
        self.n_countdown = 0
        enable_interrupts()
        
        self.countdown_time = time.time()
 

        
    def on_countdown(self, event):
        global sensor1_int, sensor2_int
        t = time.time()
        if (t - self.countdown_time > 1):
            self.semaphore.turn_light_on(self.n_countdown)
            if self.n_countdown == 6:
                self.start_race()
                self.semaphore.lights_off()
                self.countdown_timer.Stop()
            self.n_countdown +=1
            self.countdown_time = t

        if sensor1_int != 0 and self.start_time == 0:
            self.pos1_t.SetLabel("{} sortida falsa!!".format(self.name1))
            self.semaphore.lights_on()
            self.stop_race()
            sensor1_int = 0
            
        elif sensor2_int != 0 and self.start_time == 0:
            self.pos2_t.SetLabel("{} sortida falsa!!".format(self.name2))
            self.semaphore.lights_on()
            self.stop_race()
            sensor2_int = 0
        
             
    def start_race(self):
        t = time.time()
        self.start_time = t
        self.timer.Start(25)
        self.laps = [t]
            
    def stop_race(self):
        self.timer.Stop()
        self.countdown_timer.Stop()
        disable_interrupts()
        self.start_time = 0
        self.countdown_time = 0
        
    def save_data(self):

        laps1 = self.user1_laps.get_laps()
        total1 = self.user1_laps.get_total()
        laps2 = self.user2_laps.get_laps()
        total2 = self.user2_laps.get_total()

        db = DatabaseCon('localhost', 'slot', '123123123', 'slot_db')        
        print self.name1, self.username1, self.info1
        db.add_user(self.name1, self.username1, self.info1)
        db.add_user(self.name2, self.username2, self.info2)
        db.add_circuit(self.circuit, self.desc_circuit, self.dif_circuit)
        circuit_id = db.get_circuit(self.circuit)[0][0]
        user1_id = db.get_user_from_name(self.name1)[0][0]
        user2_id = db.get_user_from_name(self.name2)[0][0]
        db.add_race(circuit_id, user1_id, user2_id, total1, total2)

        race_id = db.get_last_race()[0][0]
        
        for n in range(len(laps1)):
            db.add_lap(race_id, n+1, laps1[n], laps2[n])
        
        db.close_con()

        
    def on_race_button(self, event):
        if event.GetId() == self.bstart.GetId():
            self.bstart.Disable()
            self.bstop.Enable()
            self.bsave.Disable()
            self.start_countdown()
                    
        elif event.GetId() == self.bstop.GetId():
            self.bstart.Enable()
            self.bstop.Disable()
            self.bsave.Enable()
            self.stop_race()
            #self.semaphore.lights_off()
            
        elif event.GetId() == self.bsave.GetId():
            self.save_data()
            self.bstart.Enable()
            self.bstop.Disable()
            self.bsave.Disable()
            
            
    def update_race(self, num):

        # Total time
        t = time.time()-self.start_time
        m, s = divmod(t, 60)
        t = "Time: 0:{0:02.0f}'{1:04.1f}".format(m, s)
                        
        self.total_time.SetLabel(t)
    
        global par11_int, par12_int, par21_int, par22_int, sensor1_int, sensor2_int
        if par11_int != 0:
            self.user1.add_par1(par11_int)
            par11_int = 0

        if par12_int != 0:
            self.user2.add_par1(par12_int)
            par12_int = 0

        if par21_int != 0:
            self.user1.add_par2(par21_int)
            par21_int = 0

        if par22_int != 0:
            self.user1.add_par2(par22_int)
            par22_int = 0

        if sensor1_int != 0:
            self.user1_laps.add_lap(self.laps1, sensor1_int - self.start_time)
            sensor1_int = 0
            if self.laps1 < self.total_laps:
                self.laps1 += 1
                self.lap1_t.SetLabel("Lap {} / {}".format(self.laps1, self.total_laps))
                if self.laps1 > self.laps2:
                    self.pos1 = 1
                    self.pos2 = 2
                    self.pos1_t.SetLabel("{} 1".format(self.name1))
                    self.pos2_t.SetLabel("{} 2".format(self.name2))
            else:
                disable_user1_int()
                if self.winner == 0:
                    self.winner = 1
                    self.pos1_t.SetLabel("{} winner".format(self.name1))
                
        if sensor2_int != 0:
            self.user2_laps.add_lap(self.laps2, sensor2_int - self.start_time)
            sensor2_int = 0
            if self.laps2 < self.total_laps:
                self.laps2 += 1
                self.lap2_t.SetLabel("Lap {} / {}".format(self.laps2, self.total_laps))
                if self.laps2 > self.laps1:
                    self.pos1 = 2
                    self.pos2 = 1
                    self.pos1_t.SetLabel("{} 2".format(self.name1))
                    self.pos2_t.SetLabel("{} 1".format(self.name2))
            else:
                disable_user2_int()
                if self.winner == 0:
                    self.winner = 2
                    self.pos2_t.SetLabel("{} winner".format(self.name2))
        self.ble2.waitForNotifications(0.01)
        self.pwr1.SetValue(pwm1_value)
                    
    def pwm_update(self, num):
        self.ble2.waitForNotifications(3)
        self.pwr1.SetValue(pwm1_value)
