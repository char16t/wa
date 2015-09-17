import sys

def main(directories):
    import os
    for directory in directories:
        if not os.path.exists(directory):
                os.makedirs(directory)

if __name__ == "builtins":
    main(sys.argv[1:])
