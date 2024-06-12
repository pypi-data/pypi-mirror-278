|release| |pypi|

========
posmatch
========

Positional sub-pattern matching for custom classes.

Requirements
============

Python 3.10 or higher.

Installation
============

.. code::

    pip install posmatch

Usage
=====

The ``pos_match`` decorator
---------------------------

.. code-block:: python

    from posmatch import pos_match


    @pos_match
    class Color:
        def __init__(self, red, green, blue):
            self.red = red
            self.green = green
            self.blue = blue


    color = Color(0, 0, 128)

    match color:
        case Color(r, g, b) if r == g == b:
            print('Shade of grey')
        case Color(0, 0):
            print('Shade of blue')

Output:

.. code::

    Shade of blue

The ``PosMatchMeta`` metaclass
------------------------------

.. code-block:: python

    from posmatch import PosMatchMeta


    class Date(metaclass=PosMatchMeta):
        def __init__(self, year, month, day):
            self.year = year
            self.month = month
            self.day = day


    date = Date(2121, 1, 1)

    match date:
        case Date(_, m, d) if m == 5 and d == 1:
            print('May Day')
        case Date(y) if y > 2100:
            print('Distant future')

Output:

.. code::

    Distant future

The ``PosMatchMixin`` mix-in class
----------------------------------

.. code-block:: python

    from posmatch import PosMatchMixin


    class Rectangle(PosMatchMixin):
        def __init__(self, width, height):
            self.width = width
            self.height = height


    shape = Rectangle(16, 16)

    match shape:
        case Rectangle(w, h) if w == h:
            print('Square')
        case Rectangle(x, y) if x > y:
            print('Landscape')

Output:

.. code::

    Square


.. |release| image:: https://img.shields.io/github/v/release/mportesdev/posmatch
    :target: https://github.com/mportesdev/posmatch/releases/latest
.. |pypi| image:: https://img.shields.io/pypi/v/posmatch
    :target: https://pypi.org/project/posmatch
