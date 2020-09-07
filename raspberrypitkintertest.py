from tkinter import *

class mygui:
    def __init__(self,master):
        self.master=master

        self.label=Label(master,bg='green',text='Hallo Test ist das grün?')
        self.label.pack()

root=Tk()
my_gui=mygui(root)

root.mainloop()