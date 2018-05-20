import shutil
from acquisition import adbExtract
from search import dbSearch


def clearFolders():
    '''Clears androidbackup, rawdump and evidence folders'''
    shutil.rmtree('androidbackup')
    shutil.rmtree('rawdump')
    shutil.rmtree('evidence')


def main():
    clearFolders()
    adbExtract()
    dbSearch()


if __name__ == '__main__':
    main()
