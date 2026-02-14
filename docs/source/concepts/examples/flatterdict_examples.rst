.. _examples-flatterdict:

FlatterDict Examples
--------------------

All of the following examples assume you have installed the ``cj365-flatdict`` package
and unless otherwise noted will start with the following data structure:

.. code-block:: python

    from cj365.flatdict import FlatterDict

    data = {
        'list': ['a', 'b', 'c'],
        'set': {'x', 'y', 'z'}
    }
    flatter_dict = FlatterDict(data, delimiter='.')

It is important to note that FlatterDict implements the Mapping protocol, so it
supports all the standard dictionary methods and behaviors, such as iteration,
membership testing, and more. For example, you can check if a key exists in the
FlatterDict:

..  code-block:: python

    print('list.0' in flatter_dict)
    # Output: True

    print('set.1' in flatter_dict)
    # Output: True

    print('nonexistent-key' in flatter_dict)
    # Output: False

    # It will also support existence of the parent keys
    print('list' in flatter_dict)
    # Output: True

Dictionary methods like ``.keys()``, ``.values()``, and ``.items()`` will also work
as expected in Python 3, and will return View iterator objects that reflect the
current state of the FlatterDict. For example:

..  code-block:: python

    print(flatter_dict.keys())
    # Output: dict_keys(['list.0', 'list.1', 'list.2', 'set.0', 'set.1', 'set.2'])

    print(flatter_dict.values())
    # Output: dict_values(['a', 'b', 'c', 'x', 'y', 'z'])

    print(flatter_dict.items())
    # Output: dict_items([
    #     ('list.0', 'a'), ('list.1', 'b'), ('list.2', 'c'),
    #     ('set.0', 'x'), ('set.1', 'y'), ('set.2', 'z'),
    # ])

Dictionary methods like ``.pop()`` and ``.update()`` are a bit more complex due to the
nested structure and the handling of sequences. The ``.pop()`` method will remove the
specified key and return its value, while also ensuring that the integrity of the nested
structure is maintained. If the popped key is part of a sequence, the method will also
update the keys of the remaining items in the sequence to reflect their new positions. If
the popped key is a parent key, it will remove all child keys as well. When the popped key
is not found, it will return None or a specified default value. If the popped key is a
regular key, it will simply remove that key and return its value. All of scenarios described
above are demonstrated in the following example:

..  code-block:: python

    # Popping a regular key
    print(flatter_dict.pop('list.1'))
    # Output: b
    # New state of flatter_dict: {'list': ['a', 'c'], 'set': {'x', 'y', 'z'}}

    # Popping a parent key (will return an ordered tuple of the child values)
    print(flatter_dict.pop('set'))
    # Output: ('x', 'y', 'z')
    # New state of flatter_dict: {'list': ['a', 'c']}

    # Popping a non-existent key with default value
    print(flatter_dict.pop('nonexistent-key', 'default-value'))
    # Output: default-value

    # Popping a non-existent key without default value
    print(flatter_dict.pop('another-nonexistent-key'))
    # Output: None

The ``.update()`` method allows you to update the FlatterDict with another dictionary or an
iterable of key-value pairs. When updating with a dictionary, it will handle nested structures
and sequences appropriately, ensuring that the keys are updated to reflect their new positions
if necessary. When updating with an iterable of key-value pairs, it will simply add or update
the specified keys and values without any special handling. The following example demonstrates
both scenarios:

..  code-block:: python

    # Updating with a dictionary (will handle nested structures and sequences)
    flatter_dict.update({
        'list': ['a', 'new_value', 'c'],
        'set': {'r', 's', 't'},
    })
    # New state of flatter_dict: {'list': ['a', 'new_value', 'c'], 'set': {'r', 's', 't'}}

    # Updating with an iterable of key-value pairs (no special handling)
    flatter_dict.update([
        ('list.1', 'another_new_value'),
        ('set.1', 'another_new_value'),
    ])
    # New state of flatter_dict: {
    #     'list': ['a', 'another_new_value', 'c'],
    #     'set': {'r', 'another_new_value', 't'}
    # }

FlatterDict also supports the equality operator (``==``) with other FlatterDict instances,
as well as comparisons with the same type of initial data structure (nested dictionaries,
lists, tuples, and sets). When comparing with another FlatterDict instance, it will check if
the keys and values are the same, and check the delimiter as well. When comparing with
the same type of initial data structure, it will inflate itself and compare the resulting
nested structure with the other object. The following example demonstrates these comparisons:

..  code-block:: python

    flatter_dict2 = FlatterDict(data, delimiter='.')

    # Comparing two FlatterDict instances
    print(flatter_dict == flatter_dict2)
    # Output: True

    # Comparing with the same type of initial data structure
    print(flatter_dict == data)
    # Output: True

To see the full API reference, see the :py:class:`~cj365.flatdict.flatter_dict.FlatterDict`
documentation.
