import RPi.GPIO as GPIO
import time


pwm1_pin = 2
pwm2_pin = 3
start_pin = 17
win1_pin = 19
win2_pin = 26

sensor1_pin = 10
sensor2_pin = 9

parcial11_pin = 5
parcial12_pin = 6
parcial21_pin = 13
parcial22_pin = 19

led1_pin = 23
led2_pin = 24
led3_pin = 25
led4_pin = 8
led5_pin = 7

GPIO.setmode(GPIO.BCM)

GPIO.setup(pwm1_pin, GPIO.OUT)
GPIO.setup(pwm2_pin, GPIO.OUT)

GPIO.setup(start_pin, GPIO.OUT)
GPIO.setup(win1_pin, GPIO.OUT)
GPIO.setup(win2_pin, GPIO.OUT)

GPIO.setup(sensor1_pin, GPIO.IN, pull_up_dowm=GPIO.PUD_UP)
GPIO.setup(sensor2_pin, GPIO.IN, pull_up_dowm=GPIO.PUD_UP)

GPIO.setup(parcial11_pin, GPIO.IN, pull_up_dowm=GPIO.PUD_UP)
GPIO.setup(parcial12_pin, GPIO.IN, pull_up_dowm=GPIO.PUD_UP)
GPIO.setup(parcial21_pin, GPIO.IN, pull_up_dowm=GPIO.PUD_UP)
GPIO.setup(parcial22_pin, GPIO.IN, pull_up_dowm=GPIO.PUD_UP)

GPIO.setup(led1_pin, GPIO.OUT)
GPIO.setup(led2_pin, GPIO.OUT)
GPIO.setup(led3_pin, GPIO.OUT)
GPIO.setup(led4_pin, GPIO.OUT)
GPIO.setup(led5_pin, GPIO.OUT)

GPIO.output(led1_pin, GPIO.HIGH)
GPIO.output(win2_pin, GPIO.HIGH)

GPIO.setup(butPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(sensor1, GPIO.FALLING, callback=my_callback, bouncetime=20)

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)
outputpwm = GPIO.PWM(25,100)

outputpwm.start(100)

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
