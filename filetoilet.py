import configparser
from os import listdir as ls
from os import replace as move
from os.path import abspath, isdir

conf = configparser.ConfigParser()
conf.read(f'{__file__[:__file__.rfind("/")-len(__file__)+1]}config.ini')

def check_format(file, formats) -> bool:
    for form in formats:
        return "."+form in file

def main():
    to_sort = (abspath('')+"/", ls(abspath('')+"/"))
    try:
        for file in to_sort[1]:
            try:
                u_file = f"{to_sort[0]}{file}"
                if check_format(file, conf['paths']['image'].split(' , ')):
                    print(f"Image: {u_file}")
                    move(u_file, conf['sorted']['image']+file)
                elif check_format(file, conf['paths']['video'].split(' , ')):
                    print(f"Video: {u_file}")
                    move(u_file, conf['sorted']['video']+file)
                elif check_format(file, conf['paths']['audio'].split(' , ')):
                    print(f"Audio: {u_file}")
                    move(u_file, conf['sorted']['audio']+file)
                elif check_format(file, conf['paths']['document'].split(' , ')):
                    print(f"Document: {u_file}")
                    move(u_file, conf['sorted']['document']+file)
                elif check_format(file, conf['paths']['archive'].split(' , ')):
                    print(f"Archive: {u_file}")
                    move(u_file, conf['sorted']['archive']+file)
                else:
                    if isdir(u_file):
                        print(f"Directory: {u_file}")
            except PermissionError:
                print(f"Permission denied: {u_file}")
    except PermissionError:
        print(f"Permission denied: {to_sort}")

if __name__ == "__main__":
    main()
