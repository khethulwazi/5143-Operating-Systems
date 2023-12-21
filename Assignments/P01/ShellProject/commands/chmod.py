from pathlib import Path
import os

def chmod(**kwargs):
    
    permission = str(kwargs.get('params')[0])
    fileName = str(kwargs.get('params')[1])
    path = Path.cwd() + '/' + fileName
    os.chmod(path, permission)
