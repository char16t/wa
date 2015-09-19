import sys

def main(vars):
    import os
    import pickle
    import hashlib
    
    pickle_hash = hashlib.md5()
    pickle_hash.update(os.getcwd().encode())
    pickle_dump = os.path.join(os.path.expanduser("~"), ".wa", "_wa_temp", pickle_hash.hexdigest())

    for var in vars:
        try:
            variables = pickle.load(open(pickle_dump, "rb"))
            var_value = input(var + ": ")
            variables[var] = var_value
            pickle.dump(variables, open(pickle_dump, "wb"))
        except EOFError:
            variables = {} 
            var_value = input(var + ": ")
            variables[var] = var_value
            pickle.dump(variables, open(pickle_dump, "wb"))

if __name__ == "builtins":
    main(sys.argv[1:])
