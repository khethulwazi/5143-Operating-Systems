from collections import deque

def tail(**kwargs):

    n = 10
    fileName = str(kwargs.get('params')[-1])        #.strip('[]').strip('\'\'')
    flags = kwargs.get('flags')
    if n in flags:
        n = kwargs.get('params')[0]
        print('\n',*deque(open(fileName), n))  
    else:
        print('\n',*deque(open(fileName), n))
