# -*- coding: utf-8 -*-

"""Command line interface for :mod:`front_end`.

Why does this file exist, and why not put this in ``__main__``? You might be tempted to import things from ``__main__``
later, but that will cause problems--the code will get executed twice:

- When you run ``python3 -m front_end`` python will execute``__main__.py`` as a script.
  That means there won't be any ``front_end.__main__`` in ``sys.modules``.
- When you import __main__ it will get executed again (as a module) because
  there's no ``front_end.__main__`` in ``sys.modules``.

.. seealso:: https://click.palletsprojects.com/en/7.x/setuptools/#setuptools-integration
"""

import logging
import click
from simulator.front_end.src.front_end.region_creation.input_streams import read_file

__all__ = [
    "main",
]

logger = logging.getLogger(__name__)


@click.group()
@click.version_option()
def main():
    """CLI for front_end."""


if __name__ == "__main__":
    main()



