from pathlib import Path
import pydoc

def less(**kwargs):
    print('\r')
    path = str(Path.cwd()) + '/' + str(kwargs.get('params')[-1])
    with open(path) as file:
        pydoc.pager(file.read())
