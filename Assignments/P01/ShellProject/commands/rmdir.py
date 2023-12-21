"""""Does not remove a directory that is not empty

"""""
from pathlib import Path
import os

def rmdir(**kwargs):

    dirName = str(kwargs.get('params')).strip('[]').strip('\'\'')
    path = str(Path.cwd())+'/'+dirName
    print('\n',path)
    os.rmdir(path)
