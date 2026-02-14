.. _misc-faq:

Frequently Asked Questions (FAQ)
================================

.. _@codejedi365: https://github.com/codejedi365
.. _cj365-flatdict: https://pypi.org/project/cj365-flatdict
.. _flatdict: https://pypi.org/project/flatdict/
.. _flatdict2: https://pypi.org/project/flatdict2/
.. _PEP 517: https://www.python.org/dev/peps/pep-0517/

#.  What is the difference between `flatdict`_, `flatdict2`_, and `cj365-flatdict`_ packages?

    `flatdict`_ is the original package written for Python 2.7 by Gavin M. Roy in 2012,
    which provides the basic functionality for flattening nested dictionaries and lists.
    Improvements and maintenance of this package stopped in 2020 at v4.0.1, until the
    v4.1.0 was released in 2026, which resolved the problem with installation by pip
    ``>=25.3`` with the latest build standard `PEP 517`_.

    `flatdict2`_ is a fork created by Dennis Henry in 2020 of the original `flatdict`_
    package to publish a wheel on PyPI instead of just a source distribution but it did
    not modernize the codebase. The source dist is not installable by pip 25.3 due to the
    old build standard but the wheel is installable by pip 25.3 and provides the same
    functionality as `flatdict`_.

    `cj365-flatdict`_ is a complete rewrite of the original `flatdict`_ package by
    `@codejedi365`_ in 2026, which modernized the ``v4.0.4`` codebase to Python3
    expectations, enhanced the flexibility of updating nested values, and modernized
    the build infrastructure to support the latest build standards and tools. Performance
    optimizations and testing rigor were also added to ensure the package is robust,
    performant, and memory efficient. The default delimiter was also changed from a
    colon (``:``) to a period (``.``) to align with common conventions for representing
    nested keys in Python and other programming languages.


#.  Why does FlatterDict exist when FlatDict already exists?

    :py:class:`~cj365.flatdict.flat_dict.FlatDict` is designed to enable updating of
    nested dictionaries only while :py:class:`~cj365.flatdict.flatter_dict.FlatterDict`
    is designed to enable updating of nested dictionaries and sequences (lists and
    tuples). If you only desire to extract or update lists, tuples, or sets wholesale
    as values, then :py:class:`~cj365.flatdict.flat_dict.FlatDict` will be sufficient
    for your needs. However, if you need to extract or update individual items within
    lists, tuples, or sets, then :py:class:`~cj365.flatdict.flatter_dict.FlatterDict`
    would be the appropriate choice.

    Integers, floats, strings, booleans, None, and other non-dict and non-sequence
    types are treated as simple values in both classes and cannot be updated with
    delimited keys.


#.  How does FlatterDict differ from FlatDict?

    :py:class:`~cj365.flatdict.flatter_dict.FlatterDict` is able to take a delimited
    key that includes an offset integer for a list, tuple, or set and update the
    value at that offset within the sequence. For example, if you have a list
    ``my_list = [1, 2, 3]`` and you want to update the value at index 1 to be 42, you
    could use :py:class:`~cj365.flatdict.flatter_dict.FlatterDict` to do this with a
    delimited key like ``my_list.1``. This would update the list to be
    ``my_list = [1, 42, 3]``.

    In contrast, :py:class:`~cj365.flatdict.flat_dict.FlatDict` would treat ``my_list.1``
    as an invalid key since it does not support updating of individual items within
    sequences. Instead, you would need to update the entire list at once with a key
    like ``my_list`` and provide the new list value.


#.  Why can't I use customized classes as values in FlatDict or FlatterDict?

    :py:class:`~cj365.flatdict.flat_dict.FlatDict` will be able to handle customized
    classes as values unless they specifically extend the built-in ``dict`` class.
    These classes will be treated as simple values and cannot be updated with delimited
    keys. However, if a customized class extends the built-in ``dict`` class, the
    behavior of :py:class:`~cj365.flatdict.flat_dict.FlatDict` can be unpredictable
    since it is designed to work with standard Python data types and may not be
    compatible with the internal structure and behavior of customized classes that
    extend ``dict``.

    :py:class:`~cj365.flatdict.flatter_dict.FlatterDict` will not be able to handle
    customized sequence classes because under the hood we convert sequences to
    index-keyed dictionaries to provide the delimited key updating functionality. In
    the :py:meth:`~cj365.flatdict.flatter_dict.FlatterDict.inflate()` method, we
    attempt to convert these index-keyed dictionaries back to their original sequence
    types but if the original sequence type is a customized class, we will not be able
    to convert it back and it will be inflated as a memory-efficient tuple instead.
