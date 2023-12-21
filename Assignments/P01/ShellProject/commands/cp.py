from pathlib import Path
import shutil

def cp(**kwargs):

    sourceFile = str(kwargs.get('params')[0])
    sourcePath = Path.cwd() + '/' + sourceFile
    if len(kwargs.get('params')) > 1:
        destinationFile = str(kwargs.get('params')[1])
    destinationPath = Path.cwd()

    try:
        shutil.copy(sourcePath, destinationPath)
        pass
    except shutil.SameFileError:
        print("\nError: Source and Destination are the same.")
        pass
    except PermissionError:
        print("\nError: Permission denied.")
        pass
    except:
        print("\nError: Copying failed.")
        pass
