wa
==

.. image:: https://badge.fury.io/py/wa.svg
    :target: https://pypi.python.org/pypi/wa

**Текущаяя версия wa находится в стадии разработки. Это альфа-версия и она с большой долей вероятности может содержать ошибки. Рекомендуется использовать Python 3.x, работа в Python 2 пока не протестирована.**

wa (от workflow automation) — простой кроссплатформенный инструмент, созданный для автоматизации рутинных задач в процессе разработки. Например, его можно использовать для быстрого создания каркаса проекта из ранее созданного шаблона или выполнения сложной задачи в одну команду.

Цель wa — позволить делиться лучшими практиками при разработке ПО и упросить переиспользование кода в своих программных проектах. Файл :code:`.wa` в формате YAML содержит команды и соответствующие им действия, а заготовки файлов с исходным кодом хранятся как шаблоны. :code:`.wa`-файл и шаблоны могут распространяться вместе исходным кодом вашего проекта.

.. contents:: Содержание
   :depth: 3

Установка
---------
С помощью pip

.. code-block:: bash
    
    pip install wa

или из исходного кода

.. code-block:: bash
    
    git clone https://github.com/char16t/wa.git
    cd wa
    make install

Быстрый старт
-------------
wa может быть вызван из консоли

.. code-block:: bash
    
    wa
    wa: workflow automation tool
    
wa принимает в качестве аргументов команды, которым сопоставлены действия. Описав однажды команду :code:`startproject` вы можете вызвать её следующим образом:

.. code-block:: bash
    
    wa startproject

Поддерживаются команды неограниченной вложенности. Вы можете описать также команды :code:`startproject python`, :code:`startproject cpp` или :code:`startproject cpplib`. Вызвать их можно так:

.. code-block:: bash
    
    wa startproject python
    wa startproject cpp
    
Команды описываются в файлах :code:`.wa` в формате YAML. Например, для примеров выше это может выглядеть так:

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

Файл :code:`.wa` может лежать в корне вашего проекта и в вашей домашней директории. wa сначала попробует выполнить поиск запрошенной команды в корне вашего проекта, а затем, если не найдёт её там обратится к файлу :code:`.wa` и выполнит поиск команды там. То есть, создав файл :code:`.wa` как в примере выше в домашней директории, вы сможете выполнить, например

.. code-block:: bash
    
    $ wa startproject python

Будет предложено ввести значение для переменной :code:`PROJECTNAME`
    
.. code-block:: bash
    
    $ wa startproject python
    $ PROJECTNAME=_

Пусть, это будет :code:`helloworld`:

.. code-block:: bash
    
    $ wa startproject python
    $ PROJECTNAME=helloworld

и развернуть секелет Python-проекта :code:`helloworld` в любой директории. Обратите внимание, что в текущей директории будет также создан пустой файл :code:`.wa`. Он будет сигналом для wa, что именно здесь находится корень проекта. Теперь, если вы уйдёте в поддиректорию текущей директории и попытаетесь выполнить произвольную команду, её поиск будет произведен сначала в том файле, что находится на уровень выше в дереве директорий.

Вообще говоря, wa именно так и работает: поиск файла выполняется сначала в текущей директории, затем в директории выше и так далее до корня файловой системы. Если файл :code:`.wa` не был найден, то поиск продолжится в домашней директории.

В файле :code:`.wa` лежащем в корне вашего проекта вы можете переопределить любые команды (например, :code:`startproject python` из листингов выше). То есть, вы можете распространять :code:`.wa`-файл вместе с кодом вашего проекта и помочь другим разработчикам, например, быстро создать скелет класса, оформленный по стандартам проекта.

wa позволяет также работать с файлами и каталогами относительно корня вашего проекта. Для этого нужно указать вертикальную черту перед путём к файлу или каталогу

.. code-block:: yaml
    
    newclass:
        - input CLASSNAME
        - cp |.code_templates/class.cpp |src/${CLASSNAME}.cpp
        - cp |.code_templates/header.cpp |include/${CLASSNAME}.hpp
        
При исполнении примера выше будет произведено копирование файлов :code:`.code_templates/class.cpp` и :code:`.code_templates/header.hpp` с заданным именем в директории :code:`src` и :code:`include` соответственно. Здесь главное, что вы можете находиться в любой директории вашего проекта, но копирование будет произведено относительно корня проекта, т.к. это явно указано вертикальной чертой :code:`|`.

В примере ниже вертикальной черты в начале вторых аргументов нет

.. code-block:: yaml
    
    newclass:
        - input CLASSNAME
        - cp |.code_templates/class.cpp ${CLASSNAME}.cpp
        - cp |.code_templates/header.cpp ${CLASSNAME}.hpp

При исполнении этого примера будут скопированы файлы с заданными именами в текущую директорию. Например, если вы находитесь в директории :code:`my_great_cpp_app/legacy`, то файлы будут скопированы в неё, а если находитесь в :code:`my_great_cpp_app/legacy/tests`, то в неё.

Вертикальную черту в начале путей до файлов и папок можно использовать в любых командах.

Доступные команды (API)
-----------------------
Вы можете использовать описанные ниже команды. Для каждой команды примеден пример использования.

set
~~~
:code:`set <переменная> <значение>` устанавливает значение для переменной. После в любых командах можно использовать переменную как :code:`${переменная}`. Имена переменных задаются с учётом регистра.

.. code-block:: yaml
    
    create_file_and_directory:
        - set PREFIX mysuperpupuer
        - touch ${PREFIX}_file.txt
        - mkdir ${PREFIX}_dir

input
~~~~~
:code:`input <имя переменной>` Запрашивает ввод у пользователя переменной

