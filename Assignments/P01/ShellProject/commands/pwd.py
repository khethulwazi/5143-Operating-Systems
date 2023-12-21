#Once you’ve imported Path, you can make use of existing methods 
#to get the current working directory or your user’s home directory.
#When you instantiate pathlib.Path,
#you get either a WindowsPath or a PosixPath object.
#"With Path, you instantiate a concrete path for the platform that you’re using
# while also keeping your code platform-independent."
#https://realpython.com/python-pathlib/
from pathlib import Path

def pwd(**kwargs):
  print ('\n'+ str(Path.cwd()))

