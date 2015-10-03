# coding=utf-8

import os
import sys
import shutil
import subprocess
import importlib
import importlib.machinery
import re
from tempfile import mkstemp
from jinja2 import Template
import yaml


class GeneratorAPI:

    def __init__(self, project_root):
        self.current_directory = os.path.abspath(os.getcwd())
        self.vars = {}
        self.temp_dir = os.path.join(
            '..', os.path.dirname(os.path.realpath(__file__)), 'temp')
        self.project_root = project_root

    def user_input(self, var):
        self.vars[var] = input(var + '=')

    def set(self, key, value):
        self.vars[key] = value

    def cd(self, directory):
        directory = os.path.abspath(directory)
        if directory[0] == '|':
            directory = os.path.join(self.project_root, directory[1:])
        os.chdir(directory)
        self.current_directory = directory

    def mkdir(self, directories):
        self.cd(self.current_directory)
        for directory in directories:
            if directory[0] == '|':
                directory = os.path.join(self.project_root, directory[1:])
            if not os.path.exists(directory):
                os.makedirs(directory)

    def touch(self, files):
        self.cd(self.current_directory)
        for file in files:
            if file[0] == '|':
                file = os.path.join(self.project_root, file[1:])
            if not os.path.exists(file):
                open(file, 'w').close()

    def rm(self, paths):
        self.cd(self.current_directory)
        for path in paths:
            if path[0] == '|':
                path = os.path.join(self.project_root, path[1:])
            if os.path.isdir(path):
                shutil.rmtree(path)
            elif os.path.isfile(path):
                os.remove(path)

    def cp(self, src, dst):
        self.cd(self.current_directory)
        if src[0] == '|':
            src = os.path.join(self.project_root, src[1:])
        if dst[0] == '|':
            dst = os.path.join(self.project_root, dst[1:])
        if os.path.isdir(src):
            copy_tree(src, dst)
        elif os.path.isfile(src):
            shutil.copy(src, dst)

    def cptpl(self, src, dst):
        self.cd(self.current_directory)
        if src[0] == '|':
            src = os.path.join(self.project_root, src[1:])
        if dst[0] == '|':
            dst = os.path.join(self.project_root, dst[1:])
        self.copy_tree_and_replace_vars(src, dst)

    def cptpljinja2(self, src, dst):
        self.cd(self.current_directory)
        if src[0] == '|':
            src = os.path.join(self.project_root, src[1:])
        if dst[0] == '|':
            dst = os.path.join(self.project_root, dst[1:])
        if os.path.isdir(src):
            copy_tree(src, self.temp_dir)
        elif os.path.isfile(src):
            shutil.copy(src, self.temp_dir)

        for root, subdirs, files in os.walk(self.temp_dir, topdown=False):
            for file in files:
                with open(os.path.join(root, file), 'r') as fp:
                    file_content = fp.read()
                with open(os.path.join(root, file), 'w') as fp:
                    t = Template(file_content)
                    fp.write(t.render(vars=self.vars))
                self.replace_d(os.path.join(root, file))
            for subdir in subdirs:
                self.replace_d(os.path.join(root, subdir))

        copy_tree(self.temp_dir, dst)
        # Очистить временную директорию
        shutil.rmtree(self.temp_dir)
        os.makedirs(self.temp_dir)

    def mv(self, src, dst):
        self.cp(src, dst)
        self.rm(src)

    def echo(self, args):
        for word in args:
            print(word, end='')
        print()

    def execute(self, cmd):
        self.cd(self.current_directory)
        subprocess.call(cmd)

    def py(self, filename, function):
        self.cd(self.current_directory)
        if filename[0] == '|':
            filename = os.path.join(self.project_root, filename[1:])
        loader = importlib.machinery.SourceFileLoader('tplconf', filename)
        external = loader.load_module()
        eval('external.' + fnc + '()')

    def copy_tree_and_replace_vars(self, src, dst):
        """
        Если передается директория в качестве аргумента, то будет
        рассматриваться как шаблон именно её содержимое!! Оно же и будет
        копироваться
        """
        if os.path.isdir(src):
            copy_tree(src, self.temp_dir)
        elif os.path.isfile(src):
            shutil.copy(src, self.temp_dir)

        for root, subdirs, files in os.walk(self.temp_dir, topdown=False):
            for file in files:
                self.replace_f(os.path.join(root, file))
            for subdir in subdirs:
                self.replace_d(os.path.join(root, subdir))
        copy_tree(self.temp_dir, dst)

        # Очистить временную директорию
        shutil.rmtree(self.temp_dir)
        os.makedirs(self.temp_dir)

    def replace_f(self, path, arg_name=None):
        """Replace files"""
        root, file = os.path.split(path)

        pattern = re.compile(r'(\<\<\<)([A-Za-z_]+)(\>\>\>)')
        file_path = path
        fh, abs_path = mkstemp()
        with open(abs_path, 'w') as new_file:
            with open(file_path) as old_file:
                for line in old_file:
                    for (o, var_name, c) in re.findall(pattern, line):
                        line = self.handle_args(line, var_name, arg_name)
                    new_file.write(line)
        os.close(fh)
        # Remove original file
        os.remove(file_path)
        # Move new file
        shutil.move(abs_path, file_path)

        pattern = re.compile(r'(\[\[)([A-Za-z_]+)(\]\])')
        for (o, var_name, c) in re.findall(pattern, file):
            file = self.handle_args(file, var_name, isfilename=True)
        os.rename(path, os.path.join(root, file))

    def replace_d(self, path, arg_name=None):
        """Replace directories
        Но в некоторых местах проекта может быть
        вызвана в тех местах, где нужно изменять
        имена файлов не трогая содержание
        """
        root, dir = os.path.split(path)
        pattern = re.compile(r'(\[\[)([A-Za-z_]+)(\]\])')
        for (o, var_name, c) in re.findall(pattern, dir):
            dir = self.handle_args(dir, var_name, arg_name, isfilename=True)
        os.rename(path, os.path.join(root, dir))

    def handle_args(self, line, var_name, arg_name=None, isfilename=False):
        if not (var_name in self.vars):
            self.user_input(var_name)
        if isfilename == False:
            line = re.sub('<<<' + var_name + '>>>', self.vars[var_name], line)
        else:
            line = re.sub(
                '\[\[' + var_name + '\]\]', self.vars[var_name], line)
        return line


def copy_tree(src, dst):
    """Copy directory tree"""
    for root, subdirs, files in os.walk(src):
        current_dest = root.replace(src, dst)
        if not os.path.exists(current_dest):
            os.makedirs(current_dest)
        for f in files:
            shutil.copy(os.path.join(root, f), os.path.join(current_dest, f))
