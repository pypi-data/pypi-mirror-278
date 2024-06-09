######
Scuff
######

*A slick config file format for humans.*


Introduction
=============

**Scuff** is a language suite with a slick, efficient, flexible syntax, unique
features and useful tools.

Its purpose is to represent structured data effectively.
**Scuff's** greatest strengths are its syntactic simplicity and reliable
flexibility. It comes with a Python API and a simple command line tool for
moving data between JSON syntax, Python's and its own.

One excellent use for **Scuff** is to encode and parse configuration files.

**Scuff** implements its own custom lexer, recursive-descent parser and
transpiler to read and process data. Though written in Python, the parser
is immune from Python's recursion limit.


Installation
=============

To install **Scuff** and its tools for Python from the Python Package Index,
run the following in the command line:

.. code:: bash

    $ python -m pip install scuff


Grammar
========

Assigning Variables
--------------------

Variables are assigned with a *key* and a *value*.
Key names must be valid identifiers, meaning they must contain no spaces or
symbols except underscore (``_``).
Values can be assigned to variables with or without an equals sign (``=``):

.. code:: py

    my_favorite_number = 42
    my_favorite_color "Magenta"
    is_but_a_flesh_wound yes

When left without a value, variables will evaluate to ``null`` or ``None``:

.. code:: py

    set_to_null =
    also_null
    but_this_has_a_value 15


Data Types
-----------

- Numbers
    Numbers can be integers or floats::

        1 1.2 -1_000 0.123 .123_4

- Booleans
    The boolean values ``True`` and ``False`` are given using these variants::

        True true yes
        False false no

    They are case-insensitive, so ``yes`` and ``yES`` both evaluate to ``True``.

- Strings
    Single-line strings can be enclosed by single quotes (``'``), double
    quotes (``"``) or backticks (`````), and multiline strings are enclosed by
    three of any one:

    .. code:: py

        foo "abc"
        bar 'def'
        baz '''Hi,
                did you know
                    you're cute?
                        '''


..
    Strings placed right next to each other are concatenated:

    .. code:: py
        
        first = "ABC"
        second = "DEF"
        first_plus_second = "ABC"  "DEF"
        concatenated = "ABCDEF"
                    
- Lists
    Lists are enclosed by square brackets (``[]``).
    Elements inside lists are separated by spaces, commas or line breaks:

    .. code:: py

        groceries [
            "bread",
            "milk" "eggs"
            "spam"
        ]

- Mappings
    Mappings are groups of key-value pairs enclosed by curly braces (``{}``).
    Values may be any expression, even other mappings:

    .. code:: py

        me {
            name "Samantha"
            age 24
            job "Developer"
            favorite_things {
                editor "Vim"
                languages ["Python", "Rust"]
            }
        }

    Mappings may also take the form of dotted attribute lookups:

    .. code:: py

        outer.middle.inner yes

    evauates in Python to

    .. code:: py

        {'outer': {'middle': {'inner': True}}}


- Comments
    Single-line comments are made using the ``#`` symbol:

    .. code:: py

        option = "The parser reads this."
        # But this is a comment.
            #And so is this.
        option2 = "# But not this; It's inside a string."
        # The parser ignores everything between ``#`` and the end of the line.
         #   ignore = "Comment out any lines of code you want to skip."


Python Usage
============
Once you install **Scuff**, you can then import ``scuff`` as a Python module
and use its tools:

.. code:: py

    >>> import scuff
    >>> scuff.to_json('menu {border.color "#aa22bb", font.color "#cdcdcd"}')
    '{"menu": {"border": {"color": "#aa22bb"}, "font": {"color": "#cdcdcd"}}}'

    >>> type(scuff.to_py('Documents/file.conf'))
    <class 'dict'>

    >>> scuff.to_py('a.b ["c", "d"]')
    {'a': {'b': ['c', 'd']}}

    >>> scuff.parse('hovercraft ["eel" "eel" "eel" "eel"]')
    <ast.Module object at 0x74b59c109710>
    >>> print(scuff.dump(_))
    Module(
      body=[
        Assign(
          targets=[
            Name(id='hovercraft')],
          value=List(
            elts=[
              Constant(value='eel'),
              Constant(value='eel'),
              Constant(value='eel'),
              Constant(value='eel')]))])


Command Line Usage
==================
**Scuff** also comes with a command line tool for converting between formats:

.. code:: none

    usage: scuff [-h] [-j] [-p] [-a] [--debug] [-v] source [source ...]

    positional arguments:
      source           The file path(s) or literal Scuff to process.

    options:
      -h, --help       show this help message and exit
      -j, --to-json    Convert `source` to JSON.
      -p, --to-python  Convert `source` to Python.
      -a, --show-ast   Parse `source` and show its equivalent AST.
      --debug          Use debug mode. (Not implemented)
      -v, --version    show program's version number and exit

Multiple files and strings may be converted in multiple ways at once:

.. code:: bash

    $ python -m scuff --to-json ~/.config/mybar/mybar.conf 'foo {a{b [1,{c 3}]}}'
    {"field_order": ["hostname", "uptime", "cpu_usage", "cpu_temp", "mem_usage", "disk_usage", "battery", "net_stats", "datetime"], "field_icons": {"uptime": ["Up ", "\uf2f2 "], "cpu_usage": ["CPU ", "\uf3fd "], "cpu_temp": ["", "\uf06d "], "mem_usage": ["MEM ", "\uf2db "], "disk_usage": ["/: ", "\uf233 "], "battery": ["BAT ", "\uf242 "], "net_stats": ["", "\uf1eb"]}}

    {"foo": {"a": {"b": [1, {"c": 3}]}}}




