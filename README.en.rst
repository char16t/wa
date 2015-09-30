wa
==

.. image:: https://badge.fury.io/py/wa.svg
    :target: https://pypi.python.org/pypi/wa

**The current version of wa is still under development. This is an alpha version and it is very likely to contain errors. It is recommended to use Python 3.x, work in Python 2 has not yet been tested.**

wa (workflow automation) — simple cross-platform tool created to automate routine tasks in the development process. For example, it can be used to quickly create a skeleton project from a previously created template or perform complex tasks in a single command.

The goal of wa is to allow us to share best practice in software development and simplify the reuse of code in their software projects. The manifest file in YAML format contains the commands and corresponding actions, and preparation of the source code files are stored as templates. The manifest and templates can be distributed along the source code of your project.

.. contents:: Conents
   :depth: 3

Installation
------------
Using pip

.. code-block:: bash
    
    pip install wa

Using easy_nstall

.. code-block:: bash
    
    easy_install wa

from source code

.. code-block:: bash
    
    git clone https://github.com/char16t/wa.git
    cd wa
    make install

Quick start
-------------
wa may be called from console

.. code-block:: bash
    
    wa
    wa: workflow automation tool
    
wa takes as command arguments, which are mapped to actions. Describing one command :code:`startproject` you can call it as follows:

.. code-block:: bash
    
    wa startproject

Commands unlimited nesting are supported. You can also describe the commands :code:`python startproject`, :code:`startproject cpp` or :code:`startproject cpplib`. You can call them so:

.. code-block:: bash
    
    wa startproject python
    wa startproject cpp
    
The commands are described in the files :code:`.wa` in YAML format. For the examples above it might look like this:

.. code-block:: yaml

    startproject:
        python:
            - input PROJECTNAME
            - mkdir ${PROJECTNAME}
            - mkdir ${PROJECTNAME}/tests ${PROJECTNAME}/${PROJECTNAME}
            - touch ${PROJECTNAME}/tests/__init__.py
            - touch ${PROJECTNAME}/${PROJECTNAME}/__init__.py
        cpp:
            - input PROJECTNAME
            - mkdir ${PROJECTNAME}
            - mkdir ${PROJECTNAME}/src ${PROJECTNAME}/tests ${PROJECTNAME}/include
            - touch ${PROJECTNAME}/CMakeLists.txt
            - touch ${PROJECTNAME}/src/${PROJECTNAME}.cpp
            - touch ${PROJECTNAME}/include/${PROJECTNAME}.hpp
        cpplib:
            - cp /home/user/mypath/templates/cpplib .

The file :code:`.wa` can be located in the root of your project and in your home directory. wa will first try to do a search of the requested command in the root of your project, and then, if the command is not found, will return to the file :code:`.wa` in your home directory and looks for  there. That is, by creating the file :code:`.wa` as in the above example in your home directory, you will be able to perform

.. code-block:: bash
    
    $ wa startproject python

You are prompted to enter a value for the variable :code:`PROJECTNAME`
    
.. code-block:: bash
    
    $ wa startproject python
    $ PROJECTNAME=_

Let it be :code:`helloworld`:

.. code-block:: bash
    
    $ wa startproject python
    $ PROJECTNAME=helloworld

and deploy the skeleton of a Python project :code:`helloworld` in any directory. Please note that in the current directory, perhaps it should also create an empty file :code:`.wa`. It will be a signal to wa that it is the root of the project. Now, if you go in a subdirectory of the current directory and attempt to execute an arbitrary command, the search will be done first in that file that is one level higher in the directory tree.

wa does exactly that: search a file in the current directory first, then in the directory above and so on until the root file system. If the file is :code:`.wa` was not found, the search will continue in your home directory.

In the file :code:`.wa` lying at the root of your project you can override any command (for example, :code:`python startproject` from the listings above). That is, you can redistribute it and :code:`.wa`-file along with the code of your project and to help other developers, for example, to quickly create the skeleton of the class, formatted according to the standards of the project.

wa also allows you to work with files and directories relative to the root of your project. By specifying a vertical line before the path to the file or directory

.. code-block:: yaml
    
    newclass:
        - input CLASSNAME
        - cp |.code_templates/class.cpp |src/${CLASSNAME}.cpp
        - cp |.code_templates/header.cpp |include/${CLASSNAME}.hpp
        

In the execution of the above example copies the file :code:`.code_templates/class.cpp` and :code:`.code_templates/header.hpp` with the specified name in the directory :code:`src` and :code:`include`, respectively. The main thing here is that you can be in any directory of your project, but a copy will be made relative to the root project, because it is explicitly specified with a vertical bar :code:`|`.

In the example below, a vertical bar at the beginning of the second there are no arguments

.. code-block:: yaml
    
    newclass:
        - input CLASSNAME
        - cp |.code_templates/class.cpp ${CLASSNAME}.cpp
        - cp |.code_templates/header.cpp ${CLASSNAME}.hpp

When running this example will copy all the files with the specified names in the current directory. For example, if you are in the directory :code:`my_great_cpp_app/legacy`, the files will be copied into it, and if you're in :code:`my_great_cpp_app/legacy/tests` on it.

A vertical bar at the beginning of the paths to files and folders can be used in any commands.


The available commands (API)
----------------------------

You can use the following commands. For each command an example of using.

