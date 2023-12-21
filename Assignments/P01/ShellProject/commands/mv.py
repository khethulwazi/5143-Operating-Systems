from pathlib import Path
import shutil

def mv(**kwargs):

    source = str(Path.cwd()) + str(kwargs.get('params')[0])
    if '/' in kwargs.get('params')[1]:
        destination = str(kwargs.get('params')[1])
    else:
        destination = str(Path.cwd()) + str(kwargs.get('params')[1])
    shutil.move(source, destination)
