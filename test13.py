from tkinter import *
from devicesrelais import relais, cleanclose
from BME280_new import readBME280All
from datetime import datetime
import time, random, operator, copy


#starting/ideal values for measuring constants
l3=[20,20,20,20,20]        #soilhumidity, co2, lightintensity, temp, humidity
l4=[20,20,20,20,20] 
intervall=[2,2,2,2,2]

#opening file for logging purposes
file1=open("logfile.txt","a")
file1.write('\n\n\nCOMPLETE NEW START\n')

class measuring:
    def __init__(self):
        pass
                          


    def simulation(self,use,measurand,op):       #use= if environment simulation or for simulating input devices
        self.ops={'+':operator.add,'-':operator.sub}    #op= + or -
        if use=='simulation':                           #direction =for input devices if higher or lower
                                                        #measurand tells which of list should be specifically altered
            #general environment simulation
            for ind, decrease in enumerate(l3[:2]):
                l3[ind]=decrease-1
               
            #lightintensity simulation
            l3[2]+=random.uniform(-2,2)

            #no simulation needed anymore
            self.BMP280()

        else:
            self.incr=1                             
            l3[measurand]=self.ops[op](l3[measurand],self.incr)

    def checkintervall(self,measurand):
        '''
        Derweil wird in Checkintervall noch nicht neu gemessen, da ja noch keine Gerät installiert sind
        '''
        #if measurand==4 or 3:
        #    self.BMP280()
        self.check=l3[measurand]-l4[measurand]
        if abs(self.check) >=2:
            if self.check < 0:                           #<0 measruand too low
                return 'low'
            elif self.check >0:                            #>0 measurand too high
                return 'high'
        else:
            return True

    def BMP280(self):
        try:
            temperature,pressure,humidity = readBME280All()
            l3[3]=temperature
            l3[4]=humidity
        except OSError:
            print('BMP280 scheint nicht verbunden')
            pass


values=measuring()



