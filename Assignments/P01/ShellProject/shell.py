#!/usr/local/bin/python3
################################# __HEADER__ #####################################
##################################################################################
# Advanced Operating Systems Shell
#
# Author:  Khethulwazi Kunene
#           
#
# Key Advisor:  Dr. Terry Griffin
#
# Key Contributions:  Dr. Griffin (Getch, Parser and Shell Starter Code)
#                     Bing AI, 'https://www.bing.com/'
#                     Digital Ocean, 'https://www.digitalocean.com/community/tutorials'
#                     flexiple, 'https://flexiple.com/python/python-append-to-string'
#                     Free Code Camp, 'https://www.freecodecamp.org'
#                     Geeks for Geeks, 'https://www.geeksforgeeks.org'
#                     How to Forge, 'https://www.howtoforge.com/tutorial'
#                     How-to Geak, 'https://www.howtogeek.com'
#                     julia, 'https://docs.julialang.org/en/v1/stdlib/REPL/'
#                     Learn Data Sci, 'https://www.learndatasci.com/solutions/python-move-file/'
#                     Python 3.12.0 Documentation, 'https://docs.python.org'
#                     Python for Beginners, 'https://www.pythonforbeginners.com/'
#                     Real Python, 'https://realpython.com'
#                     Stack Exchange, 'https://unix.stackexchange.com/'
#
# Search Engines:  bing
#                  Firefox
#                  Google
#
#
################################# __Shell__ ######################################
##################################################################################
"""
This file is about using getch to capture input and handle certain keys when
the are pushed. The 'command_helper.py' was about parsing and calling functions.
This file is about capturing the user input so that you can mimic shell behavior.
"""
import sys
from time import sleep
from pathlib import Path
from commands.pwd import pwd
from commands.ls import ls
from commands.cd import cd
from commands.mv import mv
from commands.cp import cp
from commands.rm import rm
from commands.wc import wc
from commands.ex import ex
from commands.cat import cat
from commands.less import less
from commands.head import head
from commands.tail import tail
from commands.grep import grep
from commands.exit import exit
from commands.touch import touch
from commands.chmod import chmod
from commands.mkdir import mkdir
from commands.rmdir import rmdir
from commands.getch import Getch
from commands.history import history
from commands.Parse import ParseCmd
from fileSystem import FileSystem
from sqliteCrud import SqliteCrud

#from CMDP import *
getch = Getch()                             # create instance of our getch class
prompt = '\033[33m' + str(Path.cwd()) + "$ " + '\033[0m' #'\033[0;33m' gold           # set default prompt
################################# Parse_cmd ######################################
##################################################################################
def PARSE(cmd):
    flags = []
    directives = []
    params = []
    cmd = cmd.split()
    print(cmd)
    for f in cmd:
        if '--' in f:
            directives.append(f.lstrip('--'))
        elif '-' in f:
            flags.append(f.lstrip('-'))
        elif '/' in f:
            params.append(f.lstrip('/'))
    return {'flags':''.join(flags),'directives':directives,'params':params}
################################# print_cmd ######################################
##################################################################################
def print_cmd(cmd, cursor_pos=0):
    """Prints the command line with cursor handling."""
    #if not cursor_pos:
        #cursor_pos = len(cmd)
    # Clear the current line
    padding = " " * 100
    sys.stdout.write("\r" + padding)
    
    # Print prompt and command
    sys.stdout.write("\r" + prompt + cmd)
    
    # Move the cursor to the specified position
    sys.stdout.write(f"\r{prompt}{cmd}")
    sys.stdout.write(f"\033[{(len(prompt)-9) + cursor_pos + 1}G")  # Move to the cursor position
    sys.stdout.flush()
################################### Main #########################################
##################################################################################
def find(cmd):
    p = ParseCmd(cmd)               # Parse is called and cmd's are broken down
    pdict = p.allCmdsDict
    #print(p.fileName)
    # Loop to call all functions requested by the user

    for F_IT in p.allCmds:
        if F_IT.cmd == 'cat':       # Concantenate
            return cat(**pdict)
        elif F_IT.cmd == 'cp':      # Copy File
            cp(**pdict)
        elif F_IT.cmd == 'grep':    # Grep File
            grep(**pdict)
        elif F_IT.cmd == 'head':    # Head of file
            head(**pdict)
        elif F_IT.cmd == 'history': # History
            #update  history
            with open('history.txt', 'w') as ht:
                for command in hist:
                    ht.write(command + "\n")
            history(**pdict)
        elif F_IT.cmd == 'less':    # Less (Page at a time)
            return less(**pdict)
        elif F_IT.cmd == 'ls':
            return ls(**pdict)
        elif F_IT.cmd == 'mv':      # Move File
            mv(**pdict)
        elif F_IT.cmd == 'rm':      # Remove File
            rm(**pdict)
        elif F_IT.cmd == 'rmdir':   # Remove Empty Directory
            rmdir(**pdict)
        elif F_IT.cmd == 'tail':    # End of File
            tail(**pdict)
        elif F_IT.cmd == 'wc':      # Word Count
            return wc(**pdict)
        elif F_IT.cmd == "touch":
            touch(**pdict)
        elif F_IT.cmd == "!":
            ex(**pdict)
        elif F_IT.cmd == "\r":
            cmd = ""
            print_cmd(cmd)
        elif F_IT.cmd == " ":
            print("")
            break
        else: 
            error = ": command not found"
            print_cmd(cmd + error, len(cmd)+len(error))                  # now print error cmd prompt
            print("")                               #print empty input to avoid consol overwrite
            break
        return

