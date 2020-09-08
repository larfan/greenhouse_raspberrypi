import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM) # normal Gpio numbers, not pin numbers
RELAIS_1_GPIO = 17
GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Modus zuweisen


def relais(widgidx,bool):
    if bool==True:
        print('Gerät ein')
        if widgidx==0:
            GPIO.output(RELAIS_1_GPIO, GPIO.HIGH)
    else:
        print('gerät aus')
        if widgidx==0:
            GPIO.output(RELAIS_1_GPIO, GPIO.LOW)