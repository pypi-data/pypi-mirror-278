NAME

::

    OBJX - objects


SYNOPSIS

::

    >>> from objx import Object, dumps, loads
    >>> o = Object()
    >>> o.a = "b"
    >>> print(loads(dumps(o)))
    {'a': 'b'}


DESCRIPTION

::

    OBJX contains all the python3 code to program objects in a functional
    way. It provides a base Object class that has only dunder methods, all
    methods are factored out into functions with the objects as the first
    argument. I call it Object Programming (OP), OOP without the oriented.

    OBJX  allows for easy json save//load to/from disk of objects. It
    provides an "clean namespace" Object class that only has dunder
    methods, so the namespace is not cluttered with method names. This
    makes storing and reading to/from json possible.

    OBJX is Public Domain.


AUTHOR

::

    Bart Thate <bthate@dds.nl>


COPYRIGHT

::

    OBJX is Public Domain.
