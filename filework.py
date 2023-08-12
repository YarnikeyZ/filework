from utils import *

def main():
    try:
        sortFilesByFormat()
        printOrMoveSortedFiles()
    except PermissionError:
        print(f"Permission denied")

if __name__ == "__main__":
    main()
