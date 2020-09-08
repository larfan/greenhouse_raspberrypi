try:
    import RPi.GPIO as GPIO
except:
    pass
import time
'''
all try statements only are for using program on main deb machine
'''
try:
    GPIO.setmode(GPIO.BCM) # normal Gpio numbers, not pin numbers
    RELAIS_1_GPIO = 17
    GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Modus zuweisen
except:
    pass
RELAIS_GPIO_pump=26
RELAIS_GPIO_fan=19
RELAIS_GPIO_growlights=13
relaydevicelist=[RELAIS_GPIO_pump,RELAIS_GPIO_fan,RELAIS_GPIO_growlights]

def relais(widgidx,bool):
    try:
        
        if bool==True:
            print('Geraet ein')
            if widgidx==0:
                GPIO.output(26, GPIO.HIGH)
        else:
            print('geraet aus')
            if widgidx==0:
                GPIO.output(26, GPIO.LOW)
    except:
        pass

def cleanclose():
    print('hi')
    try:                                                                        #try only is for using program on main deb machine
        print('Ich geh hier rein!')

        GPIO.output(26, GPIO.LOW)
        GPIO.cleanup()
        print('gehst du hier wirklich rein?')
    except:
        pass