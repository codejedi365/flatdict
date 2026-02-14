.. _examples-flatdict:

FlatDict Examples
--------------------

All of the following examples assume you have installed the ``cj365-flatdict`` package
and unless otherwise noted will start with the following data structure:

.. code-block:: python

    from cj365.flatdict import FlatDict

    data = {
        'foo': {
            'bar': 'baz',
            'qux': ["a", 'b']
        }
    }
    flat_dict = FlatDict(data, delimiter='.')

It is important to note that FlatDict implements the Mapping protocol, so it
supports all the standard dictionary methods and behaviors, such as iteration,
membership testing, and more. For example, you can check if a key exists in the
FlatDict:

..  code-block:: python

    print('foo.bar' in flat_dict)
    # Output: True

    print('foo.qux' in flat_dict)
    # Output: True

    print('nonexistent-key' in flat_dict)
    # Output: False

    # It will also support existence of the parent keys
    print('foo' in flat_dict)
    # Output: True

Dictionary methods like ``.keys()``, ``.values()``, and ``.items()`` will also work
as expected in Python 3, and will return View iterator objects that reflect the
current state of the FlatDict. For example:

..  code-block:: python

    print(flat_dict.keys())
    # Output: dict_keys(['foo.bar', 'foo.qux'])

    print(flat_dict.values())
    # Output: dict_values(['baz', ['a', 'b']])

    print(flat_dict.items())
    # Output: dict_items([
    #     ('foo.bar', 'baz'), ('foo.qux', ['a', 'b']),
    # ])

Dictionary methods like ``.pop()`` and ``.update()`` will also work as expected, and
will maintain the integrity of the nested structure. For example, the ``.pop()`` method
will remove the specified key and return its value, while also ensuring that the
integrity of the nested structure is maintained. For example:

..  code-block:: python

    popped_value = flat_dict.pop('foo.bar')
    print(popped_value)
    # Output: baz

    print(flat_dict)
    # Output: {'foo.qux': ['a', 'b']}

    flat_dict.update({'foo.bar': 'new_value'})
    print(flat_dict)
    # Output: {'foo.qux': ['a', 'b'], 'foo.bar': 'new_value'}

The ``.update()`` method will also work with nested dictionaries, allowing you to update
multiple keys at once while maintaining the nested structure. For example:

..  code-block:: python

    flat_dict.update({
        'foo.bar': 'new_value',
        'foo.new_key': 'new_value2'
    })
    print(flat_dict)
    # Output: {'foo.qux': ['a', 'b'], 'foo.bar': 'new_value', 'foo.new_key': 'new_value2'}

FlatDict also supports the equality operator (``==``) for comparing two FlatDict
instances, as well as comparing a FlatDict instance to a regular dictionary. When
comparing two FlatDict instances, they are considered equal if they have the same
keys and corresponding values, regardless of the order of the keys. When comparing
a FlatDict instance to a regular dictionary, they are considered equal if the
FlatDict can be inflated to a nested dictionary that is equal to the regular dictionary
when using the standard equality operator (``==``). For example:

..  code-block:: python

    flat_dict2 = FlatDict({'foo.qux': ['a', 'b'], 'foo.bar': 'baz'})
    regular_dict = {'foo': {'bar': 'baz', 'qux': ['a', 'b']}}

    print(flat_dict == flat_dict2)
    # Output: True

    print(flat_dict == regular_dict)
    # Output: True

To see the full API reference, see the :py:class:`~cj365.flatdict.flat_dict.FlatDict`
documentation.
