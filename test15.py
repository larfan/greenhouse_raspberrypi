from tkinter import *
from devicesrelais import relais, cleanclose
from BME280_new import readBME280All
from datetime import datetime
import MCP3008
import time, random, operator, copy, traceback


#starting/ideal values for measuring constants
l3=[1010,20,350,24,20]        #soilhumidity, co2, lightintensity, temp, humidity
l4=[1010,20,350,24,20] 
intervall=[5,2,20,1,2]

#opening file for logging purposes
file1=open("logfile.txt","a")
file1.write('\n\n\nCOMPLETE NEW START\n')

class measuring:
    def __init__(self):
        pass
                          


    def simulation(self,use,measurand,op,element):       #use= if environment simulation or for simulating input devices
        self.ops={'+':operator.add,'-':operator.sub}    #op= + or -
        if use=='simulation':                           #direction =for input devices if higher or lower
                                                        #measurand tells which of list should be specifically altered
            '''leave this here for testing purposes, when sensors aren't connected
            #general environment simulation  
            for ind, decrease in enumerate(l3[:2]):
                l3[ind]=decrease-1
            '''
            #CO2-concentration simulation
            #l3[1]=l3[1]-1
            #lightintensity simulation
            #l3[2]+=random.uniform(-2,2)

            #no simulation needed anymore
            self.BMP280()
            self.soilhumidity()
            self.lightintensity()

        elif element[4][1] is None:             #way of blocking simulated correction while powering on device
            self.incr=1                             
            l3[measurand]=self.ops[op](l3[measurand],self.incr)

    def checkintervall(self,measurand,index,element):
        
         #no correction-simulation needed anymore
        self.BMP280()
        self.soilhumidity()
        self.lightintensity()

        self.check=l3[measurand]-l4[measurand]
    
        if abs(self.check) >=intervall[index]:
            if self.check < 0:                           #<0 measruand too low
                if index ==3 and type(element) is list:         #very bad way of making heatingelment behave like growlights. in the sense of them running in the bg
                    element[4][0]=True
                return 'low'
            elif self.check >0:                            #>0 measurand too high
                
                return 'high'
        else:
            return True
    #sensoren
    def BMP280(self):
        try:
            temperature,pressure,humidity = readBME280All()
            l3[3]=temperature
            l3[4]=humidity
        except OSError:
            print('BMP280 scheint nicht verbunden')
            pass
    def soilhumidity(self):
        l3[0]=MCP3008.analogue(0)
    
    def lightintensity(self):
        l3[2]=MCP3008.analogue(1)

values=measuring()



