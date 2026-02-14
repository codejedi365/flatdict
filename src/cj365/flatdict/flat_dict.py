"""
This module contains the implementation of the :class:`FlatDict` class,
which provides a dictionary-like interface for working with nested dictionaries
using delimited keys.
"""
# +-------------------------------------------------------------------+
# | Module: cj365.flatdict.flat_dict                                  |
# | Author: codejedi365, 2026                                         |
# | * Portions Copyright (c) 2020-2024, Dennis Henry                  |
# | * Portions Copyright (c) 2013-2020, Gavin M. Roy                  |
# | Licensed under the BSD-3-Clause License.                          |
# +-------------------------------------------------------------------+

from __future__ import annotations

from contextlib import suppress
from copy import deepcopy
from functools import reduce
from typing import (
    MutableMapping,  # deprecate in favor of collections.abc.MutableMapping in Python 3.9+
)
from typing import TYPE_CHECKING, cast, overload, Any
from deprecated.sphinx import deprecated

if TYPE_CHECKING:  # pragma: no cover
    from typing import (
        Iterator,
        Iterable,
        ItemsView,
        KeysView,
        NamedTuple,
        TypedDict,
        ValuesView,
    )
    from _typeshed import SupportsKeysAndGetItem
    from typing_extensions import Self

    class FlatDictState(TypedDict):
        data: dict[Any, Any]
        delimiter: str


