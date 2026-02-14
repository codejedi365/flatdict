from cj365.flatdict import FlatDict, FlatterDict


def test_flatdict():
    """Test core FlatDict functionality for Python 3.6 compatibility."""
    print("Testing FlatDict...")

    # Test initialization with nested dict
    nested = {"a": {"b": {"c": 1}}, "d": 2}
    fd = FlatDict(nested)
    assert fd["a.b.c"] == 1
    assert fd["d"] == 2
    print("  ✓ Nested dict initialization")

    # Test delimiter property
    assert fd.delimiter == "."
    fd.delimiter = ":"
    assert fd.delimiter == ":"
    assert fd["a:b:c"] == 1
    fd.set_delimiter(".")
    print("  ✓ Delimiter property and setter")

    # Test meta_keys
    assert "a" in fd.meta_keys
    assert "a.b" in fd.meta_keys
    print("  ✓ Meta keys")

    # Test inflate
    inflated = fd.inflate()
    assert inflated == nested
    print("  ✓ Inflate")

    # Test __setitem__ and __getitem__
    fd["e.f.g"] = 3
    assert fd["e.f.g"] == 3
    assert fd["e.f"] == {"g": 3}
    print("  ✓ Set and get items")

    # Test __contains__
    assert "a.b.c" in fd
    assert "nonexistent" not in fd
    print("  ✓ Contains check")

    # Test get with default
    assert fd.get("nonexistent", "default") == "default"
    assert fd.get("a.b.c") == 1
    print("  ✓ Get with default")

    # Test setdefault
    fd.setdefault("new.key", 42)
    assert fd["new.key"] == 42
    fd.setdefault("new.key", 99)
    assert fd["new.key"] == 42
    print("  ✓ Setdefault")

    # Test keys, values, items
    keys = list(fd.keys())
    values = list(fd.values())
    items = list(fd.items())
    assert len(keys) > 0
    assert len(values) == len(keys)
    assert len(items) == len(keys)
    print("  ✓ Keys, values, items")

    # Test __len__
    length = len(fd)
    assert length == len(keys)
    print("  ✓ Length")

    # Test __iter__
    for key in fd:
        assert key in keys
    print("  ✓ Iteration")

    # Test pop
    val = fd.pop("new.key", None)
    assert val == 42
    assert "new.key" not in fd
    print("  ✓ Pop")

    # Test update
    fd.update({"x": 1, "y": {"z": 2}})
    assert fd["x"] == 1
    assert fd["y.z"] == 2
    print("  ✓ Update")

    # Test __delitem__
    fd["temp"] = "delete_me"
    assert "temp" in fd
    del fd["temp"]
    assert "temp" not in fd
    print("  ✓ Delete item")

    # Test copy
    fd_copy = fd.copy()
    assert fd_copy == fd
    assert fd_copy is not fd
    print("  ✓ Copy")

    # Test __eq__ and __ne__
    fd2 = FlatDict(fd.inflate())
    assert fd == fd2
    assert not (fd != fd2)
    print("  ✓ Equality")

    # Test clear
    fd_temp = FlatDict({"a": 1, "b": 2})
    fd_temp.clear()
    assert len(fd_temp) == 0
    print("  ✓ Clear")

    # Test flatten static method
    flat = FlatDict.flatten({"a": {"b": 1}}, ".")
    assert flat == {"a.b": 1}
    print("  ✓ Flatten static method")

    # Test unflatten static method
    unflat = FlatDict.unflatten({"a.b": 1}, ".")
    assert unflat == {"a": {"b": 1}}
    print("  ✓ Unflatten static method")

    # Test __repr__ and __str__
    repr_str = repr(fd)
    assert "FlatDict" in repr_str
    str_str = str(fd)
    assert "{" in str_str
    print("  ✓ Repr and str")

    # Test __getstate__ and __setstate__
    state = fd.__getstate__()
    fd_restored = FlatDict()
    fd_restored.__setstate__(state)
    assert fd_restored == fd
    print("  ✓ Getstate and setstate")

    print("FlatDict tests passed!\n")