def Pipe(cmd):
    p = ParseCmd(cmd)               # Parse is called and cmd's are broken down
    pdict = p.allCmdsDict
    
    if len(p.allCmds) == 1:
        return find(p.allCmds[0])
    result = find(p.allCmds[0])
    print(pdict)
    print(result)


    return Pipe(p.allCmds[-1:])

     

if __name__ == '__main__':
    cmd = ""
    ht = ""                                # empty variable for history
    hist = []                              # list for command history
    H = 0
    #I = ""
    pos = 0


    #createhistory()                           # Creates history file
    with open('history.txt', 'r+') as ht:
        for w in ht.readlines():
            hist.append(str(w).strip('\n'))
            #print(w)
    print_cmd(cmd)                          # print to terminal
    H = len(hist)

    db = "zztop.sqlite"                    #filesystem

    conn = SqliteCrud(db)                  #filesystem

    fs = FileSystem(db)                    #filesystem

    # Define table schema
    table_name = "files_data"
    columns = ["id INTEGER PRIMARY KEY", "pid INTEGER", "name TEXT", "created_date TEXT", "modified_date TEXT", "size REAL","type TEXT","owner TEXT","groop TEXT","permissions TEXT"]
    # Load table
    test_data = [
        (1, 0, 'Folder1', '2023-09-25 10:00:00', '2023-09-25 10:00:00', 0.0, 'folder', 'user1', 'group1', 'rwxr-xr-x'),
        (2, 1, 'File1.txt', '2023-09-25 10:15:00', '2023-09-25 10:15:00', 1024.5, 'file', 'user1', 'group1', 'rw-r--r--'),
        (3, 1, 'File2.txt', '2023-09-25 10:30:00', '2023-09-25 10:30:00', 512.0, 'file', 'user2', 'group2', 'rw-rw-r--'),
        (4, 0, 'Folder2', '2023-09-25 11:00:00', '2023-09-25 11:00:00', 0.0, 'folder', 'user2', 'group2', 'rwxr-xr--'),
        (5, 4, 'File3.txt', '2023-09-25 11:15:00', '2023-09-25 11:15:00', 2048.75, 'file', 'user3', 'group3', 'rw-r--r--'),
        (6, 4, 'File4.txt', '2023-09-25 11:30:00', '2023-09-25 11:30:00', 4096.0, 'file', 'user3', 'group3', 'rw-r--r--'),
        (7, 0, 'Folder3', '2023-09-25 12:00:00', '2023-09-25 12:00:00', 0.0, 'folder', 'user4', 'group4', 'rwxr-x---'),
        (8, 7, 'File5.txt', '2023-09-25 12:15:00', '2023-09-25 12:15:00', 8192.0, 'file', 'user4', 'group4', 'rw-------'),
        (9, 0, 'Folder4', '2023-09-25 13:00:00', '2023-09-25 13:00:00', 0.0, 'folder', 'user5', 'group5', 'rwxr-xr-x'),
        (10, 9, 'File6.txt', '2023-09-25 13:15:00', '2023-09-25 13:15:00', 3072.25, 'file', 'user5', 'group5', 'rwxr-xr--'),
        (11, 1, 'Folder5', '2023-09-25 13:00:00', '2023-09-25 13:00:00', 0.0, 'folder', 'user5', 'group5', 'rwxr-xr-x'),
    ]

    #create table
    if True:
        conn.drop_table(table_name)

        conn.create_table(table_name, columns)
        print(conn.describe_table(table_name))

        for row in test_data:
            conn.insert_data(table_name, row)
        
        print(conn.formatted_print(table_name))

    while True:                             # loop forever
        char = getch()                      # read a character (but don't print)
        
        if char == '\x03' or cmd == 'exit': # ctrl-c
            #update history file
            with open('history.txt', 'w') as ht:
                for command in hist:
                    ht.write(command + "\n")
            exit()
            #raise SystemExit(" Bye!")
        elif char == '\x7f':                # back space pressed
            if pos == len(cmd) and len(cmd) > 0:
                cmd = cmd[:-1]
                pos -= 1
            elif pos > 0 and len(cmd) > 0:
                cmd = ''.join([cmd[:(pos)-1],  cmd[(pos):]])
                pos -= 1
            print_cmd(cmd,pos)

        elif char in '\x1b':                # arrow key pressed
            null = getch()                  # waste a character
            direction = getch()             # grab the direction
            if direction in 'A':            # up arrow pressed
                # get the PREVIOUS command from your history (if there is one)
                # prints out 'up' then erases it (just to show something)
                #cmd += u"\u2191"
                if H <= 0:
                    oldCmd = ""
                elif H > 0:
                    H -= 1              # or H = H - 1 for decrementing
                    #print(hist[H]) 
                    oldCmd = hist[H]
                    pos = len(oldCmd)
                
                cmd = oldCmd
                print_cmd(cmd, len(cmd))
         
            if direction in 'B':            # down arrow pressed
                # get the NEXT command from history (if there is one)
                # prints out 'down' then erases it (just to show something)
                #cmd += u"\u2193"
                if H < len(hist)-1:
                    H += 1              # or H = H + 1 for incrementing
                    #print(hist[H])
                    cmd = hist[H]
                    pos = len(cmd)
                    print_cmd(cmd, pos)
                elif H == len(hist)-1:
                    cmd = ""
                    pos = 0
                    print_cmd(cmd, pos)

            if direction in 'C':            # right arrow pressed
                # move the cursor to the right on your command prompt line
                # prints out 'right' then erases it (just to show something)
                #cmd += u"\u2192"
                if pos < len(cmd):
                    pos += 1
                print_cmd(cmd, pos)
                
            if direction in 'D':            # left arrow pressed
                # moves the cursor to the left on your command prompt line
                # prints out 'left' then erases it (just to show something)
                #cmd += u"\u2190"
                #x = len(prompt) + len(cmd) - 1
                if pos > 0:
                    pos -= 1
                print_cmd(cmd, pos)             
                #sleep(10.0)

        # If no No arrows, delete or exit sequence, the commands are updated in history and processed
        elif char in '\r':
            #print("\n")
            pos = 0
            
            if cmd:
                H = len(hist) + 1
                #updateHistory(cmd)              # History called and updated with cmd's
                hist.append(cmd)
                p = ParseCmd(cmd)               # Parse is called and cmd's are broken down
                pdict = p.allCmdsDict
                #print(p.fileName)
                # Loop to call all functions requested by the user
                if p.redirect:
                    print("")
                    file = open(p.fileName, "w+")
                    og_stdout = sys.stdout
                    sys.stdout = file

                    for F_IT in p.allCmds:
                        if F_IT.cmd == 'cat':       # Concantenate
                            cat(**pdict)
                            #print('cat')
                        elif F_IT.cmd == 'cd':      # Change Directory
                            prompt = '\033[33m' +  cd(**pdict) + "$ " + '\033[0m'
                            #print(pdict)
                            #fs.cd(conn,table_name, pdict)
                            #print('cd')
                        elif F_IT.cmd == 'chmod':   # Change Mode
                            chmod(**pdict)
                            #print('chMod')
                        elif F_IT.cmd == 'cp':      # Copy File
                            cp(**pdict)
                            #print('cp')
                        elif F_IT.cmd == 'grep':    # Grep File
                            grep(**pdict)
                            #print('grep')
                        elif F_IT.cmd == 'head':    # Head of file
                            head(**pdict)
                            #print('head')
                        elif F_IT.cmd == 'history': # History
                            #update  history
                            with open('history.txt', 'w') as ht:
                                for command in hist:
                                    ht.write(command + "\n")
                            history(**pdict)
                        elif F_IT.cmd == 'less':    # Less (Page at a time)
                            less(**pdict)
                            #print('less')
                        elif F_IT.cmd == 'ls':
                            #print("\u001b[42mHello, world!\u001b[0m")
                            ls(**pdict)
                            #print(**pdict)
                            #fs.list(conn, table_name, **pdict)
                            #print('ls')
                        elif F_IT.cmd == 'mkdir':   # Make Directory
                            mkdir(**pdict)
                            #data = (12,0,'banana','2023-11-14 10:00:00','2023-11-14 10:00:00',0,'folder','user1','group6','rwxrwxrwx')
                            #fs.mkdir(fs,table_name,kwargs=data)
                            #print('mkDir')
                        elif F_IT.cmd == 'mv':      # Move File
                            mv(**pdict)
                            #print('mv')
                        elif F_IT.cmd == 'pwd':     # Current Working Directory
                            pwd(**pdict)
                            #fs.pwd()
                            #print('pwd')
                        elif F_IT.cmd == 'rm':      # Remove File
                            rm(**pdict)
                        elif F_IT.cmd == 'rmdir':   # Remove Empty Directory
                            rmdir(**pdict)
                            #print('rmDir')
                        elif F_IT.cmd == 'tail':    # End of File
                            tail(**pdict)
                            #print('tail')
                        elif F_IT.cmd == 'wc':      # Word Count
                            wc(**pdict)
                            #print('wc')
                        elif F_IT.cmd == "touch":
                            touch(**pdict)
                        elif F_IT.cmd == "!":
                            ex(**pdict)
                        elif F_IT.cmd == "\r":
                            cmd = ""
                            print_cmd(cmd)
                        elif F_IT.cmd == " ":
                            print("")
                            break
                        else: 
                            error = ": command not found"
                            print_cmd(cmd + error, len(cmd)+len(error))                  # now print error cmd prompt
                            print("")                               #print empty input to avoid consol overwrite
                            break
                        sys.stdout = og_stdout
                        file.close()

                elif p.pipe:
                    Pipe(cmd)
                else:
                    for F_IT in p.allCmds:
                        if F_IT.cmd == 'cat':       # Concantenate
                            cat(**pdict)
                            #print('cat')
                        elif F_IT.cmd == 'cd':      # Change Directory
                            prompt = '\033[33m' +  cd(**pdict) + "$ " + '\033[0m'
                            #print(pdict)
                            #fs.cd(conn,table_name, pdict)
                            #print('cd')
                        elif F_IT.cmd == 'chmod':   # Change Mode
                            chmod(**pdict)
                            #print('chMod')
                        elif F_IT.cmd == 'cp':      # Copy File
                            cp(**pdict)
                            #print('cp')
                        elif F_IT.cmd == 'grep':    # Grep File
                            grep(**pdict)
                            #print('grep')
                        elif F_IT.cmd == 'head':    # Head of file
                            head(**pdict)
                            #print('head')
                        elif F_IT.cmd == 'history': # History
                            #update  history
                            with open('history.txt', 'w') as ht:
                                for command in hist:
                                    ht.write(command + "\n")
                            history(**pdict)
                        elif F_IT.cmd == 'less':    # Less (Page at a time)
                            less(**pdict)
                            #print('less')
                        elif F_IT.cmd == 'ls':
                            #print("\u001b[42mHello, world!\u001b[0m")
                            ls(**pdict)
                            #print(**pdict)
                            #fs.list(conn, table_name, **pdict)
                            #print('ls')
                        elif F_IT.cmd == 'mkdir':   # Make Directory
                            mkdir(**pdict)
                            #data = (12,0,'banana','2023-11-14 10:00:00','2023-11-14 10:00:00',0,'folder','user1','group6','rwxrwxrwx')
                            #fs.mkdir(fs,table_name,kwargs=data)
                            #print('mkDir')
                        elif F_IT.cmd == 'mv':      # Move File
                            mv(**pdict)
                            #print('mv')
                        elif F_IT.cmd == 'pwd':     # Current Working Directory
                            pwd(**pdict)
                            #fs.pwd()
                            #print('pwd')
                        elif F_IT.cmd == 'rm':      # Remove File
                            rm(**pdict)
                        elif F_IT.cmd == 'rmdir':   # Remove Empty Directory
                            rmdir(**pdict)
                            #print('rmDir')
                        elif F_IT.cmd == 'tail':    # End of File
                            tail(**pdict)
                            #print('tail')
                        elif F_IT.cmd == 'wc':      # Word Count
                            wc(**pdict)
                            #print('wc')
                        elif F_IT.cmd == "touch":
                            touch(**pdict)
                        elif F_IT.cmd == "!":
                            ex(**pdict)
                        elif F_IT.cmd == "\r":
                            cmd = ""
                            print_cmd(cmd)
                        elif F_IT.cmd == " ":
                            print("")
                            break
                        else: 
                            error = ": command not found"
                            print_cmd(cmd + error, len(cmd)+len(error))                  # now print error cmd prompt
                            print("")                               #print empty input to avoid consol overwrite
                            break
            #print empty input to avoid consol overwrite
            #sleep(1)            
            cmd = ""                        # reset command to nothing (since we just executed it)
            print_cmd(cmd)                  # now print empty cmd prompt
        else:
            if pos == len(cmd):
                cmd += char 
            else:
               cmd = ''.join([cmd[:(pos)], char,  cmd[(pos):]]) 
            pos += 1                   # add typed character to our "cmd"
            print_cmd(cmd, pos)                  # print the cmd outc
