# -*- coding: utf-8 -*-

"""Command line interface for :mod:`back_end`.

Why does this file exist, and why not put this in ``__main__``? You might be tempted to import things from ``__main__``
later, but that will cause problems--the code will get executed twice:

- When you run ``python3 -m back_end`` python will execute``__main__.py`` as a script.
  That means there won't be any ``back_end.__main__`` in ``sys.modules``.
- When you import __main__ it will get executed again (as a module) because
  there's no ``back_end.__main__`` in ``sys.modules``.

.. seealso:: https://click.palletsprojects.com/en/7.x/setuptools/#setuptools-integration
"""

import logging
import os

import click
from .grpc.greeter_server import serve

__all__ = [
  "main",
]

logger = logging.getLogger(__name__)


@click.command()
@click.version_option()
@click.option('--demo', 'demo', flag_value=True)
@click.argument('first_arg')
def main(demo, first_arg):
    """CLI for back_end."""
    if demo or os.environ['SIMULATOR_MODE'] == 'DEMO':
        print(f"Server running. First Arg Value: {first_arg}")
        serve()
    else:
        print("No back_end demo :(")


if __name__ == "__main__":
    main()
