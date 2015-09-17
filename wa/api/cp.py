import sys

def main(args):
    import shutil
    if len(args) != 2:
        print("cp: Usage: cp <infile> <outfile>")
        sys.exit(1)
    shutil.copyfile(args[0], args[1])

if __name__ == "builtins":
    main(sys.argv[1:])
