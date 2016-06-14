import RPi.GPIO as GPIO
import time

butPin = 17 # Broadcom pin 17 (P1 pin 11)

def my_callback(channel):
    print "helloeeee"
    
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(butPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(17, GPIO.RISING, callback=my_callback, bouncetime=20)



print("Here we go! Press CTRL+C to exit")
try:
    while 1:
        time.sleep(1)
        print "runin"
#        if GPIO.input(butPin):
#            print "Hello"
#        else:
#            print "Nohello"
            
except KeyboardInterrupt:
    GPIO.cleanup()