def test_flatterdict():
    """Test core FlatterDict functionality for Python 3.6 compatibility."""
    print("Testing FlatterDict...")

    # Test initialization with nested dict
    nested = {"a": {"b": {"c": 1}}, "d": 2}
    fld = FlatterDict(nested)
    assert fld["a.b.c"] == 1
    assert fld["d"] == 2
    print("  ✓ Nested dict initialization")

    # Test initialization with list
    list_data = [1, 2, {"a": 3}]
    fld_list = FlatterDict(list_data)
    assert fld_list["0"] == 1
    assert fld_list["1"] == 2
    assert fld_list["2.a"] == 3
    print("  ✓ List initialization")

    # Test initialization with tuple
    tuple_data = (1, 2, 3)
    fld_tuple = FlatterDict(tuple_data)
    assert fld_tuple["0"] == 1
    assert fld_tuple["2"] == 3
    print("  ✓ Tuple initialization")

    # Test initialization with set
    set_data = {1, 2, 3}
    fld_set = FlatterDict(set_data)
    assert len(fld_set) == 3
    print("  ✓ Set initialization")

    # Test delimiter property
    assert fld.delimiter == "."
    fld.delimiter = ":"
    assert fld.delimiter == ":"
    assert fld["a:b:c"] == 1
    fld.set_delimiter(".")
    print("  ✓ Delimiter property and setter")

    # Test meta_keys
    assert "a" in fld.meta_keys
    assert "a.b" in fld.meta_keys
    print("  ✓ Meta keys")

    # Test inflate
    inflated = fld.inflate()
    assert inflated == nested
    print("  ✓ Inflate")

    # Test inflate with list
    inflated_list = fld_list.inflate()
    assert inflated_list == list_data
    print("  ✓ Inflate list")

    # Test __setitem__ and __getitem__
    fld["e.f.g"] = 3
    assert fld["e.f.g"] == 3
    assert fld["e.f"] == {"g": 3}
    print("  ✓ Set and get items")

    # Test __setitem__ with list
    fld["h"] = [1, 2, 3]
    assert fld["h.0"] == 1
    assert fld["h.1"] == 2
    print("  ✓ Set list item")

    # Test __contains__
    assert "a.b.c" in fld
    assert "nonexistent" not in fld
    print("  ✓ Contains check")

    # Test get with default
    assert fld.get("nonexistent", "default") == "default"
    assert fld.get("a.b.c") == 1
    print("  ✓ Get with default")

    # Test setdefault
    fld.setdefault("new.key", 42)
    assert fld["new.key"] == 42
    fld.setdefault("new.key", 99)
    assert fld["new.key"] == 42
    print("  ✓ Setdefault")

    # Test keys, values, items
    keys = list(fld.keys())
    values = list(fld.values())
    items = list(fld.items())
    assert len(keys) > 0
    assert len(values) == len(keys)
    assert len(items) == len(keys)
    print("  ✓ Keys, values, items")

    # Test __len__
    length = len(fld)
    assert length == len(keys)
    print("  ✓ Length")

    # Test __iter__
    for key in fld:
        assert key in keys
    print("  ✓ Iteration")

    # Test pop
    val = fld.pop("new.key", None)
    assert val == 42
    assert "new.key" not in fld
    print("  ✓ Pop")

    # Test update
    fld.update({"x": 1, "y": {"z": 2}})
    assert fld["x"] == 1
    assert fld["y.z"] == 2
    print("  ✓ Update")

    # Test update with list
    fld.update({"z": [10, 20]})
    assert fld["z.0"] == 10
    assert fld["z.1"] == 20
    print("  ✓ Update with list")

    # Test __delitem__
    fld["temp"] = "delete_me"
    assert "temp" in fld
    del fld["temp"]
    assert "temp" not in fld
    print("  ✓ Delete item")

    # Test copy
    fld_copy = fld.copy()
    assert fld_copy == fld
    assert fld_copy is not fld
    print("  ✓ Copy")

    # Test __eq__ and __ne__
    fld2 = FlatterDict(fld.inflate())
    assert fld == fld2
    assert not (fld != fld2)
    print("  ✓ Equality")

    # Test equality with list
    fld_list2 = FlatterDict([1, 2, {"a": 3}])
    assert fld_list == fld_list2
    print("  ✓ Equality with list")

    # Test clear
    fld_temp = FlatterDict({"a": 1, "b": 2})
    fld_temp.clear()
    assert len(fld_temp) == 0
    print("  ✓ Clear")

    # Test flatten static method
    flat = FlatterDict.flatten({"a": {"b": 1}}, ".")
    assert flat == {"a.b": 1}
    print("  ✓ Flatten static method")

    # Test flatten with list
    flat_list = FlatterDict.flatten([1, 2, 3], ".")
    assert flat_list == {"0": 1, "1": 2, "2": 3}
    print("  ✓ Flatten list")

    # Test unflatten static method
    unflat = FlatterDict.unflatten({"a.b": 1}, ".")
    assert unflat == {"a": {"b": 1}}
    print("  ✓ Unflatten static method")

    # Test __repr__ and __str__
    repr_str = repr(fld)
    assert "FlatterDict" in repr_str
    str_str = str(fld)
    assert "{" in str_str
    print("  ✓ Repr and str")

    # Test __getstate__ and __setstate__
    state = fld.__getstate__()
    fld_restored = FlatterDict()
    fld_restored.__setstate__(state)
    assert fld_restored == fld
    print("  ✓ Getstate and setstate")

    # Test nested list structures
    nested_list = {"items": [{"name": "a"}, {"name": "b"}]}
    fld_nested = FlatterDict(nested_list)
    assert fld_nested["items.0.name"] == "a"
    assert fld_nested["items.1.name"] == "b"
    print("  ✓ Nested list structures")

    print("FlatterDict tests passed!\n")


if __name__ == "__main__":
    print("=" * 60)
    print("Python 3.6 Compatibility Test Suite")
    print("=" * 60 + "\n")

    try:
        test_flatdict()
        test_flatterdict()
        print("=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
    except Exception as e:
        print("\n" + "=" * 60)
        print("Test failed! ✗")
        print("::error:: Error: {}".format(str(e)))
        print("=" * 60)
        raise
