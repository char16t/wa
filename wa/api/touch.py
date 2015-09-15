import os
import sys

def main(files):
    for fname in files:
        fhandle = open(fname, 'a')
        try:
            os.utime(fname, None)
        finally:
            fhandle.close()

if __name__ == "__main__":
    main(sys.argv[1:])
