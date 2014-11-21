'''
Created on 20.11.2014

@author: RM
'''

'''
from Tkinter import *           # Import the Tkinter library
root = Tk()                    # Create a background window object
                                # A simple way to create 2 lists
li     = ['Carl','Patrick','Lindsay','Helmut','Chris','Gwen']
movie  = ['God Father','Beauty and the Beast','Brave heart']
listb  = Listbox(root)          # Create 2 listbox widgets
listb2 = Listbox(root)
for item in li:                 # Insert each item inside li into the listb
    listb.insert(0,item)

for item in movie:              # Do the same for the second listbox
    listb2.insert(0,item)

listb.pack()                    # Pack each listbox into the main window
listb2.pack()
root.mainloop()                 # Invoke the main event handling loop
'''

from Tkinter import Tk, Text, BOTH, W, N, E, S
from ttk import Frame, Button, Label, Style


class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
        
    def initUI(self):
      
        self.parent.title("Windows")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)
        '''
        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)
        '''
        
        lbl = Label(self, text="Windows")
        lbl.grid(sticky=W, pady=4, padx=5)
        
        area1 = Text(self)
        area1.grid(row=1, column=0, columnspan=1, rowspan=4, padx=5, sticky=E+W+S+N)
        
        #area2 = Text(self)
        #area2.grid(row=1, column=2, columnspan=1, rowspan=4, padx=5, sticky=E+W+S+N)
        
        #fu python, fu tkinter

        '''        
        abtn = Button(self, text="Activate")
        abtn.grid(row=1, column=3)

        cbtn = Button(self, text="Close")
        cbtn.grid(row=2, column=3, pady=4)
        
        hbtn = Button(self, text="Help")
        hbtn.grid(row=5, column=0, padx=5)

        obtn = Button(self, text="OK")
        obtn.grid(row=5, column=3)        
        '''      

def main():
  
    root = Tk()
    root.geometry("350x300+300+300")
    app = Example(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  