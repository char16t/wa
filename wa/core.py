# coding=utf-8

import sys
import os

def main():
    if len(sys.argv) > 1:
        command_file = get_command_file(sys.argv[1:])
        execute_command(command_file)

def execute_command(command_file):
    if command_file != None:
        if command_file[-2:] == "py":
            with open(command_file) as o:
                exec(o.read())
        elif command_file[-2:] == "wa":
            with open(command_file) as o:
                for line in o.readlines():
                    execute_command(get_command_file(line.split()))
    else:
        print("Command not found")

def get_command_file(argv_list):
    current_directory = os.path.join(os.path.expanduser("~"), ".wa") 
    counter = 0
    for arg in argv_list[:-1]:
        if os.path.isfile(os.path.join(current_directory, arg + ".py")):
            return os.path.join(current_directory, arg + ".py")
        if os.path.isfile(os.path.join(current_directory, arg + ".wa")):
            return os.path.join(current_directory, arg + ".wa")

        current_directory = os.path.join(current_directory, arg)
        if not os.path.exists(current_directory):
            return None
        counter += 1

    py_command_file = os.path.join(current_directory, argv_list[-1] + ".py")
    wa_command_file = os.path.join(current_directory, argv_list[-1] + ".wa")
    if os.path.isfile(py_command_file):
        return py_command_file
    elif os.path.isfile(wa_command_file):
        return wa_command_file
    else:
        return None

if __name__ == "__main__":
    main()
