import shutil
from acquisition import adbExtract
from search import dbSearch


def clearFolders():
    '''Clears androidbackup, rawdump and evidence folders'''
    shutil.rmtree('androidbackup', ignore_errors=True)
    shutil.rmtree('rawdump', ignore_errors=True)
    shutil.rmtree('evidence', ignore_errors=True)


def main():
    clearFolders()
    adbExtract()
    dbSearch()


if __name__ == '__main__':
    main()
