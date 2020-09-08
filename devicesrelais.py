import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM) # normal Gpio numbers, not pin numbers

def relais(widgidx,bool):
    if bool==True:
        print('Gerät ein')
    else:
        print('gerät aus')