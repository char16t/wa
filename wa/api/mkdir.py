import os
import sys

def main(directories):
    for directory in directories:
        if not os.path.exists(directory):
                os.makedirs(directory)

if __name__ == "__main__":
    main(sys.argv[1:])
