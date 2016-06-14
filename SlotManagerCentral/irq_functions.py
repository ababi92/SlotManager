#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from previous_data import *
import RPi.GPIO as GPIO

pwm1_pin = 2
pwm2_pin = 3
start_pin = 17
win1_pin = 19
win2_pin = 26

sensor1_pin = 20
sensor2_pin = 21

partial11_pin = 5
partial12_pin = 6
partial21_pin = 13
partial22_pin = 19

led1_pin = 23
led2_pin = 24
led3_pin = 25
led4_pin = 8
led5_pin = 7

par11_int = 0
par12_int = 0
par21_int = 0
par22_int = 0
sensor1_int = 0
sensor2_int = 0

interrupts = 0

green = (0x1f, 0xda, 0x9a)
yellow = (0xf5, 0xea, 0xcd)
raceColour = yellow

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
