from pathlib import Path

def head(**kwargs):
    #print(kwargs)
    #print(kwargs.get('params')[-1])
    n = 10
    path = str(Path.cwd()) + '/' + kwargs.get('params')[-1]
    with open(path) as inFile:
        head = [next(inFile) for _ in range(n)]
    print(*head)
