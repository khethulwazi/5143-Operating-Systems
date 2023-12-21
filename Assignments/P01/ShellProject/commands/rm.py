"""""$rm [OPTION]... FILE...

"""""
from pathlib import Path
#import os
import shutil

def rm(**kwargs):

    fileName = str(kwargs.get('params')).strip('[]').strip('\'\'')
    flags = kwargs.get('flags')
    if 'r' and 'f' in flags:
        path = str(Path.cwd())+'/'+ fileName
        print('\n'+ path)
        # Delete a non-empty directory using its path
        shutil.rmtree(path)
        return
    else:
        path = str(Path.cwd())+'/'+ fileName
        print('\n'+ path)
        #os.remove(path)
  

if __name__=='__main__':
    #remove("test.txt")
    print("helloooo")

    #removeRF("Music")
    #sys.stdout.write("\r" + os.getcwd())
