import sys

def main(files):
    import os
    for fname in files:
        fhandle = open(fname, 'a')
        try:
            os.utime(fname, None)
        finally:
            fhandle.close()

if __name__ == "builtins":
    main(sys.argv[1:])