class guioflabels:
    def __init__(self,master):          #__init__ erlaubt es beim callen der class, argumente mitzugeben, zb window(unten), als master; diese werden dann dort verarbeitet  
                                        #__init__ is used to set things up
                                        #das master ist hier glaube ich einfach, damit man nicht mit global definieren muss
        self.master=master


        self.l1=[  ['        :---->',   #Connectionslist
                    '       :      ',   #0-2=time
                    '       :      ',   #3-5=soilhumidity,CO2concentration,lightintensity
                    '       :      ',   #6=temperature
                    '       :      ',
                    '------:       ',],
                    
                    ['              ',   
                    '        :---->',   
                    '       :      ',   
                    '       :      ',   
                    '       :      ',
                    '------:       ',],

                    ['              ',   
                    '              ',   
                    '        :---->',   
                    '       :      ',   
                    '       :      ',
                    '------:       ',],

                    ['------------->',   
                    '              ',   
                    '              ',   
                    '              ',   
                    '              ',
                    '              ',],

                    ['              ',   
                    '------------->',   
                    '              ',   
                    '              ',   
                    '              ',
                    '              ',],

                    ['              ',   
                    '              ',   
                    '------------->',   
                    '              ',   
                    '              ',
                    '              ',],

                    ['              ',   
                    '              ',   
                    '              ',   
                    '------------->',   
                    '              ',
                    '              ',],

                    ['------:        ',   #soilhumidity-->fan
                    '        :---->',   
                    '              ',   
                    '              ',   
                    '              ',
                    '              ',],

                    ['              ',      #temperature-->fan  
                    '         :---->',   
                    '       :      ',   
                    '------:       ',   
                    '              ',
                    '              ',],

                    ['              ',      #10th list is only here for default mode
                    '              ',
                    '              ',
                    '              ',
                    '              ',
                    '              ',],
                    
                     ]
        

        self.frame1=LabelFrame(master, text='INPUTS')
        self.frame1.grid(row=0,column=2)

        self.frame2=LabelFrame(master, text='OUTPUTS')
        self.frame2.grid(row=0,column=0)

        self.frame3=LabelFrame(master, width=1000,text=' ',bd=0)
        self.frame3.grid(row=0,column=1)

        self.input1=Label(self.frame1,text='waterpump')
        self.input1.grid()

        self.input2=Label(self.frame1,text='fan')
        self.input2.grid()

        self.input3=Label(self.frame1, text='growlights')
        self.input3.grid()

        self.input4=Label(self.frame1, text='heater-element')
        self.input4.grid()

        self.input5=Label(self.frame1, text='')
        self.input5.grid()

        self.input6=Label(self.frame1, text='')
        self.input6.grid()


        self.output1=Label(self.frame2, text='soil-humidity')
        self.output1.grid()

        self.output2=Label(self.frame2, text='CO2-concentration')
        self.output2.grid()

        self.output3=Label(self.frame2, text='lightintensity')
        self.output3.grid()

        self.output4=Label(self.frame2, text='temperature')
        self.output4.grid()

        self.output5=Label(self.frame2, text='humidity')
        self.output5.grid()

        self.output6=Label(self.frame2, text='time',relief=GROOVE)
        self.output6.grid()

        
      

        


        self.l2=[]                              #man sollte eher listen erstellen, als indirekt 'Daten' in den Variablen zu speichern
        for i,z in enumerate(self.l1[0],0):     #das waere in diesem Fall self.st1, self.st2, self.st3 usw., wobei 3 eine Art von Daten waere
                                                #this loop creates all tkinter connection labels
            self.l2.append(Label(self.frame3,text=z,width=10))
            self.l2[i].grid()   
      
        

       

        #predefining variables for the first run, before measuring
        self.useddevice=None
        
        #index of l3,widget,dictionary:{devices,connection,operator}, intervall, skip simulation-correction, time-dependentlist:[x/h,t/24h,t/am stueck,[von-bis nicht],[if less than n times triggered,ontime duration,possible index of measurand that uses same device ]]
        #you can inhibit the use of devices, by simply setting the path to None.
        self.ll=[[0,6,{'high':[1,self.l1[7],'-'],'low':[0,self.l1[3],'+']},2,None,[10,None,10,[0,6],[2,10,None]]],         #soilhumidity
                    [1,7,{'high':[None,None,'-'],'low':[1,self.l1[4],'+']},2,None,[10,None,10,None]],           #co2
                    [2,8,{'high':[None,None,'-'],'low':[2,self.l1[5],'+']},2,True,[None,5*3600,None,[0,6],None]],   #lightintensity
                    [3,9,{'high':[1,self.l1[8],'-'],'low':[3,self.l1[6],'+']},2,None,[None,None,None,None,[2,10,1]]],#temperature
                    [4,10,{'high':[None,None,'-'],'low':[None,None,'+']},2,True,None],                          #humidity
        
        
        ]
        self.count=0
        #list with tkinter objects, otherwise you can't copy them
        self.l5=[self.input1,self.input2,self.input3,self.input4,self.input5,self.input6,
                 self.output1,self.output2,self.output3,self.output4,self.output5,self.output6]
        
        #memory for how often devices were used
        self.memory=[[0,0,0,None,None],          #[x/h,t/24h,t/am stueck, startingtime, remember if this was already counted,remember hour for time based devices]
                    [0,0,0,None,None],
                    [0,0,0,None,None],
                    [0,None,None,None,None],
                    [None,None,None,None,None],
                    [None,None,None,None,None]
                    ]

        #set starting times for memory for 1st run
        self.now=datetime.now()
        self.start=int(self.now.strftime('%H'))              #self.start=int(datetime.now().strftime('%H'))

        self.startday=int(self.now.strftime('%d'))
        
         
        #set devices to gray in 1st run      
        for i in range(4):
            
            self.changecolor(i,None)
            
        
        
        
        self.programloop()              #call function 'automatically' here
    
            
    def programloop(self):
        try:  

            self.master.after(5000)
            
            #make temp copy of self.ll
            self.li=copy.deepcopy(self.ll)          #deepcopy kann eigentlich keine tkinter objects kopieren, deshalb sind in der self.ll liste nur indexe fuer die self.l5 liste, die die objekte enthaelt
                                                    #honestly I don't remember why a copy of self.ll is needed. Seems to work without it, however further investigation needed
            #modify memory
            self.resetmemory('realtime',None)      
                
            

            for idx,element in enumerate(self.li):
                print(l3)

                #set hour for the whole time of correcting this device
                self.hour=int(datetime.now().strftime('%H'))       #get string with current hour
                #set self.memory[4] as True, to register the use of devices
                self.memory[idx][4]=True
            #checks if device shouldn't be turned on in certain time frame                        
                if self.checktime(element,idx,'timeframe')=='continue':
                    continue
                while values.checkintervall(element[0])!=True:
                    
                    self.direction=element[2][values.checkintervall(element[0])]        #long expression just returns high/low dictionary, as to not have millions of loops 
                    self.changecolor(element[1],None)                                  #color measurand as None/red           
                    self.changecolor(self.direction[0],True)                            #color devices, both changecolor and changeconnection, have a way of ignoring the argument when its None

                    self.changeconnections(self.direction[1])                           #change connection-->point to 'used' devices

                    if element[4]==None and self.direction[0]!= None:                 #this guarantees that certain measurands don't get corrected at all, or only partially(like only raising the value)
                        self.useddevice=self.direction[0]                               #placing the used device variable here, guarantees, only really the last 'used' devices gets marked
                        self.memory[idx][3]=datetime.now()
                        self.timelog(element,idx,'x/h')                              #register general use of device one time

                        values.simulation('',element[0],self.direction[2])  

                    else:                                                   #goes into this when the measurand can't be changed in one or even two directions
                        self.timelog(element,idx,'normallogging')           #NEEDS to be outside if None, as to also add the running time of light, if lightintenisty now exceeds the upper limit
                        if self.direction[0]!= None:                        #it enters this loop, if it actually got a device to power up, in case of i.e lightintenistity too high, it doesn't
                            self.timelog(element,idx,'x/h')                      #register general use of device one time
                            self.memory[idx][3]=datetime.now()              #startingtime always needs to be after timelog, otherwise you measure the wrong way around
                        else:                                               #measurand hasn't got a device to power up
                            self.resetmemory('atthetime',idx)

                        self.changeconnections(self.l1[9])                  #set to no connection
                        if values.checkintervall(element[0])=='high':       #turn off low device because measurand is too high, and you can't change it, i.e. lightintensity 
                            self.changecolor(element[2]['low'][0],None)     #note to self: this is all very convoluted-->Think carefully before changing sth
                        break
                    
                    #correcting intervall
                    self.master.after(1000)                         

                    #add small increments of 'normally' used device, basically adds the 1000 ms from above
                    self.timelog(element,idx,'normallogging')
                    
                    #exit if t/atthetime is exceeded    (contains bascially most code from the else below)
                    if element[5] is not None:              #only for the time sensitive
                        if self.memory[idx][2] and element[5][2] is not None:               #needed to not cause errors when there is no atthetime function needed for measurand
                            if self.memory[idx][2]>=element[5][2]:                          #NOTE: Measurands with simulation-correction:None, never need to enter the followinng code, because the devices are intended to run in the background. Checking t/atthetime doesn't make sense for them
                                print('The',element[5][2],'seconds of allowed uptime, has been reached here.')
                                #set device time of powered up device to 0
                                self.resetmemory('atthetime',idx)
                                #set to no connection
                                self.changeconnections(self.l1[9])
                                #turning off used device
                                self.changecolor(self.useddevice,None)        
                                self.useddevice=None
                                break
                    
                    
                else:
                    #timelogging
                    self.timelog(element,idx,'normallogging')
                    
                    print(self.memory[idx],'\n')
                    #set device time of powered up device to 0
                    self.resetmemory('atthetime',idx)


                    #set to no connection
                    self.changeconnections(self.l1[9])          
                
                    #coloring/turning off devices...
                    self.changecolor(element[1],True)               #color measurand as correct/green
                    self.changecolor(self.useddevice,None)         #Turn off just used device
                    self.useddevice=None                           #Forget last used device
                    
                    if element[4]==True:                            #turn off measurand devices with no simulation, in case they are in the right intervall
                        self.changecolor(element[2]['high'][0],None)
                        self.changecolor(element[2]['low'][0],None)

            file1.write('Das ist l3 nach der Correction und vor der Simulation: '+str(l3)+'\n')
            file1.write('Das ist das gesamte MEMORY nach der Korrektion: '+str(self.memory)+'\n')
                    
            #just for testing code
            self.checktime(element,idx,'time-devices')

            #simulation
            print('Starting with simulation!')
            for p in range(5):
                values.simulation('simulation',None,None)
                for u in self.ll:
                    if values.checkintervall(u[0])==True:
                        self.changecolor(u[1],True)
                    else:
                        self.changecolor(u[1],None)
                self.master.after(5000)

            file1.write('Start einer neuen Runde um '+datetime.now().strftime("%H:%M:%S")+'\n')
            print('Das ist l3 nach der Simulation: '+str(l3))
            file1.write('Das ist l3 nach der Simulation: '+str(l3)+'\n')
        
        
            self.master.after(1, self.programloop)  #trick is to call function again, at end of function
        except:
            file1.close()
            cleanclose()
            print('Did you cleanup?')
            


    def changecolor(self, widgidx, bool):          #simply changes bg color  of widg, depending on bool
        if widgidx != None:                       #this guarantees no coloring of unused devices; basically same loop in changeconnections
            widg=self.l5[widgidx]                   #get real widget object from list
            if widgidx>=6:                          #formerly it was if (str(widg)[12])=='2', however tkinter objects don't seem to be named to the same convention as on this deb machine
                if bool is True:
                    widg.config(bg='green')
                else:
                    widg.config(bg='red')
                self.master.update()                    #works much better with update(), dont know why
            else:
                relais(widgidx,bool)
                
                if bool is True:
                    widg.config(bg='blue')
                else:
                    widg.config(bg='grey')
                self.master.update()  

    def changetext(self, widg, tex):          #simply changes bg text  of widg, depending on bool
        widg.config(text=tex)
        self.master.update()

    def changeconnections(self,connection):      #function, basically draws requested connection
        if connection != None:                    #this there in case of no used device
            for (connect,widget) in zip(connection, self.l2):
                widget.config(text=connect)
                self.master.update()
    
    def resetmemory(self,argument,index):
        if argument=='realtime':
            if self.startday!=int(datetime.now().strftime('%d')):   #reset day memory
                self.memory[0][1]=0
                self.memory[1][1]=0
                self.memory[2][1]=0
                self.startday=int(datetime.now().strftime('%d'))


            
            if self.start!=int(datetime.now().strftime('%H')):      #reset hour memory
                file1.write('Reset of hourly memory!\n')
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
                if self.memory[index][4] is not None and self.memory[index][0] is not None: #las part needed to not cause errors if logging this is not required
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
        checks if turning on certain devices, after one hour, if x/h is >certain value(element[5][4][0) is required
        should alway be initiated by measurand 'using' the device as the last one in for loop. i.e both co2 and temp use the fan, 
        temp correction comes after co2 correction, hence the indication of ,[2,10] is only in time dependent list in self.ll in temp and not in co2
        '''
        if argument=='time-devices':
            if element[5] is not None:
                if element[5][4] is not None:       #this ensures the reasoning from above
                    self.totaluses=self.memory[index][0]
                    if element[5][4][2] is not None:
                        self.totaluses+=self.memory[index][element[5][4][2]]    #add uses of device, when not only used by one measurand
                        print('Das sind die kombinierten totaluses von CO2 und temp ',self.totaluses)
                    if self.memory[index][0]<=element[5][4][0]:
                        pass


window=Tk()
mygui=guioflabels(window)               #this calls the class and sets mygui as instance; in class refered to instance with self; in o words self is mygui in this case        





window.mainloop()                       #(https://github.com/Akuli/python-tutorial/blob/master/basics/classes.md)