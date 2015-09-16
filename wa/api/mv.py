import sys
import shutil

def main(args):
    shutil.move(args[0], args[1])

if __name__ == "__main__":
    main(sys.argv[1:])
