History
=======

1.3.0 (June 10th, 2024)
-----------------------

* Switch project to use ruff for formatting. (#42)

* Switch project to use pyproject for project configuration. (#43)

* Pin sentry-sdk support to ``sentry-sdk<2``. Fillmore 2.x will support
  ``sentry-sdk>2``, but it requires backwards incompatible changes. (#51)

* Add support for Django 5.0 (#53)

* Drop support for Django 3.2, 4.1, and 4.2 (#54)


1.2.0 (November 6th, 2023)
--------------------------

* Add support for Python 3.12 (#32)

* Add support for Django 4.2 (#33)


1.1.0 (April 5th, 2023)
-----------------------

* Switch from flake8 to ruff (#24)

* Add ``fillmore.test.diff_event`` utilify function for comparing a Sentry
  event with an expected structure accounting for ``unittest.mock.ANY``. (#23)


1.0.0 (November 8th, 2022)
--------------------------

* Add support for Python 3.11 (#18)

This feels stable and I'm using it in multiple production real-world projects,
so releasing a 1.0.0.


0.1.2 (August 1st, 2022)
------------------------

* Fix examples in documentation so they're linted and tested. Add notes about
  ``fillmore`` logging. Rewrite testing chapter to introduce Fillmore testing
  features in a less muddled way. (#15)


0.1.1 (July 25th, 2022)
-----------------------

* Fix scrubber where paths that were valid, but didn't point to something in an
  event erroneously kicked up a RulePathError. (#12)

* Fix test examples in docs.

* Fix examples in README. Thanks @stevejalim!


0.1.0 (June 23rd, 2022)
-----------------------

* Inital extraction and writing.
