# coding=utf-8

import sys
import os
import re

variables = {}

def main(in_args):
    if len(in_args) >= 1:
        command_file, args = get_command_file(in_args)
        execute_command(command_file, args)

def execute_command(command_file, args = None):
    if args == None:
        args = [command_file]
    else:
        args = [command_file] + args

    if command_file != None:
        if command_file[-2:] == "py":
            saved_argv = sys.argv
            sys.argv = args
            exec(compile(open(command_file, "rb").read(), command_file, 'exec'),
            {}, {})
            sys.argv = saved_argv
        elif command_file[-2:] == "wa":
            with open(command_file) as o:
                for line in o.readlines():
                    line = variables_substitution(line)
                    main(line.split())
    else:
        print("Command not found")

def get_command_file(argv_list):
    current_directory = os.path.join(os.path.expanduser("~"), ".wa") 
    counter = 0
    for arg in argv_list:
        if os.path.isfile(os.path.join(current_directory, arg + ".py")):
            return (os.path.join(current_directory, arg + ".py"),
            argv_list[counter+1:])
        if os.path.isfile(os.path.join(current_directory, arg + ".wa")):
            return (os.path.join(current_directory, arg + ".wa"),
            argv_list[counter+1:])

        current_directory = os.path.join(current_directory, arg)
        if not os.path.exists(current_directory):
            break
        counter += 1

    if os.path.isfile(os.path.abspath(os.path.join(os.path.dirname(__file__), "api",
        argv_list[0] + ".py"))):
        return (os.path.abspath(os.path.join(os.path.dirname(__file__), "api", argv_list[0] +
        ".py")), argv_list[1:])
    else:
        return (None, None)

    return (None, None)

def variables_substitution(line):
    global variables
    for var in variables:
       line = line.replace('${'+var+'}', variables[var]) 
    return line

if __name__ == "__main__":
    main(sys.argv[1:])