.. code-block:: yaml
    
    startproject:
        - input PROJECTNAME
        - mkdir ${PROJECTNAME}
        - touch ${PROJECTNAME}/README.txt

cd
~~
:code:`cd <путь>` переходит по заданному пути.

.. code-block:: yaml
    
    startproject:
        - input PROJECTNAME
        - mkdir ${PROJECTNAME}
        - cd ${PROJECTNAME}
        - touch README.txt

mkdir
~~~~~
:code:`mkdir <имя папки> [<имя папки> [<имя папки>]]` создаёт папки с заданными именами.

.. code-block:: yaml
    
    mkdirs:
        - mkdir one two three/four

touch
~~~~~
:code:`touch <имя файла> [<имя файла> [<имя файла>]]` создаёт файлы с заданными именами.

.. code-block:: yaml
    
    touchs:
        - touch one two three/four

rm
~~
:code:`rm <имя файла или папки> [<имя файла или папки> [<имя файла или папки>]]` удаляет файлы и папки с заданными именами.

.. code-block:: yaml
    
    clean:
        - rm build
        - rm dist

cp
~~
:code:`cp <источник> <цель>` копирует из источника в цель.

.. code-block:: yaml
    
    license:
        - input LICENSE_NAME
        - cp /home/user/templates/${LICENSE_NAME}.template |LICENSE

cptpl
~~~~~
:code:`cptpl <источник> <цель>` копирует из источника в цель с заменой :code:`[[переменная]]` на значение переменной в именах файлов и папок и :code:`<<<переменная>>>` на значение переменной в содержимом файлов.

.. code-block:: yaml
    
    license:
        - input PROJECT_NAME PROJECT_DESCRIPTION PROJECT_LICENSE
        - cptpl /home/user/templates/cpp_lib |.

Первым аргументом указывается папка, содержащая шаблон, а вторым аргументом путь, куда этот шаблон будет скопирован. Например, для Python-проектов шаблон может выглядеть так: создадим каталог :code:`/home/user/templates/python` со следующим содержимым

.. code-block:: code
    
    [[PROJECT_NAME]]
        __init__.py
        [[PRPJECT_NAME]].py
    tests
        __init__.py

А в содержимое файла :code:`[[PRPJECT_NAME]].py` исправим на 

.. code-block:: code
    
    # This file is a part of <<<PROJECT_NAME>>>
    # Licensed under MIT. See LICENSE file for details
    # (c) 2015 <<<AUTHOR_NAME>>> <<<<AUTHOR_EMAIL>>>>
    
    def main():
        pass
        
    if __name__ == "__main__":
        main()

Теперь при вызове wa будет предложено ввести значения переменных, а затем шаблон будет скопирован. Так выглядит :code:`.wa`-файл

.. code-block:: yaml
    
    pyscaffold:
        - cptpl /home/user/templates/python |.

Обратите внимание, что в примере выше не требуется просить пользователя ввести нужные переменные. Запрос на ввод будет происходить автоматически, как только будет встречена незнакомая переменная.

wa сохраняет введенные значения переменных в рамках каждого вашего проекта. Если вы ввели ранее значение, например, для :code:`PROJECT_NAME` то больше запрос на ввод происходить не будет. Если нужно принудительно обновить значение переменной, запрашивайте у пользователя значение заново, с помощью команды :code:`input`

Теперь нужно выполнить в консоли

.. code-block:: bash

    $ wa pyscaffold
    $ PROJECT_NAME=helloworld
    $ PROJECT_AUTHOR=Foo Bar
    $ AUTHOR_EMAIL=foo@bar.com

В результате, будет создана следующа структура директорий

.. code-block:: code
    
    helloworld
        __init__.py
        helloworld.py
    tests
        __init__.py

А файл :code:`helloworld/helloworld.py` будет иметь следующее содержимое

.. code-block:: code
    
    # This file is a part of helloworld
    # Licensed under MIT. See LICENSE file for details
    # (c) 2015 Foo Bar <foo@bar.com>
    
    def main():
        pass
        
    if __name__ == "__main__":
        main()

cptpljinja2
~~~~~~~~~~~
:code:`cptpljinja2 <источник> <цель>` копирует из источника в цель с заменой :code:`[[переменная]]` на значение переменной в именах файлов и папок, а содержимое компилирует из шаблонов Jinja2, которые лежат в файлах источника.

.. code-block:: yaml
    
    license:
        - input PROJECT_NAME PROJECT_DESCRIPTION PROJECT_LICENSE
        - cptpljinja2 /home/user/templates/cpp_lib |.

mv
~~
:code:`mv <источник> <цель>` перемещает файлы и папки из источника в цель.

.. code-block:: yaml
    
    to_legacy:
        - input CLASS
        - mv |src/${CLASS}.cpp |legacy/src/${CLASS}.cpp
        - mv |include/${CLASS}.hpp |legacy/include/${CLASS}.hpp

echo
~~~~
:code:`echo <соощение>` выводит сообщение на экран.

.. code-block:: yaml
    
    copy_large_file:
        - cp /home/12Gb.raw |.
        - echo Ok, copied

exec
~~~~
:code:`exec <команда>` выполняет команду в командной строке операционной системы.

.. code-block:: yaml
    
    test:
        - cd |.
        - exec make test

py
~~
:code:`py <имя файла> <функция>` функцию из файла в интерпретаторе Python.

.. code-block:: yaml
    
    test:
        - cd |.
        - py runtests.py main


Ошибки и проблемы
-----------------
О любых ошибках, по любым вопросам и с любыми предложениями вы можете написать на почту v.manenkov (at) gmail.com или создать задачу в Github Issues https://github.com/char16t/wa/issues

Лицензия
--------
Исходный код распространяется под лицензией MIT. Текст лицензии находится в файле LICENSE. 
