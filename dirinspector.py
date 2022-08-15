import configparser
from os import listdir as ls
from os.path import abspath, isdir
from sys import argv
argv.append("")

conf = configparser.ConfigParser()
conf.read(f'{__file__[:__file__.rfind("/")-len(__file__)+1]}config.ini')

def check_format(file, formats) -> bool:
    for form in formats:
        return "."+form in file

def main():
    directory = (abspath('')+"/", ls(abspath('')+"/"))
    files = [["Hidden", 245, []], ["Image", 226, []], ["Video", 208, []],
             ["Audio", 124, []], ["Document", 255, []], ["Archive", 81, []],
             ["Code", 10, []], ["Directory", 27, []], ["Etc", 93, []]
    ]
    for file in directory[1]:
        if '.' == file[0]:
            if argv[1].upper() == "-A":
                files[0][2].append(file)
        elif check_format(file, conf['formats']['image'].split(' , ')):
            files[1][2].append(file)
        elif check_format(file, conf['formats']['video'].split(' , ')):
            files[2][2].append(file)
        elif check_format(file, conf['formats']['audio'].split(' , ')):
            files[3][2].append(file)
        elif check_format(file, conf['formats']['document'].split(' , ')):
            files[4][2].append(file)
        elif check_format(file, conf['formats']['archive'].split(' , ')):
            files[5][2].append(file)
        elif check_format(file, conf['formats']['code'].split(' , ')):
            files[6][2].append(file)
        else:
            if isdir(file):
                files[7][2].append(file)
            else:
                files[8][2].append(file)
    print(f"\033[38;5;10mDirectory: {directory[0]}\033[0;0m")
    for file_type in files:
        if file_type[2]:
            file_type[2].sort()
            print(f"\033[38;5;{file_type[1]}m--[{file_type[0]}]--\033[0;0m")
            for file in file_type[2]:
                print(f"\033[38;5;{file_type[1]}m{file}\033[0;0m")

if __name__ == "__main__":
    main()