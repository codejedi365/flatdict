from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

import pytest
from pytest_dependency import depends

from cj365.flatdict import FlatDict

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any


class Point(NamedTuple):
    x: int
    y: int


def test_flatdict_init_from_NamedTuple(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(request, [test_flatdict_dunder_getitem.__name__], scope="module")

    point = Point(x=1, y=2)

    # Test that initializing a FlatDict from a NamedTuple correctly
    # converts it to a dictionary
    flat_dict = FlatDict(point, delimiter=".")
    assert point.x == flat_dict["x"]
    assert point.y == flat_dict["y"]


def test_flatdict_init_from_flatdict(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(request, [test_flatdict_dunder_getitem.__name__], scope="module")

    data = {"a": 1, "b": 2}
    flat_dict = FlatDict(data)
    new_flat_dict = FlatDict(flat_dict)
    assert data["a"] == new_flat_dict["a"]
    assert data["b"] == new_flat_dict["b"]


def test_flatdict_init_from_flattened_dict():
    assert FlatDict({"a": 1, "b.c": 2}, delimiter=".")


def test_flatdict_init_fails_w_empty_delimiter():
    with pytest.raises(ValueError, match="Delimiter cannot be an empty string"):
        assert FlatDict({"a": 1, "b": {"c": 2}}, delimiter="")


def test_flatdict_flatten_delimiter_collision():
    with pytest.raises(ValueError, match="Key 'b.c' collides with the delimiter '.'"):
        assert FlatDict.flatten({"a": 1, "b.c": 2}, delimiter=".")


def test_flatdict_unflatten_fails_w_empty_delimiter():
    with pytest.raises(ValueError, match="Delimiter cannot be an empty string"):
        assert FlatDict.unflatten({"a": 1, "b.c": 2}, delimiter="")


def test_flatdict_clear(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(
            request,
            [test_flatdict_dunder_equality.__name__, test_flatdict_dunder_len.__name__],
            scope="module",
        )

    flat_dict = FlatDict({"a": 1, "b": 2})

    # Test that clearing a FlatDict removes all items
    # and results in an empty FlatDict
    flat_dict.clear()
    assert len(flat_dict) == 0
    assert flat_dict == {}


def test_flatdict_clear_nested(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(
            request,
            [test_flatdict_dunder_equality.__name__, test_flatdict_dunder_len.__name__],
            scope="module",
        )

    flat_dict = FlatDict({"a": {"b": 1}, "c": 2})

    # Test that clearing a FlatDict with nested dictionaries
    # removes all items and results in an empty FlatDict
    flat_dict.clear()
    assert len(flat_dict) == 0
    assert flat_dict == {}


def test_flatdict_copy(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(request, [test_flatdict_dunder_equality.__name__], scope="module")

    flat_dict = FlatDict({"a": 1, "b": {"c": 2}})

    # Test that copying a FlatDict creates a new FlatDict
    # with the same content but different instance (ie. a deep copy)
    flat_dict_copy = flat_dict.copy()

    # Evaluate (Expected -> Actual)
    assert flat_dict_copy == flat_dict
    assert flat_dict_copy is not flat_dict


def test_flatdict_copy_nested(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(
            request,
            [
                test_flatdict_dunder_equality.__name__,
                test_flatdict_dunder_getitem.__name__,
            ],
            scope="module",
        )

    flat_dict = FlatDict({"a": {"b": {"c": [2]}}})

    # Test that copying a FlatDict with nested dictionaries
    # creates a new FlatDict with the same content but different
    # nested dictionary instances (ie. a deep copy)
    flat_dict_copy = flat_dict.copy()

    # Evaluate (Expected -> Actual)
    assert flat_dict == flat_dict_copy
    assert flat_dict is not flat_dict_copy
    assert flat_dict["a"] == flat_dict_copy["a"]
    assert flat_dict["a"] is not flat_dict_copy["a"]
    assert flat_dict["a"]["b"] == flat_dict_copy["a"]["b"]
    assert flat_dict["a"]["b"] is not flat_dict_copy["a"]["b"]
    assert flat_dict["a"]["b"]["c"] == flat_dict_copy["a"]["b"]["c"]
    assert flat_dict["a"]["b"]["c"] is not flat_dict_copy["a"]["b"]["c"]


def test_flatdict_copy_empty(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(
            request,
            [test_flatdict_dunder_equality.__name__, test_flatdict_dunder_len.__name__],
            scope="module",
        )

    flat_dict = FlatDict()

    # Test that copying an empty FlatDict returns an empty FlatDict
    flat_dict_copy = flat_dict.copy()
    assert flat_dict == flat_dict_copy
    assert flat_dict is not flat_dict_copy
    assert 0 == len(flat_dict_copy)


def test_flatdict_get():
    flat_dict = FlatDict({"a": 1, "b": {"c": 2}}, delimiter=".")

    # Test that get returns the correct values for existing keys
    assert flat_dict.get("a") == 1
    assert flat_dict.get("b") == {"c": 2}
    assert flat_dict.get("b.c") == 2

    # Test that get returns None for non-existent keys
    assert flat_dict.get("d") is None
    assert flat_dict.get("d", "default") == "default"


def test_flatdict_inflate():
    expected = {"a": 1, "b": {"c": [2, 3]}}
    flat_dict = FlatDict(expected, delimiter=".")

    # Test that inflating the FlatDict returns a dictionary equal to the original nested structure
    inflated = flat_dict.inflate()

    # Evaluate (Expected -> Actual)
    assert expected == inflated
    assert expected is not inflated
    assert expected["b"] == inflated["b"]
    assert expected["b"] is not inflated["b"]
    assert expected["b"]["c"] == inflated["b"]["c"]
    assert expected["b"]["c"] is inflated["b"]["c"]


def test_flatdict_inflate_empty():
    expected = {}
    flat_dict = FlatDict()

    # Test that inflating an empty FlatDict returns an empty dictionary
    inflated = flat_dict.inflate()
    assert expected == inflated
    assert inflated is not expected


def test_flatdict_items():
    flat_dict = FlatDict({"a": 1, "b": {"c": 2}}, delimiter=".")

    # Test that the items method returns the correct set of key-value pairs
    items = flat_dict.items()
    assert set(items) == {("a", 1), ("b.c", 2)}


def test_flatdict_keys():
    flat_dict = FlatDict({"a": 1, "b": {"c": 2}}, delimiter=".")

    # Test that the keys method returns the correct set of keys
    keys = flat_dict.keys()
    assert set(keys) == {"a", "b.c"}


def test_flatdict_pop(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(
            request,
            [
                test_flatdict_dunder_equality.__name__,
                test_flatdict_dunder_contains.__name__,
            ],
            scope="module",
        )

    flat_dict = FlatDict({"a": 1, "b": {"c": 2, "d": 3}}, delimiter=".")

    # Test popping a nested key
    value = flat_dict.pop("b.d")
    assert value == 3
    assert "b.d" not in flat_dict

    # Test popping a top-level key of a nested dictionary removing
    # the entire dictionary
    value = flat_dict.pop("b")
    assert value == {"c": 2}
    assert "b.c" not in flat_dict

    # Test popping a non-existent key without a default value
    value = flat_dict.pop("b")
    assert value is None

    # Test popping a non-existent key with a default value
    value = flat_dict.pop("b", "default")
    assert value == "default"
    assert "b" not in flat_dict

    # Test popping a top-level key
    value = flat_dict.pop("a")
    assert value == 1
    assert "a" not in flat_dict

    # Test that popping the last key results in an empty FlatDict
    assert flat_dict == {}


def test_flatdict_setdefault(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(request, [test_flatdict_dunder_getitem.__name__], scope="module")

    values = [1, 2]
    flat_dict = FlatDict({"a": values[0], "b": {"c": values[1]}}, delimiter=".")

    # Test that setdefault returns the existing value for an existing key
    value = flat_dict.setdefault("a", "default")
    assert value == values[0]
    assert flat_dict["a"] == values[0]

    # Test that setdefault returns the default value for a non-existent key and sets it
    value = flat_dict.setdefault("d", "default")
    assert value == "default"
    assert flat_dict["d"] == "default"

    # Test that setdefault does not overwrite an existing nested key
    value = flat_dict.setdefault("b.c", "default")
    assert value == values[1]
    assert flat_dict["b.c"] == values[1]


def test_flatdict_set_delimiter(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(request, [test_flatdict_dunder_getitem.__name__], scope="module")

    data: dict[str, Any] = {"a": 1, "b": {"c": 2}}
    flat_dict = FlatDict(data, delimiter=".")

    # Test that changing the delimiter updates the internal structure
    # and allows access with the new delimiter
    flat_dict.delimiter = "/"
    assert flat_dict["a"] == data["a"]
    assert flat_dict["b"] == data["b"]
    assert flat_dict["b/c"] == data["b"]["c"]

    with pytest.raises(KeyError, match="Key 'b.c' not found in FlatDict"):
        assert flat_dict["b.c"]

    with pytest.raises(ValueError, match="Delimiter cannot be an empty string"):
        flat_dict.set_delimiter("")


def test_flatdict_update_merge(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(request, [test_flatdict_dunder_getitem.__name__], scope="module")

    data = {"a": 1, "b": {"c": [2]}}
    flat_dict = FlatDict(data, delimiter=".")

    # Test that updating the FlatDict with a new dictionary correctly updates the content
    flat_dict.update({"b": {"d": 3}, "e": 4})
    assert flat_dict["a"] == 1
    assert flat_dict["b"] == {"c": [2], "d": 3}
    assert flat_dict["b.c"] == [2]
    assert flat_dict["b.d"] == 3
    assert flat_dict["e"] == 4

    # Test updating the FlatDict with kwargs
    flat_dict.update(f=5, g={"h": 6})
    assert flat_dict["f"] == 5
    assert flat_dict["g"] == {"h": 6}
    assert flat_dict["g.h"] == 6

    # Test updating the FlatDict with iterable of key-value pairs
    flat_dict.update([("i", 7), ("j", {"k": 8})])
    assert flat_dict["i"] == 7
    assert flat_dict["j.k"] == 8


def test_flatdict_update_overwrite(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(request, [test_flatdict_dunder_getitem.__name__], scope="module")

    data = {"a": 1, "b": {"c": [2]}}
    flat_dict = FlatDict(data, delimiter=".")

    # Test that updating the FlatDict with a new dictionary correctly overwrites existing keys
    flat_dict.update({"a": 3, "b": {"c": [4]}})
    assert flat_dict["a"] == 3
    assert flat_dict["b"] == {"c": [4]}
    assert flat_dict["b.c"] == [4]


def test_flatdict_update_restructure(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(request, [test_flatdict_dunder_getitem.__name__], scope="module")

    data = {"a": 1, "b": {"c": [2]}}
    flat_dict = FlatDict(data, delimiter=".")

    # Test that updating the FlatDict with a new dictionary correctly restructures the content
    flat_dict.update({"b": 3})
    assert flat_dict["a"] == 1
    assert flat_dict["b"] == 3
    with pytest.raises(KeyError):
        assert flat_dict["b.c"]

    # Test that updating the FlatDict with a new dictionary correctly restructures the content again
    flat_dict.update({"b": {"d": 4}})
    assert flat_dict["a"] == 1
    assert flat_dict["b"] == {"d": 4}
    assert flat_dict["b.d"] == 4


def test_flatdict_update_empty(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(request, [test_flatdict_dunder_getitem.__name__], scope="module")

    data = {"a": 1, "b": {"c": [2]}}
    flat_dict = FlatDict(data, delimiter=".")

    # Test that updating the FlatDict with an empty dictionary does not change the content
    flat_dict.update({})
    assert flat_dict["a"] == 1
    assert flat_dict["b"] == {"c": [2]}
    assert flat_dict["b.c"] == [2]


@pytest.mark.order("third")
@pytest.mark.dependency
def test_flatdict_values(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(request, [test_flatdict_dunder_setitem.__name__], scope="module")

    initial_values = [1, 2]
    data = {"a": initial_values[0], "b": {"c": initial_values[1]}}
    flat_dict = FlatDict(data, delimiter=".")

    # Test that the values method returns the correct set of values
    # corresponding to the flattened keys
    values = flat_dict.values()
    actual_values = list(values)
    assert initial_values == actual_values

    # Test use of ValuesViewer when the FlatDict is modified
    # after calling values()
    flat_dict["d"] = 3  # requires __setitem__
    actual_values = list(values)
    expected = [*initial_values, 3]
    assert expected == actual_values


@pytest.mark.order("first")
@pytest.mark.dependency
def test_flatdict_dunder_contains():
    data = {"a": 1, "b": {"c": 2}}
    flat_dict = FlatDict(data, delimiter=".")

    # Test that the __contains__ method correctly identifies existing keys
    assert "a" in flat_dict
    assert "b.c" in flat_dict

    # Test that the __contains__ method correctly identifies non-existent keys
    assert "d" not in flat_dict
    assert "b.d" not in flat_dict
    assert "a.c" not in flat_dict

    # Test that the __contains__ method correctly identifies meta keys
    # substrings of existing keys (higher level dictionary keys)
    assert "b" in flat_dict


def test_flatdict_dunder_delitem(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(request, [test_flatdict_dunder_contains.__name__], scope="module")

    data = {"a": 1, "b": {"c": {"d": [2]}}}
    flat_dict = FlatDict(data, delimiter=".")

    # Test that the __delitem__ method correctly deletes existing keys
    del flat_dict["b.c"]
    assert "b.c.d" not in flat_dict
    assert "b.c" not in flat_dict

    # Test that the __delitem__ method raises KeyError for non-existent keys
    with pytest.raises(KeyError):
        del flat_dict["e"]

    with pytest.raises(KeyError):
        del flat_dict["b.e"]

    with pytest.raises(KeyError):
        del flat_dict["a.c"]


@pytest.mark.order("first")
@pytest.mark.dependency
def test_flatdict_dunder_equality():
    data = {"a": 1, "b": {"c": 2}}
    other_data = {"a": 1, "b": {"c": 3}}
    flat_dict1 = FlatDict(data, delimiter=".")
    flat_dict2 = FlatDict(data, delimiter=".")
    flat_dict3 = FlatDict(other_data, delimiter=".")
    flat_dict4 = FlatDict(data, delimiter="/")

    # Test that two FlatDict instances with the same content are equal
    assert flat_dict1 == flat_dict2
    assert flat_dict1 is not flat_dict2

    # Test that a FlatDict instance is equal to a regular dict with the same content
    assert flat_dict1 == data

    # Test that two FlatDict instances with different content are not equal
    assert bool(flat_dict1 == flat_dict3) is False
    assert flat_dict1 != flat_dict3

    # Test that a FlatDict instance is not equal to a regular dict with different content
    assert bool(flat_dict1 == other_data) is False
    assert flat_dict1 != other_data

    # Test that two FlatDict instances with the same content but different delimiters are not equal
    assert bool(flat_dict1 == flat_dict4) is False
    assert flat_dict1 != flat_dict4

    # Test that a comparison with a non-dict type throws a TypeError
    with pytest.raises(TypeError):
        assert flat_dict1 == 1


@pytest.mark.order("first")
@pytest.mark.dependency
def test_flatdict_dunder_getitem():
    data = {"a": 1, "b": {"c": {"d": [2]}}}
    flat_dict = FlatDict(data, delimiter=".")

    # Test that the __getitem__ method correctly retrieves existing keys
    assert data["a"] == flat_dict["a"]
    assert data["b"]["c"] == flat_dict["b.c"]
    assert data["b"]["c"]["d"] == flat_dict["b.c.d"]

    # Test that the __getitem__ method raises KeyError for non-existent keys
    with pytest.raises(KeyError):
        flat_dict["e"]

    with pytest.raises(KeyError):
        flat_dict["b.e"]

    with pytest.raises(KeyError):
        flat_dict["a.c"]


def test_flatdict_dunder_iter():
    data = {"a": 1, "b": {"c": 2}}
    flat_dict = FlatDict(data, delimiter=".")

    # Test that the __iter__ method returns an iterator over the flattened keys
    expected_key_order = ["a", "b.c"]
    actual_key_order = []
    for key in iter(flat_dict):
        actual_key_order.append(key)

    assert expected_key_order == actual_key_order


@pytest.mark.order("first")
@pytest.mark.dependency
def test_flatdict_dunder_len():
    data = {"a": 1, "b": {"c": 2}}
    flat_dict = FlatDict(data, delimiter=".")

    # Test that the __len__ method returns the correct number of flattened keys
    assert len(flat_dict) == 2


def test_flatdict_dunder_repr():
    data = {"a": 1, "b": {"c": 2}}
    flat_dict = FlatDict(data, delimiter=".")

    # Test that the __repr__ method returns a string representation of the FlatDict
    expected_repr = f"<FlatDict id={id(flat_dict)} data={{'a': 1, 'b.c': 2}}>"
    assert expected_repr == repr(flat_dict)


@pytest.mark.order("second")
@pytest.mark.dependency
def test_flatdict_dunder_setitem(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(
            request,
            [
                test_flatdict_dunder_equality.__name__,
                test_flatdict_dunder_getitem.__name__,
            ],
            scope="module",
        )

    # requires __getitem__ to test nested assignment
    flat_dict = FlatDict(delimiter=".")

    # Test that the __setitem__ method correctly sets values for new keys
    flat_dict["a"] = 1
    assert flat_dict["a"] == 1

    flat_dict["b.c"] = 2
    assert flat_dict["b.c"] == 2

    # Test that the __setitem__ method correctly updates values for existing keys
    flat_dict["a"] = 3
    assert flat_dict["a"] == 3

    flat_dict["b.c"] = 4
    assert flat_dict["b.c"] == 4

    # Test that the __setitem__ method handles assignment over existing non-dict keys
    flat_dict["b"] = 5
    assert flat_dict["b"] == 5

    # Test that the __setitem__ method handles dict assignment over existing non-dict keys
    flat_dict["b"] = {"d": 6}
    assert flat_dict["b.d"] == 6


def test_flatdict_dunder_str():
    data = {"a": 1, "b": {"c": 2}}
    flat_dict = FlatDict(data, delimiter=".")

    # Test that the __str__ method returns a string representation of the FlatDict
    expected_str = "{'a': 1, 'b.c': 2}"
    assert expected_str == str(flat_dict)


def test_flatdict_pickle(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(
            request,
            [
                test_flatdict_dunder_equality.__name__,
                test_flatdict_dunder_getitem.__name__,
            ],
            scope="module",
        )

    import pickle

    data = {"a": 1, "b": {"c": [2, 3]}}
    flat_dict = FlatDict(data, delimiter=".")

    # Test that a FlatDict instance can be pickled and unpickled correctly
    pickled = pickle.dumps(flat_dict)
    unpickled = pickle.loads(pickled)

    # Evaluate (Expected -> Actual)
    assert flat_dict == unpickled
    assert flat_dict is not unpickled
    assert flat_dict["b"] == unpickled["b"]
    assert flat_dict["b"] is not unpickled["b"]
    assert flat_dict["b"]["c"] == unpickled["b"]["c"]
    assert flat_dict["b"]["c"] is not unpickled["b"]["c"]
