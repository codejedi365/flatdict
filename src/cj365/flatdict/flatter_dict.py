"""
This module contains the implementation of the :class:`FlatterDict` class,
which provides a dictionary-like interface for working with nested dictionaries
using delimited keys but it is designed to handle lists and sets as child-dict
instances with the offset as the key.
"""
# +-------------------------------------------------------------------+
# | Module: cj365.flatdict.flatter_dict                               |
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
from typing import TYPE_CHECKING, cast, overload, Any, Sequence
from deprecated.sphinx import deprecated

from cj365.flatdict.flat_dict import FlatDict

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

    class FlatterDictState(TypedDict):
        data: Sequence[Any] | set[Any] | dict[Any, Any]
        delimiter: str
        root_type: type


# _COERCE = list, tuple, set, dict, FlatDict
_ARRAYS = list, set, tuple


class FlatterDict(MutableMapping[str, Any]):
    """
    A dictionary object that allows for single level, delimited key/value pair
    mapping of nested dictionaries, lists, or sets.
    """

    _delimiter: str
    _flat_dict: dict[str, Any]
    _inflated_obj: Sequence[Any] | set[Any] | dict[Any, Any] | None
    _meta_keys: tuple[str, ...] | None
    _root_type: type

    def __init__(
        self,
        value: Sequence[Any]
        | set[Any]
        | NamedTuple
        | dict[Any, Any]
        | FlatDict
        | FlatterDict
        | None = None,
        delimiter: str = ".",
    ):
        """
        Initialize a FlatterDict instance.

        :param value: The initial value for the flatter dictionary, can
                      be a nested structure of dicts, lists, sets, or tuples

        :param delimiter: The key delimiter to use for the flatter dictionary, defaults to "."

        :raises ValueError: if the delimiter is an empty string

        ---

        The default delimiter value is a period (``.``) but can be changed in the constructor
        or by calling :meth:`FlatterDict.set_delimiter`.

        **WARNING**: keys containing the delimiter will be treated as nested keys and
        will be inflated accordingly prior to assignment. This may lead to unexpected behavior,
        so make sure to choose a delimiter that does not collide with your keys.
        """
        super().__init__()

        if not delimiter:
            msg = "Delimiter cannot be an empty string"
            raise ValueError(msg)

        # Eliminates null
        val = value if value is not None else {}

        # If the value is already a FlatterDict or FlatDict, we can just inflate it to get the underlying data
        if isinstance(val, (FlatterDict, FlatDict)):
            val = val.inflate()

        if (  # isinstance check for NamedTuple
            isinstance(val, tuple)
            and hasattr(val, "_fields")
            and hasattr(val, "_asdict")
        ):
            val = cast("NamedTuple", val)._asdict()

        if isinstance(val, dict) and any(delimiter in key for key in val.keys()):
            val = FlatterDict.unflatten(val, delimiter)

        data: dict[Any, Any] = (
            self._convert_iterable_to_dict(val)
            if isinstance(val, (Sequence, set))
            else val
        )

        self.__setstate__(
            {"data": data, "delimiter": delimiter, "root_type": type(val)}
        )

    @property
    def delimiter(self) -> str:
        """The key delimiter used for the flat dictionary."""
        return self._delimiter

    @delimiter.setter
    def delimiter(self, value: str) -> None:
        self.set_delimiter(value)

    @property
    def meta_keys(self) -> tuple[str, ...]:
        """
        The keys that exist as parent keys to nested dictionaries or sequences
        and are not themselves present in the flat dictionary.
        """
        if self._meta_keys is None:
            self._meta_keys = self._get_meta_keys()
        return self._meta_keys

    @deprecated(
        reason="Use the 'inflate' method instead, 'as_dict()' will be removed in a future version",
        version="$NEW_VERSION",
    )
    def as_dict(self) -> Sequence[Any] | set[Any] | dict[Any, Any]:
        return self.inflate()

    def clear(self):
        """Remove all items from the flatter dictionary."""
        self._flat_dict.clear()
        self._meta_keys = None
        self._inflated_obj = None

    def copy(self) -> FlatterDict:
        """Return a deep copy of the flatter dictionary."""
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

    def inflate(self) -> Sequence[Any] | set[Any] | dict[Any, Any]:
        """
        Inflates the flatter dictionary into a nested data type structure.

        Any lists, sets, tuples, or dictionaries will be inflated as their respective types,
        with the keys of the flat dictionary used as indices for lists and sets and as keys for dictionaries.

        :returns: A nested data type representing the inflated structure of the flatter dictionary
        """
        if self._inflated_obj is None:
            self._inflated_obj = obj = self.unflatten(self._flat_dict, self.delimiter)

            if isinstance(obj, dict):
                if issubclass(self._root_type, dict):
                    return self._root_type(obj)

                elif issubclass(self._root_type, list):
                    # when FlatterDict is empty but initialized as a list
                    return list(obj.values())

                elif issubclass(self._root_type, set):
                    return set(obj.values())

                elif issubclass(self._root_type, tuple) and not hasattr(
                    self._root_type, "_asdict"
                ):
                    # when FlatterDict is empty but initialized as a tuple
                    return tuple(obj.values())

                # elif issubclass(self._root_type, tuple):  # NamedTuple
                #     return self._root_type(**obj)

            elif isinstance(obj, tuple):
                if issubclass(self._root_type, set):
                    return set(obj)

                elif issubclass(self._root_type, list):
                    return list(obj)

                elif issubclass(self._root_type, tuple):
                    return tuple(obj)

        return self._inflated_obj

    def items(self) -> ItemsView[str, Any]:
        """
        Return a view of the flatter dictionary's items (key-value pairs).

        This viewer will automatically reflect any changes to the flatter dictionary,
        including changes to the flatter dictionary and any nested data types that
        would affect the items.
        """
        return self._flat_dict.items()

    def keys(self) -> KeysView[str]:
        """
        Return a view of the flatter dictionary's keys.

        This viewer will automatically reflect any changes to the flatter dictionary,
        including changes to the flatter dictionary and any nested data types that
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
        Set the key delimiter for the flatter dictionary

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
        Update the flatter dictionary with new key/value pairs.

        :param arg: A mapping object with string keys and any type of values.
        :param kwargs: Additional key/value pairs to update the flatter dictionary with.
        :returns: None
        """
        ...

    @overload
    def update(self, arg: Iterable[tuple[str, Any]], /, **kwargs: Any) -> None:
        """
        Update the flatter dictionary with new key/value pairs.

        :param arg: An iterable of key/value tuple pairs.
        :param kwargs: Additional key/value pairs to update the flatter dictionary with.
        :returns: None
        """
        ...

    @overload
    def update(self, /, **kwargs: Any) -> None:
        """
        Update the flatter dictionary with the key/value pairs defined as kwargs.

        :param kwargs: Key/value pairs to update the flatter dictionary with.
        :returns: None
        """
        ...

    def update(self, arg: Any = None, /, **kwargs: Any) -> None:
        """
        Update the flatter dictionary with the key/value pairs from arg and kwargs.

        :param arg: The argument can be either a mapping or an iterable of key/value pairs.
        :param kwargs: Additional key/value pairs to update the flatter dictionary with.
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

        if not params:
            return

        if issubclass(self._root_type, (Sequence, set)) and any(
            k.isalpha() for k in params.keys()
        ):
            msg = "Cannot update a Set-initialized or Sequence-initialized FlatterDict with non-integer keys"
            raise ValueError(msg)

        flattened_params = self.flatten(params, self.delimiter)

        if matching_meta_keys := flattened_params.keys() & self.meta_keys:
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
        Return a view of the flatter dictionary's values.

        This viewer will automatically reflect any changes to the flatter dictionary,
        including changes to the flatter dictionary and any nested data types that
        would affect the values.
        """
        return self._flat_dict.values()

    def __contains__(self, key: object) -> bool:
        return any((bool(key in self._flat_dict), bool(key in self.meta_keys)))

    def __delitem__(self, key: object) -> None:
        key_str = str(key)

        if key_str not in self:
            err_msg = f"Key {key!r} not found in {self.__class__.__name__!r}"
            raise KeyError(err_msg)

        # Recursive function to modify the inflated object
        def delete_in_object(
            obj: Any, delimiter: str, key_name: str
        ) -> Sequence[Any] | set[Any] | dict[Any, Any]:
            key_parts = key_name.split(delimiter, 1)

            if isinstance(obj, Sequence) and not isinstance(obj, str):
                # GOAL: when the current object is a sequence, we want to delete the item at the
                # index specified by the current key part and then shift the remaining items down
                # to fill the gap.
                index = int(key_parts[0])

                # Rebuild the sequence skipping over the item at the index if the current key part
                # matches the index, otherwise recursively dig into the next level of nesting
                # Note: we wrap it in a list, so that it will unpack back into the correct position
                # or if its an empty list then it will unpack as nothing effectively deleting the
                # item at the index
                new_sequence = [
                    *obj[:index],
                    *(
                        []
                        if len(key_parts) == 1
                        else [delete_in_object(obj[index], delimiter, key_parts[1])]
                    ),
                    *obj[index + 1 :],
                ]

                if len(new_sequence) == 0:
                    # maintain type if the sequence is now empty after deletion
                    return type(obj)()

                # Convert the modified sequence to a dictionary with integer keys to maintain
                # the correct structure when flattened
                return {
                    str(k): v
                    for k, v in self._convert_iterable_to_dict(new_sequence).items()
                }

            elif not isinstance(obj, dict):
                err_msg = (
                    f"Cannot delete nested key on object of type {type(obj).__name__}"
                )
                raise KeyError(err_msg)

            if len(key_parts) == 1:
                del obj[key_name]
                return obj

            # Dig into the next level of nesting to find the key to delete, then bubble back up the
            # modified object structure to be flattened and set as the new flat dictionary
            next_key, remaining_key = key_parts
            obj[next_key] = delete_in_object(obj[next_key], delimiter, remaining_key)
            return obj

        # Recursively modify the inflated object with the new value,
        # then flatten the modified object to create the new flat dictionary
        new_flat_dict = self.flatten(
            delete_in_object(self.inflate(), self.delimiter, key_str),
            self.delimiter,
        )

        # reset & update the flat dictionary (maintains KeyView, ItemsView, ValuesView references)
        self.clear()
        self._flat_dict.update(new_flat_dict)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, dict):
            return self.inflate() == other

        if isinstance(other, Sequence) and not isinstance(other, str):
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
            inflated_obj = self.inflate()

            def get_value_from_key_in_inflated(
                inflated: Sequence[Any] | set[Any] | dict[Any, Any],
                key_parts: list[str],
            ) -> Any:
                msg = (
                    "Cannot access nested keys of type {}, attempted to access {} in {}"
                )
                for part in key_parts:
                    if isinstance(inflated, dict):
                        inflated = inflated[part]
                        continue

                    if isinstance(inflated, Sequence) and not isinstance(inflated, str):
                        inflated = inflated[int(part)]
                        continue

                    msg = msg.format(
                        repr(type(inflated).__name__),
                        repr(key_str),
                        repr(self.__class__.__name__),
                    )
                    raise KeyError(msg)
                return inflated

            return get_value_from_key_in_inflated(
                inflated_obj, key_str.split(self.delimiter)
            )

        msg = f"Key {key!r} not found in {self.__class__.__name__!r}"
        raise KeyError(msg)

    def __iter__(self) -> Iterator[str]:
        return self._flat_dict.__iter__()

    def __len__(self) -> int:
        return len(self.keys())

    def __getstate__(self) -> FlatterDictState:
        return {
            "data": self.inflate(),
            "delimiter": self.delimiter,
            "root_type": self._root_type,
        }

    def __setstate__(self, state: FlatterDictState) -> None:
        self._delimiter = state["delimiter"]
        self._inflated_obj = None
        self._meta_keys = None
        self._root_type = state["root_type"]

        if not hasattr(self, "_flat_dict"):
            self._flat_dict = {}

        self._flat_dict.clear()
        self._flat_dict.update(self.flatten(state["data"], self.delimiter))

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={id(self)} data={str(self)}>"

    def __setitem__(self, key: str, value: Any) -> None:
        val = value

        if isinstance(val, (FlatDict, FlatterDict)):
            val = val.inflate()

        if isinstance(val, dict):
            val = self.flatten(val, self.delimiter)

        if isinstance(val, (Sequence, set)) and not isinstance(val, str):
            if len(val) > 0:
                val = self.flatten(val, self.delimiter)

        if key in self._flat_dict:
            if not isinstance(val, dict):
                self._flat_dict[key] = val
                self._inflated_obj = None
                return

            self._flat_dict.pop(key)
            new_flat_dict = {
                **self._flat_dict,
                **{f"{key}{self.delimiter}{k}": v for k, v in val.items()},
            }
            self.clear()
            self._flat_dict.update(new_flat_dict)
            return

        def modify_object(
            obj: Any, delimiter: str, key_name: str, replacement_value: Any
        ) -> Sequence[Any] | set[Any] | dict[Any, Any]:
            key_parts = key_name.split(delimiter, 1)

            if isinstance(obj, Sequence) and not isinstance(obj, str):
                if not key_parts[0].isdigit():
                    err_msg = f"Cannot set key on sequence with non-integer key {key_parts[0]!r}"
                    raise KeyError(err_msg)

                # if the next key is beyond the end of the existing sequence, we need to extend the sequence
                # with None values to allow for the new key to be set at the correct index
                obj = [*obj, *[None for _ in range(int(key_parts[0]) - len(obj))]]

                # convert the sequence to a dictionary with integer keys for the next level of nesting
                # Since we extended the sequence above, when inflated it will turn back into a sequence
                obj = {
                    str(k): v for k, v in self._convert_iterable_to_dict(obj).items()
                }

            elif not isinstance(obj, dict):
                err_msg = (
                    f"Cannot set nested key on object of type {type(obj).__name__}"
                )
                raise KeyError(err_msg)

            if len(key_parts) == 1:
                obj[key_name] = replacement_value
                return obj

            next_key, remaining_key = key_parts

            if (
                next_key not in obj
                or not isinstance(obj[next_key], (dict, Sequence))
                or isinstance(obj[next_key], str)
            ):
                obj[next_key] = {}

            obj[next_key] = modify_object(
                obj[next_key], delimiter, remaining_key, replacement_value
            )
            return obj

        # Recursively modify the inflated object with the new value,
        # then flatten the modified object to create the new flat dictionary
        new_flat_dict = self.flatten(
            modify_object(self.inflate(), self.delimiter, key, val),
            self.delimiter,
        )

        # reset & update the flat dictionary (maintains KeyView, ItemsView, ValuesView references)
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
    def _convert_iterable_to_dict(value: Sequence[Any] | set[Any]) -> dict[int, Any]:
        return {i: v for i, v in enumerate(value)}

    @staticmethod
    def _reduce_to_parent_key(
        accumulator: set[str], key: str, delimiter: str
    ) -> set[str]:
        parent_key = str.join(delimiter, key.split(delimiter)[:-1])
        return accumulator | {parent_key} if parent_key else accumulator

    @staticmethod
    def flatten(
        value: Sequence[Any] | set[Any] | dict[Any, Any] | FlatDict | FlatterDict,
        delimiter: str,
    ) -> dict[str, Any]:
        """
        Flattens a nested data type structure into a flatter dictionary with delimited keys.

        :param value: The nested data structure to flatten, can be a dictionary or a FlatDict
        :param delimiter: The delimiter to use for the keys in the flatter dictionary
        :returns: A flat dictionary with delimited keys representing the nested structure

        :raises ValueError: if the delimiter is an empty string or if any keys in the nested
                            structure collide with the delimiter
        """
        if not delimiter:
            msg = "Delimiter cannot be an empty string"
            raise ValueError(msg)

        val = value.inflate() if isinstance(value, (FlatDict, FlatterDict)) else value

        data = (
            FlatterDict._convert_iterable_to_dict(val)
            if isinstance(val, (Sequence, set))
            else val
        )

        flat_dict: dict[str, Any] = {}

        for k, v in data.items():
            key_str = str(k)

            if delimiter in key_str:
                msg = f"Key {k!r} collides with the delimiter {delimiter!r}"
                raise ValueError(msg)

            if isinstance(v, (FlatDict, FlatterDict)):
                v = v.inflate()

            if isinstance(v, (Sequence, set)) and not isinstance(v, str):
                if not v:
                    # maintain type if an empty sequence or set
                    flat_dict[key_str] = v
                    continue

                # sets are unordered, so we need to convert to a sorted list first to ensure consistent ordering in the flat dict keys
                v = sorted(v) if isinstance(v, set) else v
                v = FlatterDict._convert_iterable_to_dict(v)

            if not isinstance(v, dict) or not v:
                flat_dict[key_str] = v
                continue

            for sub_k, sub_v in FlatterDict.flatten(v, delimiter).items():
                flat_dict[f"{key_str}{delimiter}{sub_k}"] = sub_v

        return flat_dict

    @staticmethod
    def unflatten(
        value: dict[str, Any], delimiter: str
    ) -> Sequence[Any] | set[Any] | dict[Any, Any]:
        """
        Inflates a flatter dictionary into a nested data type structure.

        :param value: The flat dictionary to unflatten
        :param delimiter: The delimiter used in the flatter dictionary keys
        :returns: A nested data type representing the inflated structure of the flatter dictionary

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

        # Convert any dictionaries with contiguous integer keys starting from 0 into tuples
        def convert_dicts_to_tuples(
            obj: Any,
        ) -> Sequence[Any] | set[Any] | dict[Any, Any]:
            if not isinstance(obj, dict) or len(obj) == 0:
                return obj

            if all(isinstance(k, int) and k >= 0 for k in obj.keys()) and set(
                obj.keys()
            ) == set(range(len(obj))):
                return tuple(convert_dicts_to_tuples(v) for _, v in sorted(obj.items()))

            # recursively convert any nested dictionaries that are sequences
            return {k: convert_dicts_to_tuples(v) for k, v in obj.items()}

        return convert_dicts_to_tuples(inflated_dict)
