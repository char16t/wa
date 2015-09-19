import sys

def main(vars):
    import os
    import pickle
    for var in vars:
        variables = {}
        var_value = input(var + ": ")
        variables[var] = var_value

if __name__ == "builtins":
    main(sys.argv[1:])
