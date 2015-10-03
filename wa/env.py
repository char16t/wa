# coding=utf-8

import os
import wa.api


class Environment():

    def __init__(self):
        self.manifest = None
        self.project_root = None
        self.api = wa.api.GeneratorAPI(self.project_root)

    def set_project_root(self, path):
        if path != None:
            self.project_root = path
            if os.path.isfile(os.path.join(path, '.wa')):
                self.manifest = os.path.join(path, '.wa')
            elif os.path.isfile(os.path.join(os.path.expanduser('~'), '.wa')):
                self.manifest = os.path.join(os.path.expanduser('~'), '.wa')
            self.api = wa.api.GeneratorAPI(self.project_root)

    def run(self, cmd):
        cmd = self.get_variables_values(cmd)
        arguments = cmd.split(' ')
        if arguments[0] == 'mkdir':
            self.api.mkdir(arguments[1:])
        elif arguments[0] == 'input':
            self.api.user_input(arguments[1])
        elif arguments[0] == 'set':
            self.api.set(arguments[1], arguments[2])
        elif arguments[0] == 'cd':
            self.api.cd(arguments[1])
        elif arguments[0] == 'touch':
            self.api.touch(arguments[1:])
        elif arguments[0] == 'rm':
            self.api.rm(arguments[1:])
        elif arguments[0] == 'cp':
            self.api.cp(arguments[1], arguments[2])
        elif arguments[0] == 'cptpl':
            self.api.cptpl(arguments[1], arguments[2])
        elif arguments[0] == 'cptpljinja2':
            self.api.cptpljinja2(arguments[1], arguments[2])
        elif arguments[0] == 'mv':
            self.api.mv(arguments[1], arguments[2])
        elif arguments[0] == 'echo':
            self.api.echo(arguments[1:])
        elif arguments[0] == 'exec':
            self.api.execute(arguments[1:])
        elif arguments[0] == 'py':
            # работает странно, не исключаю что оно будет
            # исполнять всё что находится вне функций в файле
            # или всё, что запускается если __name__ == __main__
            self.api.py(arguments[1], arguments[2])

    def get_variables_values(self, cmd):
        for var in self.api.vars:
            try:
                cmd = cmd.replace('${' + var + '}', self.api.vars[var])
            except:
                continue
        return cmd


def copy_tree(src, dst):
    """Copy directory tree"""
    for root, subdirs, files in os.walk(src):
        current_dest = root.replace(src, dst)
        if not os.path.exists(current_dest):
            os.makedirs(current_dest)
        for f in files:
            shutil.copy(os.path.join(root, f), os.path.join(current_dest, f))