set
~~~
:code:`set <variable> <value>` sets the value for the variable. After that, in any commands, you can use a variable like :code:`${variable}`. The variable names are defined case-sensitive.

.. code-block:: yaml
    
    create_file_and_directory:
        - set PREFIX mysuperpupuer
        - touch ${PREFIX}_file.txt
        - mkdir ${PREFIX}_dir

input
~~~~~
:code:`input <variable>` requests for input from the user variable

.. code-block:: yaml
    
    startproject:
        - input PROJECTNAME
        - mkdir ${PROJECTNAME}
        - touch ${PROJECTNAME}/README.txt

cd
~~
:code:`cd <path>` goes to the specified path.

.. code-block:: yaml
    
    startproject:
        - input PROJECTNAME
        - mkdir ${PROJECTNAME}
        - cd ${PROJECTNAME}
        - touch README.txt

mkdir
~~~~~
:code:`mkdir <directory name> [<directory name> [<directory name>]]` creates dirs with the specified names.

.. code-block:: yaml
    
    mkdirs:
        - mkdir one two three/four

touch
~~~~~
:code:`touch <file name> [<file name> [<file name>]]` creates files with the specified names

.. code-block:: yaml
    
    touchs:
        - touch one two three/four

rm
~~
:code:`rm <file or directory name> [<file or directory name> [<file or directory name>]]` removes files and folders with the specified names.

.. code-block:: yaml
    
    clean:
        - rm build
        - rm dist

cp
~~
:code:`cp <source> <target>>` copies from source to target.

.. code-block:: yaml
    
    license:
        - input LICENSE_NAME
        - cp /home/user/templates/${LICENSE_NAME}.template |LICENSE

cptpl
~~~~~
:code:`cptpl <source> <target>` copies from source to target with replacement :code:`[[variable]]` on the value of the variable in file names and folders and :code:`<<<variable>>>` the value of the variable in the contents of the files.

.. code-block:: yaml
    
    license:
        - input PROJECT_NAME PROJECT_DESCRIPTION PROJECT_LICENSE
        - cptpl /home/user/templates/cpp_lib |.

The first argument specifies the folder that contains the template, and the second argument the path where the template will be copied. For example, for the Python project template might look like this: create directory :code:`/home/user/templates/python` with the following content

.. code-block::
    
    [[PROJECT_NAME]]
        __init__.py
        [[PRPJECT_NAME]].py
    tests
        __init__.py

Insert to file :code:`[[PRPJECT_NAME]].py` this content:

.. code-block::
    
    # This file is a part of <<<PROJECT_NAME>>>
    # Licensed under MIT. See LICENSE file for details
    # (c) 2015 <<<AUTHOR_NAME>>> <<<<AUTHOR_EMAIL>>>>
    
    def main():
        pass
        
    if __name__ == "__main__":
        main()

Now when you call wa will be prompted to enter the values of the variables, and then the template will be copied. It looks like :code:`.wa`-file

.. code-block:: yaml
    
    pyscaffold:
        - cptpl /home/user/templates/python |.


Please note that in the example above are not required to ask the user to input the required variables. The prompt will happen automatically as soon as encountered unknown variable.

Now you need to run in console

.. code-block:: bash

    $ wa pyscaffold
    $ PROJECT_NAME=helloworld
    $ PROJECT_AUTHOR=Foo Bar
    $ AUTHOR_EMAIL=foo@bar.com

As a result, it will create the following directory structure

.. code-block::
    
    helloworld
        __init__.py
        helloworld.py
    tests
        __init__.py

And the file :code:`helloworld/helloworld.py` will have the following content

.. code-block::
    
    # This file is a part of helloworld
    # Licensed under MIT. See LICENSE file for details
    # (c) 2015 Foo Bar <foo@bar.com>
    
    def main():
        pass
        
    if __name__ == "__main__":
        main()

cptpljinja2
~~~~~~~~~~~
:code:`cptpljinja2 <source> <destination>>` copy from source to target with replacement :code:`[[variable]]` on the value of the variable in file names and folders and compiles content from Jinja2 templates that are in the source files.

.. code-block:: yaml
    
    license:
        - input PROJECT_NAME PROJECT_DESCRIPTION PROJECT_LICENSE
        - cptpljinja2 /home/user/templates/cpp_lib |.

mv
~~
:code:`mv <source> <destination>` moves the files and folders from source to destination..

.. code-block:: yaml
    
    to_legacy:
        - input CLASS
        - mv |src/${CLASS}.cpp |legacy/src/${CLASS}.cpp
        - mv |include/${CLASS}.hpp |legacy/include/${CLASS}.hpp

echo
~~~~
:code:`echo <message>` displays a message on the screen.

.. code-block:: yaml
    
    copy_large_file:
        - cp /home/12Gb.raw |.
        - echo Ok, copied

exec
~~~~
:code:`exec <command>` executes the command on the command line of the operating system.

.. code-block:: yaml
    
    test:
        - cd |.
        - exec make test

py
~~
:code:`py <file name> <function>` execute function from file in Python interpreter.

.. code-block:: yaml
    
    test:
        - cd |.
        - py runtests.py main


Issues
------
About any errors, problems, any questions or with any suggestions you can write to v.manenkov (at) gmail.com or create a issue in Github Issues https://github.com/char16t/wa/issues

License
-------
Source code licensed under MIT. Текст лицензии находится в файле LICENSE. The license text is in the LICENSE file.
