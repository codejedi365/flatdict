from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple, cast

import pytest
from pytest_dependency import depends

from cj365.flatdict import FlatterDict
from cj365.flatdict.flat_dict import FlatDict

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any


class Vector(NamedTuple):
    velocity: int
    direction: tuple[int, int]


def test_flatterdict_init_from_NamedTuple(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(request, [test_flatterdict_dunder_getitem.__name__], scope="module")

    vector = Vector(velocity=1, direction=(2, 3))

    # Test that initializing a FlatterDict from a NamedTuple with an
    # internal tuple correctly converts it to a dictionary
    flatter_dict = FlatterDict(vector, delimiter=".")
    assert vector.velocity == flatter_dict["velocity"]
    assert vector.direction == (
        flatter_dict["direction.0"],
        flatter_dict["direction.1"],
    )


def test_flatterdict_init_from_flatterdict(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(request, [test_flatterdict_dunder_getitem.__name__], scope="module")

    data: dict[str, Any] = {"a": 1, "b": (2, 3)}
    flat_dict = FlatterDict(data)
    new_flat_dict = FlatterDict(flat_dict)

    assert data["a"] == new_flat_dict["a"]
    assert data["b"][0] == new_flat_dict["b.0"]
    assert data["b"][1] == new_flat_dict["b.1"]


def test_flatterdict_init_from_flatdict(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(request, [test_flatterdict_dunder_getitem.__name__], scope="module")

    data: dict[str, Any] = {"a": 1, "b": (2, 3)}
    flat_dict = FlatDict(data)
    flatter_dict = FlatterDict(flat_dict)

    assert data["a"] == flatter_dict["a"]
    assert data["b"][0] == flatter_dict["b.0"]
    assert data["b"][1] == flatter_dict["b.1"]


def test_flatterdict_init_from_flattened_dict(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(request, [test_flatterdict_inflate.__name__], scope="module")

    delimiter = "."
    flat_dict = FlatterDict({"a": 1, f"b{delimiter}0": 2}, delimiter=delimiter)
    inflated_data = flat_dict.inflate()
    expected_data = {"a": 1, "b": (2,)}

    assert expected_data == inflated_data


def test_flatterdict_init_fails_w_empty_delimiter():
    with pytest.raises(ValueError, match="Delimiter cannot be an empty string"):
        assert FlatterDict({"a": 1, "b": {"c": (2, 3)}}, delimiter="")


def test_flatterdict_flatten_delimiter_collision():
    with pytest.raises(ValueError, match="Key 'b.0' collides with the delimiter '.'"):
        assert FlatterDict.flatten({"a": 1, "b.0": 2}, delimiter=".")


def test_flatterdict_unflatten_fails_w_empty_delimiter():
    with pytest.raises(ValueError, match="Delimiter cannot be an empty string"):
        assert FlatterDict.unflatten({"a": 1, "b.0": 2}, delimiter="")


def test_flatterdict_clear(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(
            request,
            [
                test_flatterdict_dunder_equality.__name__,
                test_flatterdict_dunder_len.__name__,
            ],
            scope="module",
        )

    expected_length = 0
    empty_dict: dict[Any, Any] = {}
    empty_list: list[Any] = []

    # Test that clearing a FlatterDict removes all items
    # and results in an empty FlatterDict
    flat_dict = FlatterDict({"a": 1, "b": 2})
    flat_dict.clear()
    assert expected_length == len(flat_dict)
    assert empty_dict == flat_dict

    # Test that clearing a FlatterDict initialized from a Sequence removes all items
    # and results in an empty FlatterDict
    flat_dict = FlatterDict([{"c": 3}, {"d": 4}])
    flat_dict.clear()
    assert expected_length == len(flat_dict)
    assert empty_list == flat_dict


def test_flatterdict_clear_nested(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(
            request,
            [
                test_flatterdict_dunder_equality.__name__,
                test_flatterdict_dunder_len.__name__,
            ],
            scope="module",
        )

    expected_length = 0
    empty_dict: dict[Any, Any] = {}
    empty_list: list[Any] = []

    # Test that clearing a FlatterDict with nested dictionaries
    # removes all items and results in an empty FlatterDict
    flat_dict = FlatterDict({"a": {"b": 1}, "c": (2, 3)})
    flat_dict.clear()
    assert expected_length == len(flat_dict)
    assert empty_dict == flat_dict

    flat_dict = FlatterDict([{"a": {"b": 1}}, {"c": (2, 3)}])
    flat_dict.clear()
    assert expected_length == len(flat_dict)
    assert empty_list == flat_dict


def test_flatterdict_copy_list(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(
            request,
            [
                test_flatterdict_dunder_equality.__name__,
                test_flatterdict_dunder_getitem.__name__,
            ],
            scope="module",
        )

    # Values must be greater than 256 since python interns small integers,
    # which would cause the copy to not be a deep copy. The string concatenation is to ensure
    # that the string is not interned since string literals are also interned.
    flat_dict = FlatterDict([{"a": [100, 200]}, {"b": {"c": 300}}])

    # Test that copying a FlatterDict creates a new FlatterDict
    # with the same content but different instance (ie. a deep copy)
    flat_dict_copy = flat_dict.copy()

    # Evaluate (Expected -> Actual)
    assert flat_dict == flat_dict_copy
    assert flat_dict is not flat_dict_copy
    assert flat_dict["0"] == flat_dict_copy["0"]
    assert flat_dict["0"] is not flat_dict_copy["0"]
    assert flat_dict["0.a"] == flat_dict_copy["0.a"]
    assert flat_dict["0.a"] is not flat_dict_copy["0.a"]
    assert flat_dict["0.a.0"] == flat_dict_copy["0.a.0"]
    assert flat_dict["0.a.1"] == flat_dict_copy["0.a.1"]
    assert flat_dict["1"] == flat_dict_copy["1"]
    assert flat_dict["1"] is not flat_dict_copy["1"]
    assert flat_dict["1.b"] == flat_dict_copy["1.b"]
    assert flat_dict["1.b"] is not flat_dict_copy["1.b"]
    assert flat_dict["1.b.c"] == flat_dict_copy["1.b.c"]


def test_flatterdict_copy_nested_dict(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(
            request,
            [
                test_flatterdict_dunder_equality.__name__,
                test_flatterdict_dunder_getitem.__name__,
            ],
            scope="module",
        )

    # Values must be greater than 256 since python interns small integers,
    # which would cause the copy to not be a deep copy. The string concatenation is to ensure
    # that the string is not interned since string literals are also interned.
    flat_dict = FlatterDict(
        {"a": 100, "b": {"c": 200, "d": 300}, "e": [400, "foo" + "bar"]}
    )

    # Test that copying a FlatterDict creates a new FlatterDict
    # with the same content but different instance (ie. a deep copy)
    flat_dict_copy = flat_dict.copy()

    # Evaluate (Expected -> Actual)
    assert flat_dict == flat_dict_copy
    assert flat_dict is not flat_dict_copy
    assert flat_dict["a"] == flat_dict_copy["a"]
    assert flat_dict["b"] == flat_dict_copy["b"]
    assert flat_dict["b"] is not flat_dict_copy["b"]
    assert flat_dict["b"]["c"] == flat_dict_copy["b"]["c"]
    assert flat_dict["b"]["d"] == flat_dict_copy["b"]["d"]
    assert flat_dict["e"] == flat_dict_copy["e"]
    assert flat_dict["e"] is not flat_dict_copy["e"]
    assert flat_dict["e"][0] == flat_dict_copy["e"][0]
    assert flat_dict["e"][1] == flat_dict_copy["e"][1]


def test_flatterdict_copy_empty(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(
            request,
            [
                test_flatterdict_dunder_equality.__name__,
                test_flatterdict_dunder_len.__name__,
            ],
            scope="module",
        )

    expected_length = 0
    flat_dict = FlatterDict()
    flat_dict_copy = flat_dict.copy()

    assert flat_dict == flat_dict_copy
    assert flat_dict is not flat_dict_copy
    assert expected_length == len(flat_dict_copy)


def test_flatterdict_get():
    data = {"a": {"b": 1}, "c": (2, 3)}
    flat_dict = FlatterDict(data, delimiter=".")

    # Test that get() returns the correct values for existing keys (meta & flattened keys)
    assert data["a"] == flat_dict.get("a")
    assert data["a"]["b"] == flat_dict.get("a.b")
    assert data["c"] == flat_dict.get("c")
    assert data["c"][0] == flat_dict.get("c.0")
    assert data["c"][1] == flat_dict.get("c.1")

    # Test that get() returns None for non-existent keys without a default value
    assert None is flat_dict.get("d")
    assert None is flat_dict.get("a.c")
    assert "default" == flat_dict.get("d", "default")
    assert "default" == flat_dict.get("a.c", "default")

    # Test that get() works for a FlatterDict initialized from a Sequence
    data = [{"a": 1}, {"b": 2}]
    flat_dict = FlatterDict(data, delimiter=".")

    assert data[0] == flat_dict.get("0")
    assert data[0]["a"] == flat_dict.get("0.a")
    assert data[1] == flat_dict.get("1")
    assert data[1]["b"] == flat_dict.get("1.b")

    assert None is flat_dict.get("2")
    assert None is flat_dict.get("0.b")
    assert "default" == flat_dict.get("2", "default")
    assert "default" == flat_dict.get("0.b", "default")


@pytest.mark.order("first")
@pytest.mark.dependency
def test_flatterdict_inflate():
    # TODO: switch tuple to use a list when type casting of nested structures is implemented
    expected = {"a": 100, "b": {"c": (200, "foo" + "bar")}}
    flat_dict = FlatterDict(expected, delimiter=".")

    # Test that inflating the FlatterDict returns a dictionary equal to the original nested structure
    inflated = cast("dict[str, Any]", flat_dict.inflate())

    # Evaluate (Expected -> Actual)
    assert expected["b"]["c"][0] == inflated["b"]["c"][0]
    assert expected["b"]["c"][1] == inflated["b"]["c"][1]
    assert expected["b"]["c"] == inflated["b"]["c"]
    assert expected["b"]["c"] is not inflated["b"]["c"]
    assert expected["b"] is not inflated["b"]
    assert expected["b"] == inflated["b"]
    assert expected["a"] == inflated["a"]
    assert expected == inflated
    assert expected is not inflated

    # Test that inflating a FlatterDict initialized from a Sequence
    expected = list(expected.items())
    flat_dict = FlatterDict(expected, delimiter=".")
    inflated = cast("list[tuple[str, Any]]", flat_dict.inflate())

    assert expected == inflated
    assert expected is not inflated
    assert expected[0] == inflated[0]
    assert expected[0] is not inflated[0]
    assert expected[1] == inflated[1]
    assert expected[1] is not inflated[1]


def test_flatterdict_inflate_set():
    # Test a FlatterDict starting with a set
    expected = {"a", "b"}
    flat_dict = FlatterDict(expected, delimiter=".")
    inflated = flat_dict.inflate()

    assert expected == inflated
    assert expected is not inflated


def test_flatterdict_inflate_empty():
    expected = {}
    flat_dict = FlatterDict()

    # Test that inflating an empty FlatterDict returns an empty dictionary
    inflated = flat_dict.inflate()
    assert expected == inflated
    assert expected is not inflated

    expected = []
    flat_dict = FlatterDict([])

    # Test that inflating an empty FlatterDict initialized from a Sequence returns an empty list
    inflated = flat_dict.inflate()
    assert expected == inflated
    assert expected is not inflated

    expected = set()
    flat_dict = FlatterDict(expected)

    # Test that inflating an empty FlatterDict initialized from a Set returns an empty set
    inflated = flat_dict.inflate()
    assert expected == inflated
    assert expected is not inflated

    expected = tuple()
    flat_dict = FlatterDict(expected)

    # Test that inflating an empty FlatterDict initialized from a Tuple returns an empty tuple
    inflated = flat_dict.inflate()
    assert expected == inflated


def test_flatterdict_items():
    data = {"a": 100, "b": {"c": [200, "foo" + "bar"]}}
    expected_items = [("a", 100), ("b.c.0", 200), ("b.c.1", "foobar")]

    # Test that the items method returns the correct set of key-value pairs
    flat_dict = FlatterDict(data, delimiter=".")
    items = list(flat_dict.items())
    assert expected_items == items

    data = [{"a": 100}, {"b": 200}]
    expected_items = [("0.a", 100), ("1.b", 200)]

    # Test that the items method returns the correct set of key-value pairs for a FlatterDict initialized from a Sequence
    flat_dict = FlatterDict(data, delimiter=".")
    items = list(flat_dict.items())
    assert expected_items == items


def test_flatterdict_keys():
    data = {"a": 100, "b": {"c": [200, "foo" + "bar"]}}
    expected_keys = {"a", "b.c.0", "b.c.1"}

    # Test that the keys method returns the correct set of keys
    flat_dict = FlatterDict(data, delimiter=".")
    keys = set(flat_dict.keys())
    assert expected_keys == keys

    data = [{"a": 100}, {"b": 200}]
    expected_keys = {"0.a", "1.b"}

    # Test that the keys method returns the correct set of keys for a FlatterDict initialized from a Sequence
    flat_dict = FlatterDict(data, delimiter=".")
    keys = set(flat_dict.keys())
    assert expected_keys == keys


def test_flatterdict_pop(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(
            request,
            [
                test_flatterdict_dunder_equality.__name__,
                test_flatterdict_dunder_contains.__name__,
            ],
            scope="module",
        )

    data: dict[str, Any] = {"a": 100, "b": {"c": [200, "foo" + "bar"]}, "d": {"e": 300}}
    flat_dict = FlatterDict(data, delimiter=".")

    # Test popping a nested list key
    value = flat_dict.pop("b.c.1")
    assert data["b"]["c"][1] == value
    assert "b.c.1" not in flat_dict

    # Test popping a top-level key of a nested dictionary removing
    # the entire dictionary
    value = flat_dict.pop("d")
    assert data["d"] == value
    assert "d" not in flat_dict

    # Test popping a non-existent key without a default value
    value = flat_dict.pop("d")
    assert value is None

    # Test popping a non-existent key with a default value
    value = flat_dict.pop("d", "default")
    assert value == "default"
    assert "d" not in flat_dict

    value = flat_dict.pop("b.c")
    # TODO: Remove list() when FlatterDict handles type casting for nested structures
    assert [data["b"]["c"][0]] == list(value)
    assert "b.c" not in flat_dict

    value = flat_dict.pop("b")
    empty_dict: dict[Any, Any] = {}
    assert empty_dict == value

    # Test popping a top-level key
    value = flat_dict.pop("a")
    assert data["a"] == value
    assert "a" not in flat_dict

    # Test that popping the last key results in an empty FlatterDict
    assert flat_dict == {}

    data_list: list[dict[str, Any]] = [{"a": 100}, {"b": [200, "foo" + "bar"]}]
    flat_dict = FlatterDict(data_list, delimiter=".")

    value = flat_dict.pop("0.a")
    assert data_list[0]["a"] == value
    assert "0.a" not in flat_dict

    # Test popping a starting list value from a nested list & the
    # second value becomes the new starting list value
    value = flat_dict.pop("1.b.0")
    assert data_list[1]["b"][0] == value
    assert data_list[1]["b"][1] == flat_dict["1.b.0"]
    assert "1.b.1" not in flat_dict

    value = flat_dict.pop("1.b.0")
    assert data_list[1]["b"][1] == value
    assert "1.b.0" not in flat_dict

    value = flat_dict.pop("1.b")
    empty_list: list[Any] = []
    # TODO: remove list() when FlatterDict handles type casting for nested structures
    assert empty_list == list(value)
    assert "1.b" not in flat_dict

    value = flat_dict.pop("1")
    assert empty_dict == value
    assert "1" not in flat_dict

    value = flat_dict.pop("0")
    assert empty_dict == value
    assert "0" not in flat_dict

    # Test that popping the last key results in an empty FlatterDict
    assert empty_list == flat_dict


def test_flatterdict_setdefault(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(request, [test_flatterdict_dunder_getitem.__name__], scope="module")

    expected_values = [100, 200, "foo" + "bar", 300]
    data = {
        "a": expected_values[0],
        "b": {"c": [expected_values[1], expected_values[2]]},
        "d": {"e": expected_values[3]},
    }
    flat_dict = FlatterDict(data, delimiter=".")

    # Test that setdefault returns the existing value for an existing key
    value = flat_dict.setdefault("a", "default")
    assert expected_values[0] == value
    assert expected_values[0] == flat_dict["a"]

    # Test that setdefault returns the default value for a non-existent key and sets it in a dict
    value = flat_dict.setdefault("f", "default")
    assert "default" == value
    assert "default" == flat_dict["f"]

    value = flat_dict.setdefault("b.c.2", "default")
    assert "default" == value
    assert "default" == flat_dict["b.c.2"]
    # TODO: Remove list() when FlatterDict handles type casting for nested structures
    assert [expected_values[1], expected_values[2], "default"] == list(flat_dict["b.c"])

    # Test that setdefault does not overwrite an existing nested key
    value = flat_dict.setdefault("d.e", "default")
    assert expected_values[3] == value
    assert expected_values[3] == flat_dict["d.e"]


def test_flatterdict_set_delimiter(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(request, [test_flatterdict_dunder_getitem.__name__], scope="module")

    data: dict[str, Any] = {"a": 100, "b": {"c": [200, "foo" + "bar"]}, "d": {"e": 300}}
    flat_dict = FlatterDict(data, delimiter=".")

    # Test that changing the delimiter updates the internal structure
    # and allows access with the new delimiter
    flat_dict.delimiter = "/"
    assert data["a"] == flat_dict["a"]
    assert data["b"]["c"][0] == flat_dict["b/c/0"]
    assert data["d"]["e"] == flat_dict["d/e"]

    with pytest.raises(KeyError, match="Key 'b.c' not found in 'FlatterDict'"):
        assert flat_dict["b.c"]

    with pytest.raises(ValueError, match="Delimiter cannot be an empty string"):
        flat_dict.set_delimiter("")


def test_flatterdict_update_merge(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(request, [test_flatterdict_dunder_getitem.__name__], scope="module")

    data: dict[str, Any] = {"a": 1, "b": {"c": [2]}}
    flat_dict = FlatterDict(data, delimiter=".")

    # Test that updating the FlatterDict with a new dictionary correctly updates the content
    new_data: dict[str, Any] = {"b": {"d": 3}, "e": 4}
    flat_dict.update(new_data)

    # Old data is still accessible and unchanged
    assert data["a"] == flat_dict["a"]
    assert data["b"]["c"][0] == flat_dict["b.c.0"]
    # TODO: Remove list() when FlatterDict handles type casting for nested structures
    assert data["b"]["c"] == list(flat_dict["b.c"])

    # New data is accessible
    assert new_data["b"]["d"] == flat_dict["b.d"]
    assert new_data["e"] == flat_dict["e"]

    # New data is merged
    # TODO: switch this back to using the original data["b"] when FlatterDict handles type casting for nested structures
    # expected_merge: dict[str, Any] = {**data["b"], **new_data["b"]}
    expected_merge: dict[str, Any] = {**{"c": tuple(data["b"]["c"])}, **new_data["b"]}
    assert expected_merge == flat_dict["b"]

    # Test updating the FlatterDict with kwargs
    new_data = {"f": 5, "g": {"h": 6}}
    flat_dict.update(f=new_data["f"], g=new_data["g"])
    assert new_data["f"] == flat_dict["f"]
    assert new_data["g"]["h"] == flat_dict["g.h"]
    assert new_data["g"] == flat_dict["g"]

    # Test updating the FlatterDict with iterable of key-value pairs
    new_data_list: list[tuple[str, Any]] = [("i", 7), ("j", {"k": 8})]
    flat_dict.update(new_data_list)
    assert new_data_list[0][1] == flat_dict[new_data_list[0][0]]
    assert new_data_list[1][1]["k"] == flat_dict["j.k"]

    data_list: list[dict[str, Any]] = [{"a": 1}, {"b": {"c": [2]}}]
    flat_dict = FlatterDict(data_list, delimiter=".")

    with pytest.raises(
        ValueError,
        match="Cannot update a Set-initialized or Sequence-initialized FlatterDict with non-integer keys",
    ):
        new_data_list = [("b", {"d": 3}), ("e", 4)]
        flat_dict.update(new_data_list)

    new_data_list = [("1", {"b": {"d": 3}}), ("2", {"e": 4})]
    flat_dict.update(new_data_list)
    assert data_list[0]["a"] == flat_dict["0.a"]
    assert data_list[1]["b"]["c"][0] == flat_dict["1.b.c.0"]
    # TODO: Remove list() when FlatterDict handles type casting for nested structures
    assert data_list[1]["b"]["c"] == list(flat_dict["1.b.c"])
    assert new_data_list[0][1]["b"]["d"] == flat_dict["1.b.d"]
    assert new_data_list[1][1]["e"] == flat_dict["2.e"]

    # TODO: simplify this
    expected_merge = {
        **{"c": tuple(data_list[1]["b"]["c"])},
        **new_data_list[0][1]["b"],
    }
    assert expected_merge == flat_dict["1.b"]


def test_flatterdict_update_overwrite(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(request, [test_flatterdict_dunder_getitem.__name__], scope="module")

    data: dict[str, Any] = {"a": 1, "b": {"c": [2]}}
    flat_dict = FlatterDict(data, delimiter=".")

    # Test that updating the FlatterDict with a new dictionary correctly overwrites existing keys
    new_data: dict[str, Any] = {"a": 3, "b": {"c": [4]}}
    flat_dict.update(new_data)
    assert new_data["a"] == flat_dict["a"]
    assert new_data["b"]["c"][0] == flat_dict["b.c.0"]
    # TODO: Remove list() when FlatterDict handles type casting for nested structures
    assert new_data["b"]["c"] == list(flat_dict["b.c"])
    # assert new_data["b"] == flat_dict["b"]

    # Initialize a FlatterDict from a Sequence
    data_list: list[tuple[str, Any]] = [("a", 1), ("b", {"c": [2]})]
    flat_dict = FlatterDict(data_list, delimiter=".")

    # Test that updating the FlatterDict with a new sequence correctly overwrites existing
    # keys in a Sequence-initialized FlatterDict
    new_data_list: list[tuple[str, Any]] = [("0", {"a": 3}), ("1", {"b": {"c": [4]}})]
    flat_dict.update(new_data_list)
    assert new_data_list[0][1]["a"] == flat_dict["0.a"]
    assert new_data_list[1][1]["b"]["c"][0] == flat_dict["1.b.c.0"]
    assert new_data_list[1][1]["b"]["c"] == list(flat_dict["1.b.c"])

    # TODO: simplify this
    expected_merge = {**{"c": tuple(new_data_list[1][1]["b"]["c"])}}
    assert expected_merge == flat_dict["1.b"]


def test_flatterdict_update_restructure(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(request, [test_flatterdict_dunder_getitem.__name__], scope="module")

    data: dict[str, Any] = {"a": 1, "b": {"c": [2]}}
    flat_dict = FlatterDict(data, delimiter=".")

    # Test that updating the FlatterDict with a new dictionary correctly
    # restructures the content
    new_data: dict[str, Any] = {"b": 3}
    flat_dict.update(new_data)
    assert data["a"] == flat_dict["a"]
    assert new_data["b"] == flat_dict["b"]
    with pytest.raises(KeyError, match="Key 'b.c' not found in 'FlatterDict'"):
        assert flat_dict["b.c"]

    # Test that updating the FlatterDict with a new dictionary correctly
    # restructures the content again
    new_data = {"b": {"d": 4}}
    flat_dict.update(new_data)
    assert data["a"] == flat_dict["a"]
    assert new_data["b"]["d"] == flat_dict["b.d"]
    with pytest.raises(KeyError, match="Key 'b.c' not found in 'FlatterDict'"):
        assert flat_dict["b.c"]

    # Test that updating the FlatterDict with a new dictionary correctly
    # restructures the content again with a sequence value
    new_data = {"b": {"d": [5]}}
    flat_dict.update(new_data)
    assert data["a"] == flat_dict["a"]
    assert new_data["b"]["d"][0] == flat_dict["b.d.0"]
    # TODO: Remove list() when FlatterDict handles type casting for nested structures
    assert new_data["b"]["d"] == list(flat_dict["b.d"])
    with pytest.raises(KeyError, match="Key 'b.d.1' not found in 'FlatterDict'"):
        assert flat_dict["b.d.1"]


def test_flatterdict_update_empty(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(request, [test_flatterdict_dunder_getitem.__name__], scope="module")

    data: dict[str, Any] = {
        "a": 100,
        "b": {"c": 200, "d": 300},
        "e": [400, "foo" + "bar"],
    }
    flat_dict = FlatterDict(data, delimiter=".")

    # Test that updating the FlatterDict with an empty dictionary does not change the content
    flat_dict.update({})
    assert data["a"] == flat_dict["a"]
    assert data["b"]["c"] == flat_dict["b.c"]
    assert data["b"]["d"] == flat_dict["b.d"]
    assert data["e"][0] == flat_dict["e.0"]
    assert data["e"][1] == flat_dict["e.1"]
    # TODO: remove list() after type casting fix
    assert data["e"] == list(flat_dict["e"])

    # Initialize a FlatterDict from a Sequence
    data_list: list[dict[str, Any]] = [{"a": 100}, {"b": {"c": 200}}]
    flat_dict = FlatterDict(data_list, delimiter=".")

    # Test a merge an empty list into a Sequence-initialized FlatterDict does not change the content
    flat_dict.update([])
    assert data_list[0]["a"] == flat_dict["0.a"]
    assert data_list[1]["b"]["c"] == flat_dict["1.b.c"]
    assert data_list[1]["b"] == flat_dict["1.b"]
    assert data_list[0] == flat_dict["0"]
    assert data_list[1] == flat_dict["1"]

    # Test a merge an empty dictionary into a Sequence-initialized FlatterDict does not change the content
    flat_dict.update({})
    assert data_list[0]["a"] == flat_dict["0.a"]
    assert data_list[1]["b"]["c"] == flat_dict["1.b.c"]
    assert data_list[1]["b"] == flat_dict["1.b"]
    assert data_list[0] == flat_dict["0"]
    assert data_list[1] == flat_dict["1"]


def test_flatterdict_update_from_flatterdict(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(request, [test_flatterdict_dunder_getitem.__name__], scope="module")

    base_data: dict[str, Any] = {"a": 1, "b": {"c": [2, 3], "d": 4}}
    base_flat_dict = FlatterDict(base_data, delimiter=".")

    # Test merging a FlatterDict with overlapping and new keys into another FlatterDict
    update_data: dict[str, Any] = {"b": {"d": 99, "e": 5}, "f": 6}
    update_flat_dict = FlatterDict(update_data, delimiter=".")
    base_flat_dict.update(update_flat_dict)

    # Original key unchanged
    assert base_data["a"] == base_flat_dict["a"]
    # Nested sequence key preserved from base where not overwritten
    assert base_data["b"]["c"][0] == base_flat_dict["b.c.0"]
    assert base_data["b"]["c"][1] == base_flat_dict["b.c.1"]
    # Overlapping nested key overwritten by update
    assert update_data["b"]["d"] == base_flat_dict["b.d"]
    # New nested key added from update
    assert update_data["b"]["e"] == base_flat_dict["b.e"]
    # New top-level key added from update
    assert update_data["f"] == base_flat_dict["f"]

    # Test that updating with an empty FlatterDict does not change the content
    before_keys = set(base_flat_dict.keys())
    base_flat_dict.update(FlatterDict())
    assert before_keys == set(base_flat_dict.keys())


@pytest.mark.order("third")
@pytest.mark.dependency
def test_flatterdict_values(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(request, [test_flatterdict_dunder_setitem.__name__], scope="module")

    initial_values = [1, 2, 3]
    data = {"a": initial_values[0], "b": {"c": (initial_values[1], initial_values[2])}}
    flat_dict = FlatterDict(data, delimiter=".")

    # Test that the values method returns the correct set of values
    # corresponding to the flattened keys
    values = flat_dict.values()
    actual_values = list(values)
    assert initial_values == actual_values

    # Test use of ValuesViewer when the FlatterDict is modified
    # after calling values()
    flat_dict["d"] = 3  # requires __setitem__
    actual_values = list(values)
    expected = [*initial_values, 3]
    assert expected == actual_values


@pytest.mark.order("first")
@pytest.mark.dependency
def test_flatterdict_dunder_contains():
    data = {"a": 1, "b": {"c": [2, 3]}, "d": [{"e": 4}]}
    flat_dict = FlatterDict(data, delimiter=".")

    # Test that the __contains__ method correctly identifies existing keys
    assert "a" in flat_dict
    assert "b.c" in flat_dict
    # sequence type keys
    assert "d.0.e" in flat_dict
    assert "b.c.0" in flat_dict

    # Test that the __contains__ method correctly identifies non-existent keys
    assert "f" not in flat_dict
    assert "b.d" not in flat_dict
    assert "a.c" not in flat_dict
    assert "d.1" not in flat_dict
    assert "d.0.f" not in flat_dict

    # Test that the __contains__ method correctly identifies meta keys
    # substrings of existing keys (higher level dictionary & sequence keys)
    assert "b" in flat_dict
    assert "d" in flat_dict
    assert "d.0" in flat_dict
    assert "b.c" in flat_dict

    # Start with Sequence data
    data = [{"a": 1}, {"b": 2}]
    flat_dict = FlatterDict(data, delimiter=".")

    # Test that the __contains__ method correctly identifies existing keys
    assert "0.a" in flat_dict
    assert "1.b" in flat_dict

    # Test that the __contains__ method correctly identifies non-existent keys
    assert "0.b" not in flat_dict
    assert "1.a" not in flat_dict
    assert "2" not in flat_dict

    # Test that the __contains__ method correctly identifies meta keys
    assert "0" in flat_dict
    assert "1" in flat_dict

    # Start with Set data
    data = {"a", "b"}
    flat_dict = FlatterDict(data, delimiter=".")

    # Test that the __contains__ method correctly identifies existing keys
    assert "0" in flat_dict
    assert "1" in flat_dict

    # Test that the __contains__ method correctly identifies non-existent keys
    assert "2" not in flat_dict


def test_flatterdict_dunder_delitem(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(
            request,
            [
                test_flatterdict_dunder_contains.__name__,
                test_flatterdict_dunder_getitem.__name__,
            ],
            scope="module",
        )

    data: dict[str, Any] = {
        "a": 100,
        "b": {"c": 200, "d": 300},
        "e": [400, "foo" + "bar"],
    }
    flat_dict = FlatterDict(data, delimiter=".")

    # Test that the __delitem__ method correctly deletes existing keys
    del flat_dict["b"]
    assert "b.c.d" not in flat_dict
    assert "b.c" not in flat_dict

    del flat_dict["e.0"]
    assert "e.0" in flat_dict
    assert "e.1" not in flat_dict
    assert data["e"][1] == flat_dict["e.0"]

    # Test that the __delitem__ method raises KeyError for non-existent keys
    with pytest.raises(KeyError, match="Key 'f' not found in 'FlatterDict'"):
        del flat_dict["f"]

    with pytest.raises(KeyError, match="Key 'b.e' not found in 'FlatterDict'"):
        del flat_dict["b.e"]

    with pytest.raises(KeyError, match="Key 'a.c' not found in 'FlatterDict'"):
        del flat_dict["a.c"]


@pytest.mark.order("first")
@pytest.mark.dependency
def test_flatterdict_dunder_equality():
    data = {"a": 1, "b": {"c": (2, 3)}, "d": ({"e": 4},)}
    other_data = tuple(data.items())
    flat_dict1 = FlatterDict(data, delimiter=".")
    flat_dict2 = FlatterDict(data, delimiter=".")
    flat_dict3 = FlatterDict(other_data, delimiter=".")
    flat_dict4 = FlatterDict(other_data, delimiter=".")
    flat_dict5 = FlatterDict(data, delimiter="/")

    # Test that two FlatterDict instances with the same content are equal
    assert flat_dict1 == flat_dict2
    assert flat_dict1 is not flat_dict2

    # Test that a FlatterDict instance is equal to a regular dict with the same content
    assert flat_dict1 == data

    # Test that two FlatterDict instances with different content are not equal
    assert bool(flat_dict1 == flat_dict3) is False
    assert flat_dict1 != flat_dict3

    # Test that a FlatterDict instance is not equal to a regular dict with different content
    assert bool(flat_dict1 == other_data) is False
    assert flat_dict1 != other_data

    # Test that two FlatterDict instances that start as Sequences with the same content are equal
    assert flat_dict3 == flat_dict4
    assert flat_dict3 is not flat_dict4

    # Test that a FlatterDict instance that starts as a Sequence is equal to the same sequence
    assert flat_dict3 == other_data

    # Test that two FlatterDict instances with the same content but different delimiters are not equal
    assert bool(flat_dict1 == flat_dict5) is False
    assert flat_dict1 != flat_dict5

    # Test that a comparison with a non-dict or non-sequence type throws a TypeError
    with pytest.raises(TypeError):
        assert flat_dict1 == 1


@pytest.mark.order("first")
@pytest.mark.dependency
def test_flatterdict_dunder_getitem():
    data = {"a": 1, "b": {"c": (2, 3)}, "d": ({"e": 4},)}
    flat_dict = FlatterDict(data, delimiter=".")

    # Test that the __getitem__ method correctly retrieves existing values from keys
    assert data["a"] == flat_dict["a"]
    assert data["b"]["c"][0] == flat_dict["b.c.0"]
    assert data["d"][0]["e"] == flat_dict["d.0.e"]

    # Test that the __getitem__ method correctly retrieves existing values from meta keys
    assert data["b"]["c"] == flat_dict["b.c"]
    assert data["d"] == flat_dict["d"]
    assert data["d"][0] == flat_dict["d.0"]

    # Test that the __getitem__ method raises KeyError for non-existent keys
    with pytest.raises(KeyError, match="Key 'e' not found in 'FlatterDict'"):
        flat_dict["e"]

    with pytest.raises(KeyError, match="Key 'b.e' not found in 'FlatterDict'"):
        flat_dict["b.e"]

    with pytest.raises(KeyError, match="Key 'a.c' not found in 'FlatterDict'"):
        flat_dict["a.c"]

    data = tuple(data.items())
    flat_dict = FlatterDict(data, delimiter=".")

    # Test that the __getitem__ method correctly retrieves existing keys for a FlatterDict initialized from a Sequence
    assert data[0][1] == flat_dict["0.1"]

    # Test that the __getitem__ method correctly retrieves existing values from meta keys for a FlatterDict initialized from a Sequence
    assert data[1][1]["c"] == flat_dict["1.1.c"]
    assert data[2][1][0]["e"] == flat_dict["2.1.0.e"]


def test_flatterdict_dunder_iter():
    data = {"a": 100, "b": {"c": 200, "d": 300}, "e": [400, "foo" + "bar"]}
    flat_dict = FlatterDict(data, delimiter=".")

    # Test that the __iter__ method returns an iterator over the flattened keys
    expected_key_order = ["a", "b.c", "b.d", "e.0", "e.1"]
    actual_key_order = []
    for key in iter(flat_dict):
        actual_key_order.append(key)

    assert expected_key_order == actual_key_order

    # Test __iter__() for a FlatterDict initialized from a Sequence
    data = [{"a": 100}, {"b": 200}]
    flat_dict = FlatterDict(data, delimiter=".")

    expected_key_order = ["0.a", "1.b"]
    actual_key_order = []
    for key in iter(flat_dict):
        actual_key_order.append(key)

    assert expected_key_order == actual_key_order


@pytest.mark.order("first")
@pytest.mark.dependency
def test_flatterdict_dunder_len():
    data = {"a": 1, "b": {"c": (2, 3)}, "d": ({"e": 4},)}
    expected_length = 4  # "a", "b.c.0", "b.c.1", "d.0.e"

    flat_dict = FlatterDict(data, delimiter=".")
    assert expected_length == len(flat_dict)


def test_flatterdict_dunder_repr():
    data = {"a": 100, "b": {"c": 200, "d": 300}, "e": [400, "foo" + "bar"]}
    flat_dict = FlatterDict(data, delimiter=".")

    # Test that the __repr__ method returns a string representation of the FlatterDict
    expected_repr = f"<FlatterDict id={id(flat_dict)} data={{'a': 100, 'b.c': 200, 'b.d': 300, 'e.0': 400, 'e.1': 'foobar'}}>"
    assert expected_repr == repr(flat_dict)


@pytest.mark.order("second")
@pytest.mark.dependency
def test_flatterdict_dunder_setitem(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(
            request,
            [
                test_flatterdict_dunder_equality.__name__,
                test_flatterdict_dunder_getitem.__name__,
            ],
            scope="module",
        )

    data: dict[str, Any] = {"a": 1, "b": {"c": (2, 3)}, "d": ({"e": 4},), "f": {"g": 5}}

    # starts with empty FlatterDict to test assignment of new keys
    flat_dict = FlatterDict(delimiter=".")

    # Test setting values for new keys
    # Top level key-value
    flat_dict["a"] = 3
    assert flat_dict["a"] == 3

    # Nested dictionary key-value
    flat_dict["f.g"] = 10
    assert flat_dict["f.g"] == 10

    # Insert Internal key value of a dict that is of an internal sequence type (building types as needed)
    flat_dict["d.0.e"] = 8
    assert flat_dict["d.0.e"] == 8

    # key-value with sequence value
    flat_dict["b.c"] = (1, 2, 3)
    assert flat_dict["b.c"] == (1, 2, 3)

    # Test updating values for existing keys
    # Overwrites existing top level key-value
    flat_dict["a"] = data["a"]
    assert flat_dict["a"] == data["a"]

    # Overwrites existing nested key-value
    flat_dict["f.g"] = data["f"]["g"]
    assert flat_dict["f.g"] == data["f"]["g"]

    # Overwrites existing internal sequence key-value
    flat_dict["d.0.e"] = data["d"][0]["e"]
    assert flat_dict["d.0.e"] == data["d"][0]["e"]

    # Overwrites existing key-value with sequence value
    flat_dict["b.c"] = data["b"]["c"]
    assert flat_dict["b.c"] == data["b"]["c"]

    # Insertions built expected data structure
    assert flat_dict == data

    # Type Change Tests
    # -----------------

    # Test assignment over existing non-dict keys
    flat_dict["f"] = 5
    assert flat_dict["f"] == 5

    # Test dict assignment over existing non-dict keys
    flat_dict["f"] = data["f"]
    assert flat_dict["f.g"] == data["f"]["g"]

    # Test handling of non-dict assignment into existing sequence
    flat_dict["d.0"] = 7
    assert flat_dict["d.0"] == 7

    # Test handling of dict assignment into existing sequence
    flat_dict["d.0"] = data["d"][0]
    assert flat_dict["d.0.e"] == data["d"][0]["e"]

    # Test handling of non-sequence assignment to replace existing sequence
    flat_dict["b.c"] = 9
    assert flat_dict["b.c"] == 9

    # Test handling of sequence assignment to replace existing non-sequence
    flat_dict["b.c"] = data["b"]["c"]
    assert flat_dict["b.c"] == data["b"]["c"]

    # Modifications changed and returned expected data structure
    assert flat_dict == data

    # Test insertions to ending of existing sequence
    flat_dict[f"b.c.{len(data['b']['c'])}"] = 10
    assert flat_dict["b.c"] == (*data["b"]["c"], 10)

    # Test insertions to beyond the end of existing sequence
    flat_dict[f"b.c.{len(data['b']['c']) + 2}"] = 12
    assert flat_dict["b.c"] == (*data["b"]["c"], 10, None, 12)

    # Test insertions into existing empty sequence
    flat_dict["h"] = []
    flat_dict["h.0"] = 1
    assert flat_dict["h.0"] == 1

    with pytest.raises(
        KeyError, match="Cannot set key on sequence with non-integer key"
    ):
        flat_dict["h.a"] = 2

    # Test __setitem__ with a FlatterDict value
    flat_dict["j"] = FlatterDict({"k": 100})
    assert flat_dict["j.k"] == 100

    # Working with a Sequence-based FlatterDict
    # -----------------------------------------
    data_list: list[dict[str, Any]] = [{"a": 1}, {"b": 2}]
    flat_dict = FlatterDict([], delimiter=".")

    # Test setting values for new keys in a FlatterDict initialized from a Sequence
    flat_dict["0.a"] = 3
    assert flat_dict["0.a"] == 3

    # Test appending to an existing sequence via key
    flat_dict["1"] = {"b": 10}
    assert flat_dict["1.b"] == 10

    # Test overwriting an existing sequence with a non-sequence value
    flat_dict["1"] = 5
    assert flat_dict["1"] == 5

    # Test overwriting an existing non-sequence value with a sequence
    flat_dict["1"] = data_list[1]
    assert flat_dict["1.b"] == data_list[1]["b"]

    # Test modifying into an existing dictionary value with a sequence assignment
    flat_dict["0.a.c"] = 10
    assert flat_dict["0.a.c"] == 10
    assert flat_dict["0.a"] == {"c": 10}

    # Test modifying into an existing dictionary value with a non-sequence assignment
    flat_dict["0.a"] = data_list[0]["a"]
    assert flat_dict["0.a"] == data_list[0]["a"]

    # Test that modifications to a FlatterDict initialized from a Sequence built the expected data structure
    assert flat_dict == data_list

    with pytest.raises(
        KeyError, match="Cannot set key on sequence with non-integer key"
    ):
        flat_dict["a"] = 2


def test_flatterdict_dunder_str():
    data = {"a": 100, "b": {"c": 200, "d": 300}, "e": [400, "foo" + "bar"]}
    flat_dict = FlatterDict(data, delimiter=".")

    # Test that the __str__ method returns a string representation of the FlatterDict
    expected_str = "{'a': 100, 'b.c': 200, 'b.d': 300, 'e.0': 400, 'e.1': 'foobar'}"
    assert expected_str == str(flat_dict)


def test_flatterdict_pickle(request: pytest.FixtureRequest):
    if not str(request.config.getoption("-k")):
        depends(
            request,
            [
                test_flatterdict_dunder_equality.__name__,
                test_flatterdict_dunder_getitem.__name__,
            ],
            scope="module",
        )

    import pickle

    data = {"a": 100, "b": {"c": 200, "d": 300}, "e": [400, "foo" + "bar"]}
    flat_dict = FlatterDict(data)

    # Test that a FlatterDict instance can be pickled and unpickled correctly
    pickled = pickle.dumps(flat_dict)
    unpickled = pickle.loads(pickled)

    # Evaluate (Expected -> Actual)
    assert flat_dict == unpickled
    assert flat_dict is not unpickled
    assert flat_dict["a"] == unpickled["a"]
    assert flat_dict["b"] == unpickled["b"]
    assert flat_dict["b"] is not unpickled["b"]
    assert flat_dict["b"]["c"] == unpickled["b"]["c"]
    assert flat_dict["b"]["d"] == unpickled["b"]["d"]
    assert flat_dict["e"] == unpickled["e"]
    assert flat_dict["e"] is not unpickled["e"]
    assert flat_dict["e"][0] == unpickled["e"][0]
    assert flat_dict["e"][1] == unpickled["e"][1]
