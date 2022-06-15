'''
'''
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
window = Tk()
window.title("Heartland Automation MaxN10 PLC Logger")
window.geometry('800x600')
thread_pool_executor = futures.ThreadPoolExecutor(max_workers=1)
config.init()

def fileLocation():
    global pickedFileLocation
    pickedFileLocation=filedialog.asksaveasfilename(initialdir="/",title="Select File Location")
    lbl = Label(window, text="Enter IP Address")
    lbl.grid(column=0, row=1, pady=5)
    global ipAddressBox
    ipAddressBox = Entry(window,width=20)
    ipAddressBox.grid(column=1,row=1, padx=(1,1), pady=5)
    lbl1 = Label(window, text="File stored at:"+pickedFileLocation)
    lbl1.grid(column=3, row=0,pady=5)
    btn = Button(window, text="Enter IP", command=clicked)
    btn.grid(column=2, row=1, padx=(5,10), pady=5)
    global lb
    

def clicked():
    config.ipAddress.append(ipAddressBox.get())
    global comm
    frame=Frame(window)
    frame.place(x=5,y=150)
    
    global lb  
    lb=Listbox(frame, selectmode=MULTIPLE, width=30)
    lb.grid(column=0, row=2)
    scrollbar = Scrollbar(frame, orient="vertical",command=lb.yview,width=32)
    scrollbar.grid(column=1, row=2,sticky=N+S)
    lb.config(yscrollcommand=scrollbar.set)
    
    with PLC() as comm:
        comm.IPAddress = config.ipAddress[0]
        tags = comm.GetTagList(allTags=True)
    for t in tags.Value:
        if t.DataType=='BOOL':
            config.tagName.append(t.TagName)
            print(t.TagName, t.DataType)
        elif t.DataType=='DINT':   
            config.tagName.append(t.TagName)
            print(t.TagName, t.DataType)
        elif t.DataType=='NONE':   
            config.tagName.append(t.TagName)
            print(t.TagName, t.DataType)            
        elif t.DataType=='SINT':   
            config.tagName.append(t.TagName)
            print(t.TagName, t.DataType) 
        elif t.DataType=='INT':   
            config.tagName.append(t.TagName)
            print(t.TagName, t.DataType)
        elif t.DataType=='UDINT':   
            config.tagName.append(t.TagName)
            print(t.TagName, t.DataType)
            window.update_idletasks()
    lb.insert(END, *config.tagName)
    
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
   select_tag= list()
   selected = lb.curselection()
   global stopVar
   stopVar = True 
   global logState
   logState="Running"
   logStateLabel= Label(window, text="Log is "+logState)
   logStateLabel.grid(column=0, row=3, pady=5)
   for i in selected:
       selectItem =lb.get(i)
       select_tag.append(selectItem)
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



fileLbl = Label(window, text="Select File Location")
fileLbl.grid(column=0, row=0, pady=5)
fileBtn = Button(window, text="Select File", command=fileLocation)
fileBtn.grid(column=1, row=0, pady=5)

window.mainloop()
