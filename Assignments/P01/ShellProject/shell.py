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
from commands.pwd import pwd
from commands.ls import ls
from commands.cd import cd
from commands.mv import mv
from commands.cp import cp
from commands.rm import rm
from commands.wc import wc
from commands.cat import cat
from commands.less import less
from commands.head import head
from commands.tail import tail
from commands.grep import grep
from commands.exit import exit
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
prompt = "$"                               # set default prompt
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
def print_cmd(cmd):
    """ This function "cleans" off the command line, then prints
        whatever cmd that is passed to it to the bottom of the terminal.
    """
    padding = " " * 80
    sys.stdout.write("\r"+padding)
    sys.stdout.write("\r"+prompt+cmd)
    sys.stdout.flush()
################################### Main #########################################
##################################################################################
if __name__ == '__main__':
    cmd = ""
    ht = ""                                # empty cmd variable
    H = 0
    I = 0
    #open('history.txt', 'a')
    #createhistory()                           # Creates history file
    with open('history.txt', 'r+') as ht:
        History = ht.readlines()
        print(ht.readlines())
    print_cmd(cmd)                          # print to terminal

    db = "zztop.sqlite"

    conn = SqliteCrud(db)

    fs = FileSystem(db)

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
            #delete history file
            exit()
            #raise SystemExit(" Bye!")
        elif char == '\x7f':                # back space pressed
            cmd = cmd[:-1]
            print_cmd(cmd)
        elif char in '\x1b':                # arrow key pressed
            null = getch()                  # waste a character
            direction = getch()             # grab the direction
            if direction in 'A':            # up arrow pressed
                # get the PREVIOUS command from your history (if there is one)
                # prints out 'up' then erases it (just to show something)
                cmd += u"\u2191"
                H -= 1              # or H = H - 1 for decrementing
                #cmd = History[H]
                print(History)
                # sleep(0.3)
                #cmd = cmd[:-1]
            if direction in 'B':            # down arrow pressed
                # get the NEXT command from history (if there is one)
                # prints out 'down' then erases it (just to show something)
                cmd += u"\u2193"
                H += 1              # or H = H + 1 for incrementing
                cmd = History[H]
                print_cmd(cmd)
                #sleep(0.3)
                #cmd = cmd[:-1]
            if direction in 'C':            # right arrow pressed
                # move the cursor to the right on your command prompt line
                # prints out 'right' then erases it (just to show something)
                cmd += u"\u2192"
                cmd = input[:+1]
                print_cmd(cmd)
                sleep(0.3)
                #cmd = cmd[:-1]
            if direction in 'D':            # left arrow pressed
                # moves the cursor to the left on your command prompt line
                # prints out 'left' then erases it (just to show something)
                cmd += u"\u2190"
                input = ""
                P = 0
                i=0
                for i in input:
                    I += i
                print('I')
                print(I)
                P -= 1
                #cmd = I[P]
                # print_cmd(cmd)
                sleep(10.0)
                #cmd = cmd[:-1]
            #print_cmd(cmd)                 # print the command (again)
        # If no No arrows, delete or exit sequence, the commands are updated in history and processed
        elif char in '\r':
            #print("\n")
            #updateHistory(cmd)              # History called and updated with cmd's
            p = ParseCmd(cmd)               # Parse is called and cmd's are broken down
            pdict = p.allCmdsDict
            PD = pdict
            for cmd in p.allCmds:           # pulls all cmd's from from Parser
                pass
            # Loop to call all functions requested by the user
            for F_IT in p.allCmds:
                if F_IT.cmd == 'cat':       # Concantenate
                    cat(**pdict)
                    #print('cat')
                    pass
                elif F_IT.cmd == 'cd':      # Change Directory
                    cd(**pdict)
                    #print(pdict)
                    #fs.cd(conn,table_name, pdict)
                    #print('cd')
                    #pass
                elif F_IT.cmd == 'chmod':   # Change Mode
                    chmod(**pdict)
                    #print('chMod')
                    pass
                elif F_IT.cmd == 'cp':      # Copy File
                    cp(**pdict)
                    #print('cp')
                    pass
                elif F_IT.cmd == 'grep':    # Grep File
                    grep(**pdict)
                    #print('grep')
                    #pass
                elif F_IT.cmd == 'head':    # Head of file
                    head(**pdict)
                    #print('head')
                    pass
                elif F_IT.cmd == 'history': # History
                    history(**pdict)
                    #print('history')
                    #pass
                elif F_IT.cmd == 'less':    # Less (Page at a time)
                    less(**pdict)
                    #print('less')
                    pass
                elif F_IT.cmd == 'ls':
                    ls(**pdict)
                    #print(**pdict)
                    #fs.list(conn, table_name, **pdict)
                    #print('ls')
                    #pass
                elif F_IT.cmd == 'mkdir':   # Make Directory
                    mkdir(**pdict)
                    #data = (12,0,'Bananas','2023-11-14 10:00:00','2023-11-14 10:00:00',0,'folder','user1','group6','rwxrwxrwx')
                    #fs.mkdir(f,table_name,kwargs=data)
                    #print('mkDir')
                    #pass
                elif F_IT.cmd == 'mv':      # Move File
                    mv(**pdict)
                    #print('mv')
                    pass
                elif F_IT.cmd == 'pwd':     # Current Working Directory
                    pwd(**pdict)
                    #fs.pwd()
                    #print('pwd')
                    #pass
                elif F_IT.cmd == 'rm':      # Remove File
                    rm(**pdict)
                    #pass
                elif F_IT.cmd == 'rmdir':   # Remove Empty Directory
                    rmdir(**pdict)
                    #print('rmDir')
                    pass
                elif F_IT.cmd == 'tail':    # End of File
                    tail(**pdict)
                    #print('tail')
                    pass
                elif F_IT.cmd == 'wc':      # Word Count
                    wc(**pdict)
                    #print('wc')
                    #pass
             #     sleep(1)
            cmd = ""                        # reset command to nothing (since we just executed it)
            print_cmd(cmd)                  # now print empty cmd prompt
        else:
            cmd += char                     # add typed character to our "cmd"
            print_cmd(cmd)                  # print the cmd out
