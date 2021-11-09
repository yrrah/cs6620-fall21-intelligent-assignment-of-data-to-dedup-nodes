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
from front_end.hash_files.get_hash_files import download_files, get_web_dir_list
from front_end.simulate import Simulator

logger = logging.getLogger(__name__)


@click.command()
@click.version_option()
@click.option('--demo', 'demo', flag_value=True)
@click.option('--hello_world', 'hello_world', flag_value=True)
@click.option('--run', 'run', flag_value=True)
def main(demo, hello_world, run):
    """CLI for front_end."""
    if demo:
        os.environ['SIMULATOR_MODE'] = 'DEMO'
        os.environ['SERVER_IP'] = 'localhost:50051'
    if hello_world:
        os.environ['SIMULATOR_MODE'] = 'HELLO'
    if run:
        os.environ['SIMULATOR_MODE'] = 'RUN'
        os.environ['INPUT_DIR'] = './hash_files/'
        os.environ['TRACES_SUBDIR'] = 'fslhomes/2011-8kb-only/'
        os.environ['TRACES_LIST'] = 'simulator/front_end/src/traces/user006.txt'
        os.environ['REGION_ALGO'] = 'FIXED-SIZE'
        os.environ['REGION_SIZE'] = '4'
        os.environ['ROUTING'] = 'SIMPLE'
        os.environ['DOMAINS'] = '2'
        os.environ['BACKEND_IPS'] = 'localhost,localhost'

    # run a small demo with 1 backend pod
    if os.environ['SIMULATOR_MODE'] == 'DEMO':
        print(f"Demo Client running on front_end.")
        if not os.path.exists("./hash_files"):
            os.makedirs("./hash_files")
        trace_files = get_web_dir_list("https://tracer.filesystems.org/traces/fslhomes/2011-8kb-only/", limit=15)
        download_files("./hash_files", "https://tracer.filesystems.org/traces/fslhomes/2011-8kb-only/", trace_files)
        hash_file_demo("./hash_files/fslhomes-user006-2011-09-10.8kb.hash.anon", 'localhost')

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



