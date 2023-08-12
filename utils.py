from os.path import abspath, isdir
from os import listdir as ls
from os import replace as move
import configparser
import platform
import argparse

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
    """
    Checks file for having one of given formats.
    """
    for form in formats.split(', '):
        if file[-len(form)-1:] == '.'+form:
            return True

def sortFilesByFormat() -> None:
    """
    Sorts files by their type.
    """
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

def printOrMoveSortedFiles() -> None:
    """
    Prints and can move sorted files.
    """
    print(f"Directory: {directory[0]}") if stdout else print(f"\033[38;5;10mDirectory: {directory[0]}\033[0;0m")
    for fileType in fileTypes:
        if sortthem and fileType == "Directory" or fileType == "Etc":
            continue
        fileType = fileTypes[fileType]
        if fileType.fileList:
            fileType.fileList.sort()
            print(f"--[{fileType.typeName}]--") if stdout else print(f"\033[38;5;{fileType.colorCode}m--[{fileType.typeName}]--\033[0;0m")
            for file in fileType.fileList:
                u_file = f"{directory[0]}{file}"
                if sortthem:
                    move(u_file, configPaths[fileType.typeName.lower()]+file)
                print(file) if stdout else print(f"\033[38;5;{fileType.colorCode}m{file}\033[0;0m")

# Config reading
pathSymbol = '/' if platform.system() == "Linux" else '\\'
fullPath = __file__
lastPathSymbol = fullPath.rfind(pathSymbol)

conf = configparser.ConfigParser()
conf.read(f'{fullPath[:lastPathSymbol-len(fullPath)+1]}config.ini')

# Setting up/Reading args
argparser = argparse.ArgumentParser(prog='filework', description='Shows files like "ls" or "dir" but can sort them in folders.')

argparser.add_argument('-a', '--showall', default=False, action='store_true', help='show all files (show hidden ones)')
argparser.add_argument('-c', '--coloroff', default=False, action='store_true', help='print to console without color')
argparser.add_argument('-s', '--sortthem', default=False, action='store_true', help='sorts files to their corresponding categories')

args = argparser.parse_args()

# Setting up variables and file types
configFileTypes = dict(conf['formats'])
configPaths = dict(conf['paths'])
stdout = args.stdout
showall = not args.showall
sortthem = args.sortthem
directory = (abspath('')+pathSymbol, ls(abspath('')+pathSymbol))

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
