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

from front_end.grpc.hello_world_demo.greeter_server import serve
from front_end.simulate import Simulator

logger = logging.getLogger(__name__)


@click.command()
@click.version_option()
@click.option('--hello_world', 'hello_world', flag_value=True)
@click.option('--run', 'run', flag_value=True)
def main(hello_world, run):
    """CLI for front_end."""
    if hello_world:
        os.environ['SIMULATOR_MODE'] = 'HELLO'
    if run:
        os.environ['SIMULATOR_RUN_NAME'] = 'debug_test'
        os.environ['SIMULATOR_MODE'] = 'RUN'
        os.environ['SIMULATOR_INPUT_DIR'] = './hash_files/'
        os.environ['SIMULATOR_OUTPUT_DIR'] = './logs/'
        os.environ['SIMULATOR_TRACES_LISTS_DIR'] = './simulator/front_end/src/traces/'
        os.environ['SIMULATOR_TRACES_LISTS'] = 'fslhomes_2011-8kb-only_018'
        os.environ['SIMULATOR_REGION_ALGO'] = 'FIXED-SIZE'
        os.environ['SIMULATOR_MIN_REGION_SIZE'] = '2'
        os.environ['SIMULATOR_MAX_REGION_SIZE'] = '6'
        os.environ['SIMULATOR_BIT_MASK'] = '5'
        os.environ['SIMULATOR_REGION_SIZE'] = '4'
        os.environ['SIMULATOR_ROUTING'] = 'FIRST_FINGERPRINT_7'
        os.environ['SIMULATOR_DOMAINS'] = '100'
        os.environ['SIMULATOR_BACKEND_IPS'] = 'localhost'

    # run a hello world test
    if os.environ['SIMULATOR_MODE'] == 'HELLO':
        print(f"Hello Server running on front_end.")
        serve()

    # run the full simulator
    if os.environ['SIMULATOR_MODE'] == 'RUN':
        sim = Simulator()
        sim.simulate()

    print("Front End shutting down...")


if __name__ == "__main__":
    main()



