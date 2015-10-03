# coding=utf-8

import os
import sys
import yaml


def parse_args(envirnment, arguments):
    manifest = envirnment.manifest
    try:
        with open(manifest, 'r') as stream:
            available_arguments = yaml.load(stream)
    except:
        print('An error occurred while attempting to open the Manifest-file.')
        sys.exit()
    else:
        for argument in arguments:
            if available_arguments != None:
                if argument in available_arguments:
                    value = available_arguments[argument]
                    available_arguments = available_arguments[argument]
                else:
                    # print('This command is not available. Try again.')
                    # sys.exit()
                    alternate_parse_args(envirnment, arguments)
                    return
            else:
                alternate_parse_args(envirnment, arguments)
                return
        if type(value) is list:
            for v in value:
                envirnment.run(v)
        elif not type(value) is dict:
            envirnment.run(value)
        else:
            print('This command is not available. Try again.')
            sys.exit()

# Поиск команды в конфигурации из домашней директории, если такая
# есть.


def alternate_parse_args(envirnment, arguments):
    manifest = os.path.join(os.path.expanduser('~'), '.wa')
    try:
        with open(manifest, 'r') as stream:
            available_arguments = yaml.load(stream)
    except:
        print('An error occurred while attempting to open the Manifest-file.')
        sys.exit()
    else:
        for argument in arguments:
            if available_arguments != None:
                if argument in available_arguments:
                    value = available_arguments[argument]
                    available_arguments = available_arguments[argument]
                else:
                    print('This command is not available. Try again.')
                    sys.exit()
            else:
                print('This command is not available. Try again.')
                sys.exit()
        if type(value) is list:
            for v in value:
                envirnment.run(v)
        elif not type(value) is dict:
            envirnment.run(value)
        else:
            print('This command is not available. Try again.')
            sys.exit()

# А что если пользовательская папка является корнем файловой системы? Баг?


def find_manifest(path=os.getcwd()):
    if not os.path.isfile(os.path.join(path, '.wa')) and os.path.dirname(path) != os.path.dirname(os.path.expanduser('~')):
        if os.path.dirname(path) == path:
            # you have yourself root.
            # works on Windows and *nix paths.
            # does NOT work on Windows shares (\\server\share)

            # If .wa not found, but exist in <home path>
            # current dir will be a project root
            if os.path.isfile(os.path.join(os.path.expanduser('~'), '.wa')):
                touch('.wa')
                return '.'
            else:
                print(os.path.join(os.path.expanduser('~'), '.wa'))
                print('Manifest-file not found')
                sys.exit()
        path = os.path.abspath(os.path.join(path, os.pardir))
        return find_manifest(path)
    else:
        return path


def touch(fname):
    if os.path.exists(fname):
        os.utime(fname, None)
    else:
        open(fname, 'a').close()
