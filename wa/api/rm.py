import sys
import os
import shutil

def main(args):
    for arg in args:
        if os.path.isfile(os.path.abspath(arg)):
            os.remove(os.path.abspath(arg))
        if os.path.isdir(os.path.abspath(arg)):
            shutil.rmtree(os.path.abspath(arg))

if __name__ == "__main__":
    main(sys.argv[1:])
