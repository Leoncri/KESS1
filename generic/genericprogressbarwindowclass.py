import tkinter as tk
from tkinter import ttk
import tkinter.messagebox

import threading

# class for generating a progress bar window that runs a task in background
class GenericProgressBarWindow(tk.Toplevel):
    def __init__(self, parent, task, title, result=False):
        # init window
        super().__init__()
        
        # store the return variable
        self.result = result
        
        # change title of the window
        self.title(title)
        
        # create a progress bar
        self.pb = ttk.Progressbar(self, orient="horizontal", mode="determinate", length = 280)
        self.pb.grid(column=0, row=0, padx=10, pady=20)
        
        # create the text below
        self.pl = ttk.Label(self, text="")
        self.pl.grid(column=0, row=1)
        
        # start the task
        self.task = threading.Thread(target=task, args=(self,))
        self.task.start()
    
    def SetProgress(self, progress, text):
        # set the progress of the bar in % and the text below
        if progress >= 0 and progress <= 100:
            self.pb['value'] = progress
            self.pl['text'] = text
        
        return
    
    def SetReturnVariable(self, value):
        print ("Setting return variable to " + str(value))
        self.result = value
        return
    
    def Finished(self):
        self.destroy()
        return
    
    def ShowError(self, title, errorMessage):
        # show the error
        tkinter.messagebox.showerror(title=title, message=errorMessage)
        return
    
    def ShowWarning(self, title, warningMessage):
        # show the warning
        tkinter.messagebox.showwarning(title=title, message=warningMessage)
        return
    
    def ShowInfo(self, title, infoMessage):
        # show the info
        tkinter.messagebox.showinfo(title=title, message= infoMessage)
        return