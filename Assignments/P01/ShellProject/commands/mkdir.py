from pathlib import Path
import os

def mkdir(**kwargs):
    path = str(Path.cwd()) + '/' + str(kwargs.get('params')).strip('[]').strip('\'\'')
    
    if not os.path.isdir(path):
        print('\n',path)
        os.makedirs(path)
