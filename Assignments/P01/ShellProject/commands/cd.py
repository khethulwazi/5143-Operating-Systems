from pathlib import Path
import os

def cd(**kwargs):
  
  dirName = str(kwargs.get('params')).strip('[]').strip('\'\'')
  #print ('\n'+str(Path.cwd()))

  print(os.path.abspath(str(Path.cwd())+'/'+dirName))
  path = str(Path.cwd())+'/'+dirName
  os.chdir(path)
