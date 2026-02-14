Quick Reference
===============

This section provides a quick reference guide to the main features and usage of the FlatDict package.

FlatDict
--------

:py:class:`~cj365.flatdict.flat_dict.FlatDict` provides a dictionary-like interface
for working with nested dictionaries using delimited keys. It allows you to access,
update, and manipulate nested dictionaries as if they were flat dictionaries.

.. code-block:: python

    from cj365.flatdict import FlatDict

    data = {
        'foo': {
            'bar': 'baz',
            'qux': ["a", 'b']
        }
    }
    flat_dict = FlatDict(data, delimiter='.')

    # printing all keys
    print(flat_dict.keys())
    # Output: dict_keys(['foo.bar', 'foo.qux'])

    # Accessing values using delimited keys
    print(flat_dict['foo.bar'])
    # Output: baz

    print(flat_dict['foo.qux'])
    # Output: ['a', 'b']

    # Updating values using delimited keys
    flat_dict['foo.bar'] = 'new_value'
    print(flat_dict['foo.bar'])
    # Output: new_value

    # Converting back to nested dictionary
    nested_dict = flat_dict.inflate()
    print(nested_dict)
    # Output: {'foo': {'bar': 'new_value', 'qux': ['a', 'b']}}

To see more examples and use cases of :py:class:`~cj365.flatdict.flat_dict.FlatDict`,
check out the :ref:`Example Use <examples-flatdict>` section.

FlatterDict
-----------

:py:class:`~cj365.flatdict.flatter_dict.FlatterDict` provides a similar interface but
also handles sequences and sets as child-dict instances with the offset as the key. It
allows you to work with nested dictionaries that contain lists and sets as if they were
flat dictionaries.

.. code-block:: python

    from cj365.flatdict import FlatterDict

    data = {
        'list': ['a', 'b', 'c'],
        'set': {'x', 'y', 'z'}
    }
    flatter_dict = FlatterDict(data, delimiter='.')

    # printing all keys
    print(flatter_dict.keys())
    # Output: dict_keys(['list.0', 'list.1', 'list.2', 'set.0', 'set.1', 'set.2'])

    # Accessing values using delimited keys
    print(flatter_dict['list.0'])
    # Output: a

    print(flatter_dict['set.0'])
    # Output: x

    # Updating values using delimited keys
    flatter_dict['list.1'] = 'new_value'
    print(flatter_dict['list.1'])
    # Output: new_value

    # Converting back to nested dictionary
    nested_dict = flatter_dict.inflate()
    print(nested_dict)
    # Output: {'list': ['a', 'new_value', 'c'], 'set': {'x', 'y', 'z'}}

To see more examples and use cases of :py:class:`~cj365.flatdict.flatter_dict.FlatterDict`,
check out the :ref:`Example Use <examples-flatterdict>` section.
