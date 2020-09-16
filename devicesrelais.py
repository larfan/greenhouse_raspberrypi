try:
    import RPi.GPIO as GPIO
except:
    pass
import time
'''
all try statements only are for using program on main deb machine
'''

RELAIS_GPIO_pump=6
RELAIS_GPIO_lighbulb=13
RELAIS_GPIO_fan=19
RELAIS_GPIO_growlights=26
relaydevicelist=[RELAIS_GPIO_pump,RELAIS_GPIO_fan,RELAIS_GPIO_growlights,RELAIS_GPIO_lighbulb]

try:
    GPIO.setmode(GPIO.BCM) # normal Gpio numbers, not pin numbers
    GPIO.setup(RELAIS_GPIO_pump, GPIO.OUT) # GPIO Modus zuweisen
    GPIO.setup(RELAIS_GPIO_lighbulb, GPIO.OUT) # GPIO Modus zuweisen
    GPIO.setup(RELAIS_GPIO_fan, GPIO.OUT) # GPIO Modus zuweisen
    GPIO.setup(RELAIS_GPIO_growlights, GPIO.OUT) # GPIO Modus zuweisen
    for device in relaydevicelist:          #set Gpios to high, as to close relays
        GPIO.output(device,GPIO.HIGH)

except:
    pass

def relais(widgidx,bool):
    try:
        if widgidx<=3:
            if bool==True:
                print('Geraet ein')
                GPIO.output(relaydevicelist[widgidx], GPIO.LOW)
            else:
                print('geraet aus')
                GPIO.output(relaydevicelist[widgidx], GPIO.HIGH)
    except:
        pass

def cleanclose():
    try:                                                                        #try only is for using program on main deb machine
       

        GPIO.output(relaydevicelist, GPIO.LOW)
        GPIO.cleanup()
        print('CLEAN CLOSE!')
    except:
        pass