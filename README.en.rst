==
wa
==
Workflow automation tool

Avaiable on PyPI: https://pypi.python.org/pypi/wa/0.1.0

Python 3.x only tested! This is alpha version

wa (workflow automation) — simple cross-platform tool created to automate routine tasks in the development process. For example, it can be used to quickly create a skeleton project from a previously created template or perform complex tasks in a single command.

 	
The goal of wa is to allow us to share best practice in software development and simplify the reuse of code in their software projects. The manifest file in YAML format contains the commands and corresponding actions, and preparation of the source code files are stored as templates. The manifest and templates can be distributed along the source code of your project.


Installation
------------

.. code-block:: bash

    $ pip install wa

        
To verify that the installation was successful by executing from the console

.. code-block:: bash

    $ wa
    $ wa: workflow automation tool

    
Usage
-----

Consider the example manifest-file. In the simplest case you can do a single file `.wa` with the following content:

.. code-block:: yaml
    
    start:
        project:
            - input projectname
            - mkdir ${projectname}

 	
wa will look for the file `.wa` in the current directory. If not, will rise to a higher level in the directory tree and will continue to seek `.wa` there, and so on until you get to the root of the file system. Thus there is a limit &mdash; the file `.wa` in your home directory will be ignored, but if in other places the file is not found wa will use the manifest file from the home directory. In this case, your current directory will be perceived as project root.

In the same directory run:

.. code-block:: bash
    
    $ wa start project
    $ projectname = helloworld
    
Directory `helloworld` will be created  

API
---

You can use the following commands:

 * :code:`set <variable> <value>` sets the value for the variable. After this in any commands, you can use a variable as :code:`${variable}`. The variable names are defined case-sensitive.
 * :code:`input <variable>`  	requests for input from the user variable
 * :code:`cd <path>` goes to the specified path.
 * :code:`mkdir <dir name> [<dir name> [<dir name>]]` creates folders with the specified names.
 * :code:`touch <file> [<file> [<file>]]` creates files with the specified names.
 * :code:`rm <file or directory name> [<file or directory name> [<file or directory name>]]` removes files and folders with the specified names.
 * :code:`cp <source> <target>` copies from source to target.
 * :code:`cptpl <source> <target>` copies from source to target with replacement :code:`[[variable]]` on the value of the variable in file names and folders and :code:`<<<variable>>>` the value of the variable in the contents of the files.
 * :code:`cptpljinja2 <source> <destination>` copy from source to target with replacement :code:`[[variable]]` on the value of the variable in file names and folders and compiles content from Jinja2 templates that are in the source files.
 * :code:`mv <source> <destination>` moves the files and folders from source to destination.
 * :code:`echo <message>` displays a message on the screen.
 * :code:`exec <command>` executes the command on the command line of the operating system.
 * :code:`py <file name> <function>` function from file in Python interpreter.
 
Notes: :code:`mkdir |hello` means creating a folder :code:`hello` in the root of the project. The vertical bar at the beginning of the argument means the root of the project in other commands similarly.
