"""FlatDict is a dict object that allows for single level, delimited
key/value pair mapping of nested dictionaries.

"""
import sys

from cj365.flatdict.flat_dict import FlatDict


class FlatterDict(FlatDict):
    """Like :class:`~flatdict2.FlatDict` but also coerces lists and sets
     to child-dict instances with the offset as the key. Alternative to
     the implementation added in v1.2 of FlatDict.

    """
    _COERCE = list, tuple, set, dict, FlatDict
    _ARRAYS = list, set, tuple

    def __init__(self, value=None, delimiter=':', dict_class=dict):
        self.original_type = type(value)
        if self.original_type in self._ARRAYS:
            value = {str(i): v for i, v in enumerate(value)}
        super(FlatterDict, self).__init__(value, delimiter, dict_class)

    def __setitem__(self, key, value):
        """Assign the value to the key, dynamically building nested
        FlatDict items where appropriate.

        :param mixed key: The key for the item
        :param mixed value: The value for the item
        :raises: TypeError

        """
        if isinstance(value, self._COERCE) and \
                not isinstance(value, FlatterDict):
            value = self.__class__(value, self._delimiter)
        if self._has_delimiter(key):
            pk, ck = key.split(self._delimiter, 1)
            if pk not in self._values:
                self._values[pk] = self.__class__({ck: value}, self._delimiter)
                return
            if getattr(self._values[pk], 'original_type',
                       None) in self._ARRAYS:
                try:
                    k, cck = ck.split(self._delimiter, 1)
                    int(k)
                except ValueError:
                    raise TypeError(
                        'Assignment to invalid type for key {}{}{}'.format(
                            pk, self._delimiter, ck))
                self._values[pk][k][cck] = value
                return
            elif not isinstance(self._values[pk], FlatterDict):
                raise TypeError(
                    'Assignment to invalid type for key {}'.format(pk))
            self._values[pk][ck] = value
        else:
            self._values[key] = value

    def as_dict(self):
        """Return the :class:`~flatdict2.FlatterDict` as a nested
        :class:`dict`.

        :rtype: dict

        """
        out = {}
        for key in self.keys():
            if self._has_delimiter(key):
                pk, ck = key.split(self._delimiter, 1)
                if self._has_delimiter(ck):
                    ck = ck.split(self._delimiter, 1)[0]
                if isinstance(self._values[pk], FlatterDict) and pk not in out:
                    if self._values[pk].original_type == tuple:
                        out[pk] = tuple(self._child_as_list(pk))
                    elif self._values[pk].original_type == list:
                        out[pk] = self._child_as_list(pk)
                    elif self._values[pk].original_type == set:
                        out[pk] = set(self._child_as_list(pk))
                    elif self._values[pk].original_type == dict:
                        out[pk] = self._values[pk].as_dict()
            else:
                if isinstance(self._values[key], FlatterDict):
                    out[key] = self._values[key].original_type()
                else:
                    out[key] = self._values[key]
        return out

    def _child_as_list(self, pk, ck=None):
        """Returns a list of values from the child FlatterDict instance
        with string based integer keys.

        :param str pk: The parent key
        :param str ck: The child key, optional
        :rtype: list

        """
        if ck is None:
            subset = self._values[pk]
        else:
            subset = self._values[pk][ck]
        # Check if keys has delimiter, which implies deeply nested dict
        keys = subset.keys()
        if any(self._has_delimiter(k) for k in keys):
            out = []
            split_keys = {k.split(self._delimiter)[0] for k in keys}
            for k in sorted(split_keys, key=lambda x: int(x)):
                if subset[k].original_type == tuple:
                    out.append(tuple(self._child_as_list(pk, k)))
                elif subset[k].original_type == list:
                    out.append(self._child_as_list(pk, k))
                elif subset[k].original_type == set:
                    out.append(set(self._child_as_list(pk, k)))
                elif subset[k].original_type == dict:
                    out.append(subset[k].as_dict())
            return out

        # Python prior 3.6 does not guarantee insertion order, remove it after
        # EOL python 3.5 - 2020-09-13
        if sys.version_info[0:2] < (3, 6):  # pragma: nocover
            return [subset[k] for k in sorted(keys, key=lambda x: int(x))]
        else:
            return [subset[k] for k in keys]
