.. _changelog:

=========
CHANGELOG
=========

.. _changelog-v5.0.1:

v5.0.1 (2026-02-22)
===================

🪲 Bug Fixes
------------

* **FlatDict**: Enable ``update()`` from another FlatDict object (`PR#2`_, `ac6d9fe`_)

* **FlatterDict**: Enable ``update()`` from another FlatterDict or FlatDict object (`PR#3`_,
  `936cfbd`_)

📖 Documentation
----------------

* **api**: Adjust table-of-contents layout for classes (`de313fb`_)

⚙️ Build System
----------------

* **deps**: Specify ``typing_extensions`` package in range from ``v4.13`` to ``< v5.0`` (`44ae99e`_)

.. _44ae99e: https://github.com/codejedi365/flatdict/commit/44ae99ebd2613cef64914b47af10acb68d464c70
.. _936cfbd: https://github.com/codejedi365/flatdict/commit/936cfbd5cd6c4618fdbc96069a870dec56ededc9
.. _ac6d9fe: https://github.com/codejedi365/flatdict/commit/ac6d9fef01a0b1a4b0f0422f81aa0d6935d78ab8
.. _de313fb: https://github.com/codejedi365/flatdict/commit/de313fbd70c364595b5eb50510c88abe57989b36
.. _PR#2: https://github.com/codejedi365/flatdict/pull/2
.. _PR#3: https://github.com/codejedi365/flatdict/pull/3


.. _changelog-v5.0.0:

v5.0.0 (2026-02-22)
===================

✨ Features
-----------

* **FlatDict**: Add constructor flexibility for passing a NamedTuple (`2512a57`_)

* **typing**: Add typing flag to package (`8556507`_)

⚡ Performance Improvements
---------------------------

* **FlatDict**: Optimize ``FlatDict`` implementation (`5ba90d0`_)

* **FlatterDict**: Optimize ``FlatterDict`` implementation (`a63449c`_)

📖 Documentation
----------------

* Refactor & enhance documentation (`3f58958`_)

♻️ Refactoring
---------------

* **FlatDict**: Change default delimiter to a period (`8f29aaf`_)

* **FlatterDict**: Change default delimiter to a period (`bdc84da`_)

💥 Breaking Changes
-------------------

* **FlatDict**: The default delimiter has been changed to a period (`.`) instead of a colon (`:`).
  This is a stylistic change but it will impact users whom did not define a delimiter parameter in
  the ``FlatDict`` constructor and expect it to be a colon. If you do not desire this change, update
  your constructor to specify a colon as the delimiter for the ``FlatDict``. Example:
  ``FlatDict(..., delimiter=":")``.

* **FlatterDict**: The default delimiter has been changed to a period (`.`) instead of a colon
  (`:`). This is a stylistic change but it will impact users whom did not define a delimiter
  parameter in the ``FlatterDict`` constructor and expect it to be a colon. If you do not desire
  this change, update your constructor to specify a colon as the delimiter for the ``FlatterDict``.
  Example: ``FlatterDict(..., delimiter=":")``.

.. _2512a57: https://github.com/codejedi365/flatdict/commit/2512a579f3b4484be270f7993a6826a259d0051c
.. _3f58958: https://github.com/codejedi365/flatdict/commit/3f58958228f4261d0d63c738a60162e8b3dc7882
.. _5ba90d0: https://github.com/codejedi365/flatdict/commit/5ba90d0703733d0454469ac0d4368069e5f78e6b
.. _8556507: https://github.com/codejedi365/flatdict/commit/855650782cf91d438b9d044db7fa6d396217400c
.. _8f29aaf: https://github.com/codejedi365/flatdict/commit/8f29aaf5980fdbfbcd4c1f6f5792dee743141a6a
.. _a63449c: https://github.com/codejedi365/flatdict/commit/a63449c36cc07067019e8e8b2fe62ace15783b14
.. _bdc84da: https://github.com/codejedi365/flatdict/commit/bdc84da0d6ffce8aec5308acc3293c8cd3d797d2


.. _changelog-v4.0.4:

v4.0.4 (2024-08-28)
===================

🪲 Bug Fixes
------------

- move to main branch and update release (`PR#10`_)

- fix for versions and deploy trigger (`PR#11`_)

- update to use deploy key (`PR#12`_)

.. _PR#10: https://github.com/dennishenry/flatdict/pull/10
.. _PR#11: https://github.com/dennishenry/flatdict/pull/11
.. _PR#12: https://github.com/dennishenry/flatdict/pull/12


.. _changelog-v4.0.3:

v4.0.3 (2024-08-28)
===================

🪲 Bug Fixes
------------

- update deployment (`PR#03`_)

- updating workflow (`PR#04`_)

- move to new pypi publish (`PR#05`_)

- updating configurations (`PR#06`_)

- updating project name (`PR#07`_)

- updating module name (`PR#08`_)

- final changes for 4.0.3 (`PR#09`_)

.. _PR#03: https://github.com/dennishenry/flatdict/pull/3
.. _PR#04: https://github.com/dennishenry/flatdict/pull/4
.. _PR#05: https://github.com/dennishenry/flatdict/pull/5
.. _PR#06: https://github.com/dennishenry/flatdict/pull/6
.. _PR#07: https://github.com/dennishenry/flatdict/pull/7
.. _PR#08: https://github.com/dennishenry/flatdict/pull/8
.. _PR#09: https://github.com/dennishenry/flatdict/pull/9


.. _changelog-v4.0.2:

