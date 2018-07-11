import shutil
import os
import datetime
import subprocess
import tkinter
from acquisition import adbExtract

def clearFolders():
    '''Clears androidbackup, rawdump and evidence folders'''
    shutil.rmtree('androidbackup', ignore_errors=True)
    shutil.rmtree('rawdump', ignore_errors=True)
    shutil.rmtree('evidence', ignore_errors=True)


class Window(tkinter.Frame):

    def __init__(self, master=None):
        '''Initialise the Master Window'''

        tkinter.Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        '''Create Init Window'''

        self.master.title("GUI")
        self.pack(fill=tkinter.BOTH, expand=1)
        useDevice = tkinter.Button(self, text="Use Device", command=adbExtract)
        useDevice.place(x=10, y=10)

        selADB = tkinter.Button(self, text="Select File ")
        selADB.place(x=10, y=50)

        v = tkinter.StringVar()
        updateLabel = tkinter.Label(self, textvariable=v).place(x=10, y=90)

        v.set("This is the new text bruhh")


root = tkinter.Tk()
root.geometry("400x300")
app = Window(root)
root.mainloop()


if __name__ == '__main__':
    main()