class guioflabels:
    def __init__(self):          #__init__ erlaubt es beim callen der class, argumente mitzugeben, zb window(unten), als master; diese werden dann dort verarbeitet  
                                        #__init__ is used to set things up
       

        #predefining variables for the first run, before measuring
        self.useddevice=None
        
        #index of l3,widget,dictionary:{devices,connection,operator}, intervall, [skip correction,skipt simulated-correction], time-dependentlist:[x/h,t/24h,t/am stueck,[von-bis nicht],[if less than n times triggered,ontime duration,possible index of measurand that uses same device,which device to use(high/low) ]]
        #you can inhibit the use of devices, by simply setting the path to None.
        self.ll=[[0,6,{'high':[1,False,'-'],'low':[0,False,'+']},2,[None,True],[10,None,10,[0,6],[10,10,None,'low']]],         #soilhumidity
                    [1,7,{'high':[None,None,'-'],'low':[1,False,'+']},2,[None,None],[10,None,10,None,None]],           #co2
                    [2,8,{'high':[None,None,'-'],'low':[2,False,'+']},2,[True,True],[None,5*3600,None,[0,6],None]],   #lightintensity
                    [3,9,{'high':[1,False,'-'],'low':[3,False,'+']},2,[None,True],[None,None,30,None,[10,30,1,'high']]],#temperature
                    [4,10,{'high':[None,None,'-'],'low':[None,None,'+']},2,[True,True],None],                          #humidity
        
        
        ]
        self.count=0
        
        #memory for how often devices were used
        self.memory=[[0,0,0,None,None],          #[x/h,t/24h,t/am stueck, startingtime, remember if this was already counted,remember hour for time based devices]
                    [0,0,0,None,None],
                    [0,0,0,None,None],
                    [0,None,0,None,None],
                    [None,None,None,None,None],
                    [None,None,None,None,None]
                    ]

        #set starting times for memory for 1st run
        self.now=datetime.now()
        self.start=int(datetime.now().strftime('%H'))         #self.start=int(datetime.now().strftime('%H'))

        self.startday=int(self.now.strftime('%d'))
        
         
        #set devices to off in 1st run      
        for i in range(4):
            
            self.relay(i,None)
            
        
        
        
        self.programloop()              #call function 'automatically' here
    
            
    def programloop(self):
        try:  

            time.sleep(5)            
            #make temp copy of self.ll
            self.li=copy.deepcopy(self.ll)          #deepcopy kann eigentlich keine tkinter objects kopieren, deshalb sind in der self.ll liste nur indexe fuer die self.l5 liste, die die objekte enthaelt
                                                    #honestly I don't remember why a copy of self.ll is needed. Seems to work without it, however further investigation needed
                 
                
            

            for idx,element in enumerate(self.li):
                
                
                
                #set hour for the whole time of correcting this device
                self.hour=int(datetime.now().strftime('%H'))       #get string with current hour
                #set self.memory[4] as True, to register the use of devices
                self.memory[idx][4]=True
                #checks if device shouldn't be turned on in certain time frame                        
                if self.checktime(element,idx,'timeframe')=='continue':
                    continue


                for self.data in self.onecheckintervallinstance(element,idx):           #this replaces while values.checkintervall(element[0],idx,element)!=True loop 
                    #just for testing
                    print(element[0],': ',self.data)

                    print(l3)
                    ###du willst hier was einbauen dass bei True kein error vorkommt
                    self.direction=element[2][values.checkintervall(element[0],idx,element)]        #long expression just returns high/low dictionary, as to not have millions of loops 
                    self.relay(self.direction[0],True)                            #color devices, both relay and changeconnection, have a way of ignoring the argument when its None

                    
                    if element[4][0]==None and self.direction[0]!= None:                 #this guarantees that certain measurands don't get corrected at all, or only partially(like only raising the value)
                        self.useddevice=self.direction[0]                               #placing the used device variable here, guarantees, only really the last 'used' devices gets marked
                        self.memory[idx][3]=datetime.now()                       
                        self.timelog(element,idx,'x/h')                              #register general use of device one time
                        values.simulation('',element[0],self.direction[2],element)
                        if idx==3:                                          #turn off heating element, similar to growlight this has to be done once here in while loop and then one time in else down below
                            self.relay(element[2]['low'][0],None)  
                    else:                                                   #goes into this when the measurand can't be changed in one or even two directions
                        self.timelog(element,idx,'normallogging')           #NEEDS to be outside if None, as to also add the running time of light, if lightintenisty now exceeds the upper limit
                        if self.direction[0]!= None:                        #it enters this loop, if it actually got a device to power up, in case of i.e lightintenistity too high, it doesn't
                            self.timelog(element,idx,'x/h')                      #register general use of device one time
                            self.memory[idx][3]=datetime.now()              #startingtime always needs to be after timelog, otherwise you measure the wrong way around
                        else:                                               #measurand hasn't got a device to power up
                            self.resetmemory('atthetime',idx,element)

                        if values.checkintervall(element[0],idx,'')=='high':       #turn off low device because measurand is too high, and you can't change it, i.e. lightintensity 
                            self.relay(element[2]['low'][0],None)     #note to self: this is all very convoluted-->Think carefully before changing sth
                        break
                    
                    #correcting intervall
                    time.sleep(1)

                    #add small increments of 'normally' used device, basically adds the 1000 ms from above
                    self.timelog(element,idx,'normallogging')
                    
                    #exit if t/atthetime is exceeded    (contains bascially most code from the else below)
                    if element[5] is not None:              #only for the time sensitive
                        if self.memory[idx][2] and element[5][2] is not None:               #needed to not cause errors when there is no atthetime function needed for measurand
                            if self.memory[idx][2]>=element[5][2]:                          #NOTE: Measurands with simulation-correction:None, never need to enter the followinng code, because the devices are intended to run in the background. Checking t/atthetime doesn't make sense for them
                                print('The',element[5][2],'seconds of allowed uptime, has been reached here.')
                                #set device time of powered up device to 0
                                self.resetmemory('atthetime',idx,element)
                                #set to no connection
                                #turning off used device
                                self.relay(self.useddevice,None)        
                                self.useddevice=None
                                break
                    
                    #testing
                    print(l3)
                else:
                    #timelogging
                    self.timelog(element,idx,'normallogging')

                    #set device time of powered up device to 0
                    self.resetmemory('atthetime',idx,element)
                
                    #turning off devices...
                    self.relay(self.useddevice,None)         #Turn off just used device
                    self.useddevice=None                           #Forget last used device
                    
                    if element[4][0]==True:                            #turn off measurand devices with no simulation, in case they are in the right intervall
                        self.relay(element[2]['high'][0],None)
                        self.relay(element[2]['low'][0],None)
                    if idx==3:                                          #turn off heating element, similar to growlight above
                            self.relay(element[2]['low'][0],None)
                            


            '''    
            modify memory
            also turn on devices that have'nt been turned on enough the last hour
            the device function is called in the resetmemory function, because it needs to be checked before the memory is deleted
            '''
            self.resetmemory('realtime',idx,element)       #this is here, because it needs acces to the element, to be able to call the checktime function in it   


            file1.write('Das ist l3 nach der Correction und vor der Simulation: '+str(l3)+'\n')
            file1.write('Das ist das gesamte MEMORY nach der Korrektion: '+str(self.memory)+'\n')
                    
            print('MEMORY:',self.memory,'\n')
            #simulation
            print('Starting with simulation!')
            for p in range(5):
                values.simulation('simulation',None,None,None)
                time.sleep(5)

            file1.write('\nStart einer neuen Runde um '+datetime.now().strftime("%H:%M:%S")+'\n')
            print('Das ist l3 nach der Simulation: '+str(l3)+'\n')
            print('Start einer neuen Runde um ',datetime.now().strftime("%H:%M:%S"))
            file1.write('Das ist l3 nach der Simulation: '+str(l3)+'\n')
        
        
            self.programloop()
        except:                           #apparently Exception is the base class of all exceptions
             
            
            file1.close()
            cleanclose()
            print('Did you cleanup?')
            print(traceback.format_exc())           #seems to print good traceback
            

    def onecheckintervallinstance(self,element,index):        #this function is called a generator
        while True:                             #python 3.8 offers := feature, this block of code isn't required anymore
            self.data=values.checkintervall(element[0],index,element)      #https://stackoverflow.com/questions/19767891/python-assign-value-to-variable-during-condition-in-while-loop/19767980
            if self.data == True:
                break
            yield self.data


    def relay(self, widgidx, bool):          #simply changes bg color  of widg, depending on bool
        if widgidx != None:                       #this guarantees no coloring of unused devices; basically same loop in changeconnections
            relais(widgidx,bool)

    
    
    def resetmemory(self,argument,index,element):
        if argument=='realtime':
            if self.startday!=int(datetime.now().strftime('%d')):   #reset day memory
                self.memory[0][1]=0
                self.memory[1][1]=0
                self.memory[2][1]=0
                self.startday=int(datetime.now().strftime('%d'))


            if self.start!=int(datetime.now().strftime('%H')):      #reset hour memory
                file1.write('Reset of hourly memory at: '+datetime.now().strftime("%H:%M:%S")+'!\n')
                self.checktime(self.ll[0],0,'time-devices') 
                self.checktime(self.ll[3],3,'time-devices') 

                self.memory[0][0]=0
                self.memory[1][0]=0
                self.memory[2][0]=0
                self.memory[3][0]=0

                self.start=int(datetime.now().strftime('%H'))

      
        if argument=='atthetime':
            
            self.memory[index][2]=0
            

    def timelog(self,element,index,argument):
        if element[5]!=None:                        #check if logging times is even necessary
            if self.memory[index][3] is not None:   #check if it hasn't been already added/the function been called
                self.endingtime=datetime.now()
                self.timedelta=self.endingtime-self.memory[index][3]
                self.seconds=self.timedelta.total_seconds()
                if argument =='normallogging':             
                    #logs  t/24h
                    if self.memory[index][1] is not None:   #needed to not cause errors if logging this is not required     
                        self.memory[index][1]+=self.seconds
                        self.memory[index][3]=None
                        self.checktime(element,index,'t/24h')   #logs at the end of device cycle(mostly when it's finally turned off), if daily uptime has been exceeded
                    #logs t/atthetime
                    if self.memory[index][2] is not None:       #needed to not cause errors if logging this is not required
                        self.memory[index][2]+=self.seconds     #this sits here, in this loop, because it also only needs real device-on times added to it
            if argument =='x/h':                 #logs how often device is turned on, because of this measurand/h
                if self.memory[index][4] is not None and self.memory[index][0] is not None: #last part needed to not cause errors if logging this is not required
                    self.memory[index][0]+=1
                    self.memory[index][4]=None   
                    #check if limit has been exceeded
                    self.checktime(element,index,'x/h')

    def checktime(self,element,index,argument):
        if argument=='x/h':                     #goes here only 1 time, because when it's called in timelog(argument=x/h) above, self memory[index][4] gets set to None, which means that the use of the device has been counted 
            if element[5] is not None:          #checks if measurand correction should even be affected by time
                if element[5][0] is not None:
                    if self.memory[index][0]>=element[5][0]:
                        print('Limit of',element[5][0],'times powering this device per hour, has been exceeded')
                        file1.write('Limit of '+str(element[5][0])+' times powering this device per hour, has been exceeded!\n')
        
        if argument=='t/24h':
            if element[5] is not None:          #checks if measurand correction should even be affected by time
                if element[5][1] is not None:
                    if self.memory[index][1]>=element[5][1]:
                        print('The ',element[5][1],'seconds, of allowed daily uptime for this device, has been exceeded')
                        file1.write('The '+str(element[5][1])+' seconds, of allowed daily uptime for this device, has been exceeded!\n')
        #checks if device shouldn't be turned on in certain time frame
        if argument=='timeframe':
            if element[5] is not None:           #checks if measurand correction should be affected by time
                    if element[5][3] is not None:
                        if element[5][3][0]<element[5][3][1]:
                            if self.hour >=element[5][3][0] and self.hour <= element[5][3][1]:
                                print('Currently in the forbidden hours!')
                                file1.write('Currently in the forbidden hours!\n')
                                return 'continue'                                        #jumps to next iteration in for loop
                            else:
                                print('Measurand is not in the forbidden hours rn.')
                                pass
                        else:
                            if self.hour >=element[5][3][0] or self.hour <= element[5][3][1]:       #difference to if in upper if loop is the or instead of and
                                print('Currently in the forbidden hours!')
                                file1.write('Currently in the forbidden hours!\n')
                                return 'continue'                                         #jumps to next iteration in for loop
                            else:
                                print('Measurand is not in the forbidden hours rn.')
                                pass   
        '''   
        checks if turning on certain devices, after one hour, if x/h is <certain value(element[5][4][0) is required
        should alway be initiated by measurand 'using' the device as the last one in for loop. i.e both co2 and temp use the fan, 
        temp correction comes after co2 correction, hence the indication of ,[2,10] is only in time dependent list in self.ll in temp and not in co2
        '''
        if argument=='time-devices':                #self.start lastly gets corrected in resetmemory, which is executed after the for loop calling this function 

            if element[5] is not None:
                if element[5][4] is not None:       #this ensures the reasoning from above
                    self.totaluses=self.memory[index][0]
                    if element[5][4][2] is not None:
                        self.totaluses+=self.memory[element[5][4][2]][0]    #add uses of device, when not only used by one measurand
                        print('Das sind die kombinierten totaluses von CO2 und temp ',self.totaluses)
                    if self.totaluses<=element[5][4][0]:
                        print('This device gets turned on for ',element[5][4][1], 'seconds, to compensate for the last hour.')
                        file1.write('Turning on device for '+str(element[5][4][1])+'seconds, to compensate for the last hour.\n')

                        self.direction=element[2][element[5][4][3]]     #select device, based upon specified 'high'/'low'

                        self.relay(self.direction[0],True)                            

                        time.sleep(element[5][4][1])

                        self.relay(self.direction[0],None)            #turn off relay
           

mygui=guioflabels()               #this calls the class and sets mygui as instance; in class refered to instance with self; in o words self is mygui in this case        




                      #(https://github.com/Akuli/python-tutorial/blob/master/basics/classes.md)@ext:spadin.remote-x11-ssh