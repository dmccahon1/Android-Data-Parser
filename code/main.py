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


def main():
    print("test")

    
if __name__ == '__main__':
    main()
