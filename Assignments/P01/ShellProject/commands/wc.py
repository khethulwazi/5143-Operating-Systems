"""The Linux wc command calculates a file's word, 
    line, character, or byte count.
"""
import os

def wc(**kwargs):
    
    infileName = str(kwargs.get('params')).strip('[]').strip('\'\'')
    # creating variable to store the
    # number of words
    lineCount = 0
    byteCount = 0

    with open(infileName,'r') as file:
        #return the absolute path of the file
        path = os.path.abspath(infileName)
        #counts the bytes in the file
        byteCount = os.path.getsize(path)
        print("Path: ", path)
        print("byteCount: ", byteCount)
        # Reading the content of the file
        # using the read() function and storing
        # them in a new variable
        data = file.read()

        # Splitting the data into separate lines
        # using the splitlines() function
        lineCount = len(data.splitlines())
        print("lineCount = ", lineCount)
        # Splitting the data into separate words
        # using the split() function
        words = len(data.split())
        print("words = ", words)
        # Printing total number of words
        print(lineCount, words, byteCount, infileName)
