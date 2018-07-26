import shutil
from acquisition import adbExtract


def clearFolders():
    '''Deletes androidbackup, rawdump and evidence folders'''
    shutil.rmtree('android_backup', ignore_errors=True)
    shutil.rmtree('rawdump', ignore_errors=True)
    shutil.rmtree('evidence', ignore_errors=True)


def main():
    clearFolders()
    adbExtract()


if __name__ == '__main__':
    main()
