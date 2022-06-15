import sys # import is only necessary because eip.py is not in this directory
import config
import os #needed to run programs within this script
sys.path.append('..')
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from pylogix import PLC
from concurrent import futures
import time
from datetime import datetime
import threading
from tkinter import messagebox
window = Tk()
window.title("Heartland Automation MaxN10 PLC Logger")
window.geometry('800x300')

thread_pool_executor = futures.ThreadPoolExecutor(max_workers=1)

config.init()

def fileLocation():
    global pickedFileLocation
    pickedFileLocation=filedialog.asksaveasfilename(initialdir="/",title="Select File Location")
    global ipAddressBox
    lbl1 = Label(window, text="File stored at:"+pickedFileLocation)
    lbl1.grid(column=3, row=0,pady=5)
    btn = Button(window, text="Connect to PLC", command=clicked)
    btn.grid(column=2, row=1, padx=(5,10), pady=5)
    global lb
    

def clicked():
    
    global comm
    with PLC() as comm:
        comm.IPAddress = config.ipAddress[0]
        tags = comm.GetTagList()
    for t in tags.Value:
        if t.DataType=='BOOL':
            config.tagName.append(t.TagName)
            print(t.TagName, t.DataType)
        elif t.DataType=='DINT':   
            config.tagName.append(t.TagName)
            print(t.TagName, t.DataType) 
        elif t.DataType=='SINT':   
            config.tagName.append(t.TagName)
            print(t.TagName, t.DataType) 
        elif t.DataType=='INT':   
            config.tagName.append(t.TagName)
            print(t.TagName, t.DataType) 
            window.update_idletasks()
    
    global run
    run = Button(window, text="Run Log", command=runLogButton)
    run.grid(column=1, row=2, pady=5)
    global stopButton
    stopButton = Button(window, text="Stop Log", command=stopLog)
    stopButton.grid(column=2, row=2, pady=5)
    
def runLogButton():
    thread_pool_executor.submit(runLog)

def runLog():
   global select_tag
   select_tag= ['Counter', 'Toggle_Bit']
   global stopVar
   stopVar = True 
   global logState
   logState="Running"
   logStateLabel= Label(window, text="Log is "+logState)
   logStateLabel.grid(column=0, row=3, pady=5)
   filename=datetime.now()
   with open(pickedFileLocation, 'w') as txt_file:    
       while stopVar == True:
           for x in select_tag:
               print (x)
               now = datetime.now()
               ret = comm.Read(x)
               txt_file.write(now.strftime("%Y-%m-%d %H:%M:%S")+' '+str(x)+'= '+str(ret.Value)+'\n')
           time.sleep(1)
           txt_file.write('------------------'+'\n')
           
def stopLog():
    global logState
    logState="Stopped"
    logStateLabel= Label(window, text="Log is "+logState)
    logStateLabel.grid(column=0, row=3, pady=5)
    global stopVar
    stopVar = False
    print ("Stopped")

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()

fileLbl = Label(window, text="Select File Location")
fileLbl.grid(column=0, row=0, pady=5)
fileBtn = Button(window, text="Select File", command=fileLocation)
fileBtn.grid(column=1, row=0, pady=5)

window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