class FlatDict(MutableMapping[str, Any]):
    """
    A dictionary object that allows for single level, delimited key/value pair
    mapping of nested dictionaries.
    """

    _delimiter: str
    _flat_dict: dict[str, Any]
    _inflated_dict: dict[Any, Any] | None
    _meta_keys: tuple[str, ...] | None

    def __init__(
        self,
        value: dict[Any, Any] | NamedTuple | FlatDict | None = None,
        delimiter: str = ".",
    ):
        """
        Initialize a new FlatDict instance.

        :param value: The initial data to populate the FlatDict with. Can be a
                      nested dictionary, a NamedTuple, another FlatDict, or None.

        :param delimiter: The delimiter to use for the keys in the flat dictionary.

        :raises ValueError: if the delimiter is an empty string

        ---

        The default delimiter value is a period (``.``) but can be changed in the constructor
        or by calling :meth:`FlatDict.set_delimiter`.

        **WARNING**: keys containing the delimiter are not allowed and will raise a
        :exc:`ValueError` on assignment or when setting the delimiter.
        """
        super().__init__()

        if not delimiter:
            msg = "Delimiter cannot be an empty string"
            raise ValueError(msg)

        data = {}

        if isinstance(value, FlatDict):
            data = value.inflate()

        elif (
            isinstance(value, tuple)
            and hasattr(value, "_fields")
            and hasattr(value, "_asdict")
        ):
            data = value._asdict()

        elif value is not None:
            data = cast("dict[Any, Any]", value)

        if any(delimiter in key for key in data.keys()):
            data = FlatDict.unflatten(data, delimiter)

        self.__setstate__({"data": data, "delimiter": delimiter})

    @property
    def delimiter(self) -> str:
        """The key delimiter used for the flat dictionary."""
        return self._delimiter

    @delimiter.setter
    def delimiter(self, value: str) -> None:
        self.set_delimiter(value)

    @property
    def meta_keys(self) -> tuple[str, ...]:
        """The keys that exist as parent keys to nested dictionaries"""
        if self._meta_keys is None:
            self._meta_keys = self._get_meta_keys()
        return self._meta_keys

    @deprecated(
        reason="Use the 'inflate' method instead, will be removed in a future version",
        version="$NEW_VERSION",
    )
    def as_dict(self) -> dict[Any, Any]:
        return self.inflate()

    def clear(self):
        """Remove all items from the flat dictionary."""
        self._flat_dict.clear()
        self._meta_keys = None
        self._inflated_dict = None

    def copy(self) -> FlatDict:
        """Return a deep copy of the flat dictionary."""
        return self.__class__(deepcopy(self.inflate()), delimiter=self._delimiter)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieves the value for a delimited-key if key exists, otherwise returns the default.

        If default is not given, it defaults to ``None``, so this method never raises :exc:`KeyError`.

        :param key: The key name (with delimiters if necessary)
        :param default: The value to return if the key is not found
        """
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def inflate(self) -> dict[Any, Any]:
        """
        Inflates the flat dictionary into a nested dictionary structure.

        :returns: A nested dictionary representing the inflated structure of the flat dictionary
        """
        if self._inflated_dict is None:
            self._inflated_dict = self.unflatten(self._flat_dict, self.delimiter)
        return self._inflated_dict

    def items(self) -> ItemsView[str, Any]:
        """
        Return a view of the flat dictionary's items (key-value pairs).

        This viewer will automatically reflect any changes to the flat dictionary,
        including changes to the flat dictionary and any nested dictionaries that
        would affect the items.
        """
        return self._flat_dict.items()

    def keys(self) -> KeysView[str]:
        """
        Return a view of the flat dictionary's keys.

        This viewer will automatically reflect any changes to the flat dictionary,
        including changes to the flat dictionary and any nested dictionaries that
        would affect the keys.
        """
        return self._flat_dict.keys()

    def pop(self, key: str, default: Any = None) -> Any:
        """
        Remove the specified key and return the corresponding value.
        If the key is not found, return the default value.

        :param key: The delimited-key of the value to remove
        :param default: The value to return if the key is not found
        :returns: The value for the key if it exists, otherwise the default
        """
        if key not in self:
            return default

        value = self[key]
        self.__delitem__(key)
        return value

    def setdefault(self, key: str, default: Any = None) -> Any:
        """
        Safely retrieve a delimited-key value, or insert the default value if the key does not exist.

        :param key: The key name (with delimiters if necessary)
        :param default: The value to set and return if the key is not found
        :returns: The value for the key if it exists, otherwise the default
        """
        if key not in self:
            self.__setitem__(key, default)

        return self.__getitem__(key)

    def set_delimiter(self, delimiter: str) -> Self:
        """
        Set the key delimiter for the flat dictionary

        :param delimiter: The delimiter to use
        :raises ValueError: if the delimiter collides with an existing key
        """
        # Validates the new delimiter and converts existing cached flat dict
        new_flat_dict = self.flatten(self.inflate(), delimiter)
        self.clear()
        self._flat_dict.update(new_flat_dict)
        self._delimiter = delimiter
        return self

    @overload
    def update(self, arg: SupportsKeysAndGetItem[str, Any], /, **kwargs: Any) -> None:
        """
        Update the flat dictionary with new key/value pairs.

        :param arg: A mapping object with string keys and any type of values.
        :param kwargs: Additional key/value pairs to update the flat dictionary with.
        :returns: None
        """
        ...

    @overload
    def update(self, arg: Iterable[tuple[str, Any]], /, **kwargs: Any) -> None:
        """
        Update the flat dictionary with new key/value pairs.

        :param arg: An iterable of key/value tuple pairs.
        :param kwargs: Additional key/value pairs to update the flat dictionary with.
        :returns: None
        """
        ...

    @overload
    def update(self, /, **kwargs: Any) -> None:
        """
        Update the flat dictionary with the key/value pairs defined as kwargs.

        :param kwargs: Key/value pairs to update the flat dictionary with.
        :returns: None
        """
        ...

    def update(self, arg: Any = None, /, **kwargs: Any) -> None:
        """
        Update the flat dictionary with the key/value pairs from arg and kwargs.

        :param arg: The argument can be either a mapping or an iterable of key/value pairs.
        :param kwargs: Additional key/value pairs to update the flat dictionary with.
        :returns: None
        """
        params = {**kwargs}
        if arg is not None:
            if hasattr(arg, "keys") and hasattr(arg, "__getitem__"):
                params.update(
                    {
                        k: arg[k]
                        for k in cast("SupportsKeysAndGetItem[str, Any]", arg).keys()
                    }
                )
            else:
                params.update({k: v for k, v in arg})

        flattened_params = self.flatten(params, self.delimiter)

        if matching_meta_keys := flattened_params.keys() & set(self.meta_keys):
            for key in matching_meta_keys:
                self[key] = flattened_params[key]

        # only handle nested keys, top-level keys will be handled by the standard update
        differing_parent_keys: set[str] = reduce(
            lambda acc, key: self._reduce_to_parent_key(acc, key, self.delimiter),
            set(flattened_params.keys()) - set(self.keys()),
            set(),
        )

        while differing_parent_keys:
            for parent_key in differing_parent_keys:
                if parent_key in self._flat_dict:
                    # if the parent key exists but is not a dictionary, must remove the parent key
                    self._flat_dict.pop(parent_key)

            differing_parent_keys = reduce(
                lambda acc, key: self._reduce_to_parent_key(acc, key, self.delimiter),
                differing_parent_keys,
                set(),
            )

        new_flat_dict = {**self._flat_dict, **flattened_params}
        self.clear()
        self._flat_dict.update(new_flat_dict)

    def values(self) -> ValuesView[Any]:
        """
        Return a view of the flat dictionary's values.

        This viewer will automatically reflect any changes to the flat dictionary,
        including changes to the flat dictionary and any nested dictionaries that
        would affect the values.
        """
        return self._flat_dict.values()

    def __contains__(self, key: object) -> bool:
        return any((bool(key in self._flat_dict), bool(key in self.meta_keys)))

    def __delitem__(self, key: object) -> None:
        key_str = str(key)

        if key_str in self._flat_dict:
            del self._flat_dict[key_str]
            self._meta_keys = None
            self._inflated_dict = None
            return

        if key_str in self.meta_keys:
            pointer = inflated_dict = self.inflate()
            key_parts = key_str.split(self.delimiter)

            for k in key_parts[:-1]:
                pointer = pointer[k]

            del pointer[key_parts[-1]]

            new_flat_dict = self.flatten(inflated_dict, self.delimiter)
            self.clear()
            self._flat_dict.update(new_flat_dict)
            return

        msg = f"Key {key!r} not found in FlatDict"
        raise KeyError(msg)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, dict):
            return self.inflate() == other

        if isinstance(other, self.__class__):
            return all(
                (self.delimiter == other.delimiter, self._flat_dict == other._flat_dict)
            )

        msg = f"Comparison to incompatible type: {type(other).__name__!r}"
        raise TypeError(msg)

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __getitem__(self, key: object) -> Any:
        key_str = str(key)

        if key_str in self._flat_dict:
            return self._flat_dict[key_str]

        if key_str in self.meta_keys:
            inflated_dict = self.inflate()
            key_parts = key_str.split(self.delimiter)

            for part in key_parts[:-1]:
                inflated_dict = inflated_dict[part]

            return inflated_dict[key_parts[-1]]

        msg = f"Key {key!r} not found in FlatDict"
        raise KeyError(msg)

    def __iter__(self) -> Iterator[str]:
        return self._flat_dict.__iter__()

    def __len__(self) -> int:
        return len(self.keys())

    def __getstate__(self) -> FlatDictState:
        return {"data": self.inflate(), "delimiter": self.delimiter}

    def __setstate__(self, state: FlatDictState) -> None:
        self._delimiter = state["delimiter"]
        self._inflated_dict = None
        self._meta_keys = None

        if not hasattr(self, "_flat_dict"):
            self._flat_dict = {}

        self._flat_dict.clear()
        self._flat_dict.update(self.flatten(state["data"], self.delimiter))

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={id(self)} data={str(self)}>"

    def __setitem__(self, key: str, value: Any) -> None:
        pointer = inflated_dict = self.inflate()
        key_parts = key.split(self.delimiter)

        for k in key_parts[:-1]:
            if k not in pointer or not isinstance(pointer[k], dict):
                pointer[k] = {}
            pointer = pointer[k]

        pointer[key_parts[-1]] = value

        new_flat_dict = self.flatten(inflated_dict, self.delimiter)
        self.clear()
        self._flat_dict.update(new_flat_dict)

    def __str__(self) -> str:
        return f"{{{str.join(', ', [f'{k!r}: {self[k]!r}' for k in self.keys()])}}}"

    def _get_meta_keys(self) -> tuple[str, ...]:
        meta_keys: set[str] = set()
        parent_dict_keys: set[str] = reduce(
            lambda acc, key: self._reduce_to_parent_key(acc, key, self.delimiter),
            set(self.keys()),
            set(),
        )

        while parent_dict_keys:
            meta_keys |= parent_dict_keys

            parent_dict_keys = reduce(
                lambda acc, key: self._reduce_to_parent_key(acc, key, self.delimiter),
                parent_dict_keys,
                set(),
            )

        return tuple(sorted(meta_keys))

    @staticmethod
    def _reduce_to_parent_key(
        accumulator: set[str], key: str, delimiter: str
    ) -> set[str]:
        parent_key = str.join(delimiter, key.split(delimiter)[:-1])
        return accumulator | {parent_key} if parent_key else accumulator

    @staticmethod
    def flatten(value: dict[Any, Any] | FlatDict, delimiter: str) -> dict[str, Any]:
        """
        Flattens a nested dictionary into a single level dictionary with delimited keys.

        :param value: The nested dictionary or FlatDict to flatten
        :param delimiter: The delimiter to use for the keys in the flat dictionary
        :returns: A flat dictionary with delimited keys representing the nested structure of the input

        :raises ValueError: if the delimiter is an empty string or if any keys in the
                            input collide with the delimiter
        """
        if not delimiter:
            msg = "Delimiter cannot be an empty string"
            raise ValueError(msg)

        val = value.inflate() if isinstance(value, FlatDict) else (value or {})

        flat_dict = {}
        for k, v in val.items():
            if delimiter in k:
                msg = f"Key {k!r} collides with the delimiter {delimiter!r}"
                raise ValueError(msg)

            if not isinstance(v, dict):
                flat_dict[k] = v
                continue

            for sub_k, sub_v in FlatDict.flatten(v, delimiter).items():
                flat_dict[f"{k}{delimiter}{sub_k}"] = sub_v

        return flat_dict

    @staticmethod
    def unflatten(value: dict[str, Any], delimiter: str) -> dict[Any, Any]:
        """
        Inflates a flat dictionary with delimited keys into a nested dictionary.

        :param value: The flat dictionary to unflatten
        :param delimiter: The delimiter used in the flat dictionary keys
        :returns: A nested dictionary representing the inflated structure

        :raises ValueError: if the delimiter is an empty string
        """
        if not delimiter:
            msg = "Delimiter cannot be an empty string"
            raise ValueError(msg)

        inflated_dict: dict[Any, Any] = {}

        def convert_type(val: str) -> int | float | str:
            with suppress(ValueError):
                return int(val)

            with suppress(ValueError):
                return float(val)

            return val

        for k, v in value.items():
            current_key_str = k
            pointer = inflated_dict

            # Keep splitting the key until there are no more delimiters, building
            # out the nested dict structure as we go
            while len(key_parts := current_key_str.split(delimiter, maxsplit=1)) > 1:
                next_key = convert_type(key_parts[0])

                if next_key not in pointer:
                    pointer[next_key] = {}

                pointer = pointer[next_key]
                current_key_str = key_parts[-1]

            # No more delimiters in key, now we can assign the value to the final key
            pointer[convert_type(current_key_str)] = v

        return inflated_dict