v4.0.2 (2024-08-28)
===================

🪲 Bug Fixes
------------

- Fixes for building wheel


.. _changelog-v4.0.1:

v4.0.1 (2020-02-13)
===================

🪲 Bug Fixes
------------

- Gracefully fail to install if setuptools is too old


.. _changelog-v4.0.0:

v4.0.0 (2020-02-12)
===================

- FIXED deprecation warning from Python 3.9 (`PR#40`_)

- FIXED keep order of received dict and it's nested objects (`PR#38`_)

- Removes compatibility with Python 2.7 and Python 3.4

.. _PR#38: https://github.com/gmr/flatdict/pull/38
.. _PR#40: https://github.com/gmr/flatdict/pull/40


.. _changelog-v3.4.0:

v3.4.0 (2019-07-24)
===================

- FIXED sort order with regard to a nested list of dictionaries (`PR#33`_)

.. _PR#33: https://github.com/gmr/flatdict/pull/33


.. _changelog-3.3.0:

v3.3.0 (2019-07-17)
===================

- FIXED ``FlatDict.setdefault()`` to match dict behavior (`PR#32`_)

- FIXED empty nested Flatterdict (`PR#30`_)

- CHANGED functionality to allow setting and updating nests within iterables (`PR#29`_)

.. _PR#29: https://github.com/gmr/flatdict/pull/29
.. _PR#30: https://github.com/gmr/flatdict/pull/30
.. _PR#32: https://github.com/gmr/flatdict/pull/32


.. _changelog-3.2.1:

v3.2.1 (2019-06-10)
===================

- FIXED docs generation for readthedocs.io


.. _changelog-3.2.0:

v3.2.0 (2019-06-10)
===================

- FIXED List Flattening does not return list when an odd number of depth in the dictionary (`PR#27`_)

- CHANGED FlatterDict to allow for deeply nested dicts and lists when invoking ``FlatterDict.as_dict()`` (`PR#28`_)

- Flake8 cleanup/improvements

- Distribution/packaging updates to put metadata into setup.cfg

.. _PR#27: https://github.com/gmr/flatdict/pull/27
.. _PR#28: https://github.com/gmr/flatdict/pull/28


.. _changelog-3.1.0:

v3.1.0 (2018-10-30)
===================

- FIXED ``FlatDict`` behavior with empty iteratable values

- CHANGED behavior when casting to str or repr (`PR#23`_)

.. _PR#23: https://github.com/gmr/flatdict/pull/23


.. _changelog-3.0.1:

v3.0.1 (2018-07-01)
===================

- Add 3.7 to Trove Classifiers

- Add Python 2.7 unicode string compatibility (`PR#22`_)

.. _PR#22: https://github.com/gmr/flatdict/pull/22


.. _changelog-v3.0.0:

v3.0.0 (2018-03-06)
===================

- CHANGED ``FlatDict.as_dict`` to return the nested data structure based upon delimiters, coercing ``FlatDict`` objects to ``dict``.

- CHANGED ``FlatDict`` to extend ``collections.MutableMapping`` instead of dict

- CHANGED ``dict(FlatDict())`` to return a shallow ``dict`` instance with the delimited keys as strings

- CHANGED ``FlatDict.__eq__`` to only evaluate against dict or the same class

- FIXED ``FlatterDict`` behavior to match expectations from pre-2.0 releases.


.. _changelog-2.0.1:

v2.0.1 (2018-01-18)
===================

- FIXED metadata for pypi upload


.. _changelog-2.0.0:

v2.0.0 (2018-01-18)
===================

- Code efficiency refactoring and cleanup

- Rewrote a majority of the tests, now at 100% coverage

- ADDED ``FlatDict.__eq__`` and ``FlatDict.__ne__`` (`PR#13`_)

- ADDED ``FlatterDict`` class that performs the list, set, and tuple coercion that was added in v1.20

- REMOVED coercion of lists and tuples from ``FlatDict`` that was added in 1.2.0.

- REMOVED ``FlatDict.has_key()`` as it duplicates of ``FlatDict.__contains__``

- ADDED Python 3.5 and 3.6 to support matrix

- REMOVED support for Python 2.6 and Python 3.2, 3.3

- CHANGED ``FlatDict.set_delimiter`` to raise a ``ValueError`` if a key already exists with the delimiter value in it. (`PR#8`_)

.. _PR#8: https://github.com/gmr/flatdict/pull/8
.. _PR#13: https://github.com/gmr/flatdict/pull/13


.. _changelog-v1.2.0:

v1.2.0 (2015-06-25)
===================

- ADDED Support lists and tuples as well as dicts. (`PR#4`_)

.. _PR#4: https://github.com/gmr/flatdict/pull/4


.. _changelog-1.1.3:

v1.1.3 (2015-01-04)
===================

- ADDED Python wheel support


.. _changelog-1.1.2:

v1.1.2 (2013-10-09)
===================

- Documentation and CI updates

- CHANGED use of ``dict()`` to a dict literal ``{}``


.. _changelog-1.1.1:

v1.1.1 (2012-08-17)
===================

- ADDED ``FlatDict.as_dict()``

- ADDED Python 3 support

- ADDED ``FlatDict.set_delimiter()``

- Bugfixes and improvements from `naiquevin <https://github.com/naiquevin>`_


.. _changelog-1.1.0:

v1.1.0 (2012-08-17)
===================

- ADDED ``FlatDict.as_dict()``


.. _changelog-1.0.0:

v1.0.0 (2012-08-10)
===================

- Initial release
