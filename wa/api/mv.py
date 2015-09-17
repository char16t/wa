import sys

def main(args):
    import shutil
    shutil.move(args[0], args[1])

if __name__ == "builtins":
    main(sys.argv[1:])
