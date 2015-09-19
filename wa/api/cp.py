import sys

def main(args):
    import shutil
    import os
    
    def copytree(src, dst, symlinks=False, ignore=None):
        if not os.path.exists(dst):
            os.makedirs(dst)
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)

    if len(args) != 2:
        print("cp: Usage: cp <infile> <outfile>")
        sys.exit(1)
    copytree(args[0], args[1])

if __name__ == "builtins":
    main(sys.argv[1:])
