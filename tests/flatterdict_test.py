"""
Unittests for flatdict2.FlatDict

"""
import flatdict2

from tests.flatdict_test import FlatDictTests


class FlatterDictTests(FlatDictTests):

    TEST_CLASS = flatdict2.FlatterDict

    FLAT_EXPECTATION = {
        'foo:bar:baz': 0,
        'foo:bar:qux': 1,
        'foo:bar:corge': 2,
        'foo:bar:list:0': -1,
        'foo:bar:list:1': -2,
        'foo:bar:list:2': -3,
        'foo:grault:baz': 3,
        'foo:grault:qux': 4,
        'foo:grault:corge': 5,
        'foo:list:0': 'F',
        'foo:list:1': 'O',
        'foo:list:2': 'O',
        'foo:list:3': '',
        'foo:list:4': 'B',
        'foo:list:5': 'A',
        'foo:list:6': 'R',
        'foo:list:7': '',
        'foo:list:8': 'L',
        'foo:list:9': 'I',
        'foo:list:10': 'S',
        'foo:list:11': 'T',
        'foo:set:0': 10,
        'foo:set:1': 20,
        'foo:set:2': 30,
        'foo:tuple:0': 'F',
        'foo:tuple:1': 0,
        'foo:tuple:2': 0,
        'foo:abc:def': True,
        'garply:foo': 0,
        'garply:bar': 1,
        'garply:baz': 2,
        'garply:qux:corge': 3,
        'fred': 4,
        'xyzzy': 'plugh',
        'thud': 5,
        'waldo:fred': 6,
        'waldo:wanda': 7,
        'neighbors:0:left': 'john',
        'neighbors:0:right': 'michelle',
        'neighbors:1:left': 'steven',
        'neighbors:1:right': 'wynona',
        'double_nest:0:0': 1,
        'double_nest:0:1': 2,
        'double_nest:1:0': 3,
        'double_nest:1:1': 4,
        'double_nest:2:0': 5,
        'double_nest:2:1': 6,
    }

    KEYS = [
        'foo:bar:baz',
        'foo:bar:qux',
        'foo:bar:corge',
        'foo:bar:list:0',
        'foo:bar:list:1',
        'foo:bar:list:2',
        'foo:grault:baz',
        'foo:grault:qux',
        'foo:grault:corge',
        'foo:list:0',
        'foo:list:1',
        'foo:list:2',
        'foo:list:3',
        'foo:list:4',
        'foo:list:5',
        'foo:list:6',
        'foo:list:7',
        'foo:list:8',
        'foo:list:9',
        'foo:list:10',
        'foo:list:11',
        'foo:set:0',
        'foo:set:1',
        'foo:set:2',
        'foo:tuple:0',
        'foo:tuple:1',
        'foo:tuple:2',
        'foo:abc:def',
        'garply:foo',
        'garply:bar',
        'garply:baz',
        'garply:qux:corge',
        'fred',
        'xyzzy',
        'thud',
        'waldo:fred',
        'waldo:wanda',
        'neighbors:0:left',
        'neighbors:0:right',
        'neighbors:1:left',
        'neighbors:1:right',
        'double_nest:0:0',
        'double_nest:0:1',
        'double_nest:1:0',
        'double_nest:1:1',
        'double_nest:2:0',
        'double_nest:2:1',
    ]

    VALUES = {
        'foo': {
            'bar': {
                'baz': 0,
                'qux': 1,
                'corge': 2,
                'list': [-1, -2, -3]
            },
            'grault': {
                'baz': 3,
                'qux': 4,
                'corge': 5
            },
            'list': ['F', 'O', 'O', '', 'B', 'A', 'R', '', 'L', 'I', 'S', 'T'],
            'set': {10, 20, 30},
            'tuple': ('F', 0, 0),
            'abc': {
                'def': True
            }
        },
        'garply': {
            'foo': 0,
            'bar': 1,
            'baz': 2,
            'qux': {
                'corge': 3
            }
        },
        'fred': 4,
        'xyzzy': 'plugh',
        'thud': 5,
        'waldo:fred': 6,
        'waldo:wanda': 7,
        'neighbors': [{
            'left': 'john',
            'right': 'michelle'
        }, {
            'left': 'steven',
            'right': 'wynona'
        }],
        'double_nest': [
            [1, 2],
            (3, 4),
            {5, 6},
        ]
    }

    AS_DICT = {
        'foo': {
            'bar': {
                'baz': 0,
                'qux': 1,
                'corge': 2,
                'list': [-1, -2, -3]
            },
            'grault': {
                'baz': 3,
                'qux': 4,
                'corge': 5
            },
            'list': ['F', 'O', 'O', '', 'B', 'A', 'R', '', 'L', 'I', 'S', 'T'],
            'set': {10, 20, 30},
            'tuple': ('F', 0, 0),
            'abc': {
                'def': True
            }
        },
        'garply': {
            'foo': 0,
            'bar': 1,
            'baz': 2,
            'qux': {
                'corge': 3
            }
        },
        'fred':
        4,
        'xyzzy':
        'plugh',
        'thud':
        5,
        'waldo': {
            'fred': 6,
            'wanda': 7
        },
        'neighbors': [{
            'left': 'john',
            'right': 'michelle'
        }, {
            'left': 'steven',
            'right': 'wynona'
        }],
        'double_nest': [
            [1, 2],
            (3, 4),
            {5, 6},
        ]
    }

    def test_set_item(self):
        vals = {'double_nest': [[1, 2], [3, 4]]}
        d = self.TEST_CLASS(vals)
        new_vals = {'double_nest': [[-1, 2], [3, 4]]}
        d['double_nest:0:0'] = -1
        self.assertEqual(d.as_dict(), new_vals)

    def test_update_nest(self):
        vals = {'double_nest': [[1, 2], [3, 4]]}
        d = self.TEST_CLASS(vals)
        new_vals = {'double_nest': [[-1, 2], [3, 4]]}
        d.update(new_vals)
        self.assertEqual(d.as_dict(), new_vals)

    def test_set_nest_dict(self):
        vals = {'dicts': [{'a': 1, 'b': 2}, {'c': 3, 'd': 4}]}
        d = self.TEST_CLASS(vals)
        vals['dicts'][0]['a'] = -1
        d['dicts:0:a'] = -1
        self.assertEqual(d.as_dict(), vals)

    def test_update_nest_dict(self):
        vals = {'dicts': [{'a': 1, 'b': 2}, {'c': 3, 'd': 4}]}
        d = self.TEST_CLASS(vals)
        vals['dicts'][0]['a'] = -1
        d.update(vals)
        self.assertEqual(d.as_dict(), vals)
