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
import os
import click


__all__ = [
    "main",
]

from front_end.grpc.client import hash_file_demo
from front_end.grpc.hello_world_demo.greeter_server import serve
from front_end.hash_files.get_hash_files import download_files

logger = logging.getLogger(__name__)


@click.command()
@click.version_option()
@click.option('--demo', 'demo', flag_value=True)
@click.option('--hello_world', 'hello_world', flag_value=True)
def main(demo, hello_world):
    """CLI for front_end."""
    if demo:
        os.environ['SIMULATOR_MODE'] = 'DEMO'
        os.environ['SERVER_IP'] = 'localhost'
    if hello_world:
        os.environ['SIMULATOR_MODE'] = 'HELLO'
        os.environ['SERVER_IP'] = 'localhost'

    if os.environ['SIMULATOR_MODE'] == 'HELLO':
        print(f"Hello Server running on front_end.")
        serve()
    elif os.environ['SIMULATOR_MODE'] == 'DEMO':
        print(f"Demo Client running on front_end.")
        download_files("https://tracer.filesystems.org/traces/fslhomes/2011-8kb-only/", limit=1)
        serve()
        hash_file_demo("./hash_files/fslhomes-user006-2011-09-10.8kb.hash.anon")
    else:
        print("No front_end demo :(")


if __name__ == "__main__":
    main()



