import configparser
import platform
import argparse
from os import listdir as ls
from os.path import abspath, isdir

class FileType:
    def __init__(self, typeName, colorCode, fileList) -> None:
        self.typeName = typeName
        self.colorCode = colorCode
        self.fileList = fileList

    def __str__(self) -> str:
        return f"{self.typeName=}, {self.colorCode=}, {self.fileList=}"

    def addFile(self, fileName) -> None:
        self.fileList.append(fileName)

def checkFormat(file, formats) -> bool:
    for form in formats.split(', '):
        if file[-len(form)-1:] == '.'+form:
            return True

def sortFilesByFormat() -> None:
    for file in directory[1]:
        if '.' == file[0] and showall:
            continue
        if isdir(file):
            fileTypes['Directory'].addFile(file)
        elif checkFormat(file, configFileTypes['image']):
            fileTypes['Image'].addFile(file)
        elif checkFormat(file, configFileTypes['video']):
            fileTypes['Video'].addFile(file)
        elif checkFormat(file, configFileTypes['audio']):
            fileTypes['Audio'].addFile(file)
        elif checkFormat(file, configFileTypes['document']):
            fileTypes['Document'].addFile(file)
        elif checkFormat(file, configFileTypes['archive']):
            fileTypes['Archive'].addFile(file)
        elif checkFormat(file, configFileTypes['code']):
            fileTypes['Code'].addFile(file)
        else:
            fileTypes['Etc'].addFile(file)

def printSortedFiles() -> None:
    print(f"Directory: {directory[0]}") if stdout else print(f"\033[38;5;10mDirectory: {directory[0]}\033[0;0m")
    for fileType in fileTypes:
        fileType = fileTypes[fileType]
        if fileType.fileList:
            fileType.fileList.sort()
            print(f"--[{fileType.typeName}]--") if stdout else print(f"\033[38;5;{fileType.colorCode}m--[{fileType.typeName}]--\033[0;0m")
            for file in fileType.fileList:
                print(file) if stdout else print(f"\033[38;5;{fileType.colorCode}m{file}\033[0;0m")

def main() -> None:
    global configFileTypes, showall, stdout, fileTypes, directory

    # Config reading
    pathSymbol = '/' if platform.system() == "Linux" else '\\'
    fullPath = __file__
    lastPathSymbol = fullPath.rfind(pathSymbol)

    conf = configparser.ConfigParser()
    conf.read(f'{fullPath[:lastPathSymbol-len(fullPath)+1]}config.ini')

    # Setting up/Reading args
    argparser = argparse.ArgumentParser(prog='dirinspector', description='Shows files like "ls" or "dir"')
    
    argparser.add_argument('-a', '--showall', default=False, action='store_true', help='show all files (show hidden ones)')
    argparser.add_argument('-s', '--stdout', default=False, action='store_true', help='print to console without color')
    
    args = argparser.parse_args()
    
    # Setting up variables and file types
    directory = (abspath('')+pathSymbol, ls(abspath('')+pathSymbol))
    configFileTypes = dict(conf['formats'])
    stdout = args.stdout
    showall = not args.showall

    fileTypes = {
        'Hidden': FileType('Hidden', 245, []),
        'Image': FileType('Image', 226, []),
        'Video': FileType('Video', 208, []),
        'Audio': FileType('Audio', 124, []),
        'Document': FileType('Document', 255, []),
        'Archive': FileType('Archive', 81, []),
        'Code': FileType('Code', 10, []),
        'Directory': FileType('Directory', 27, []),
        'Etc': FileType('Etc', 93, [])
    }

    # Doing what we wanna do
    sortFilesByFormat()
    printSortedFiles()

if __name__ == "__main__":
    main()
