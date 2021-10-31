## 💪 Getting Started

> https://docs.google.com/document/d/1-H0h2GN-14Hcp5mWwOrwPcTCV1HYhRVE1y7BR9VXs4U/edit#
> https://github.com/cthoyt/cookiecutter-snekpack  
> Python package structure based on this tutorial

### Command Line Interface

```shell
$ python -m back_end --help
$ python -m front_end --help
```

> TODO show the most useful thing the CLI does! The CLI will have documentation auto-generated
by `sphinx`.

## 🚀 Installation

The back_end depends on https://twmht.github.io/python-rocksdb/index.html which builds rocksdb from c++ source when 
it is installed. The requirements are slightly different for each OS https://github.com/facebook/rocksdb/blob/main/INSTALL.md
`simulator/back_end_dependencies` contains a Docker file which prepares a centos7 image with all dependencies installed. 

The most recent code and data can be installed directly from GitHub with:

```bash
$ git clone git+https://github.com/yrrah/cs6620-fall21-intelligent-assignment-of-data-to-dedup-nodes.git
$ cd cs6620-fall21-intelligent-assignment-of-data-to-dedup-nodes
$ pip install simulator/front_end
$ pip install simulator/back_end
```


To install in development mode, use the following:

```bash
$ git clone git+https://github.com/yrrah/cs6620-fall21-intelligent-assignment-of-data-to-dedup-nodes.git
$ cd cs6620-fall21-intelligent-assignment-of-data-to-dedup-nodes
$ pip install -e simulator/front_end
$ pip install -e simulator/back_end
```

### ⚖️ License

The code in this package is licensed under the MIT License.

<!--
### 📖 Citation

Citation goes here!
-->

<!--
### 🎁 Support

This project has been supported by the following organizations (in alphabetical order):

-->

### 🍪 Cookiecutter

This package was created with [@audreyfeldroy](https://github.com/audreyfeldroy)'s
[cookiecutter](https://github.com/cookiecutter/cookiecutter) package using [@cthoyt](https://github.com/cthoyt)'s
[cookiecutter-snekpack](https://github.com/cthoyt/cookiecutter-snekpack) template.

### ❓ Testing

After cloning the repository and installing `tox` with `pip install tox`, the unit tests in the `tests/` folder can be
run reproducibly with:

```shell
$ tox
```

Additionally, these tests are automatically re-run with each commit in a [GitHub Action](https://github.com//cs6620-fall21-intelligent-assignment-of-data-to-dedup-nodes/actions?query=workflow%3ATests).

### 📦 Making a Release

After installing the package in development mode and installing
`tox` with `pip install tox`, the commands for making a new release are contained within the `finish` environment
in `tox.ini`. Run the following from the shell:

```shell
$ tox -e finish
```

This script does the following:

1. Uses BumpVersion to switch the version number in the `setup.cfg` and
   `src/back_end/version.py` to not have the `-dev` suffix
2. Packages the code in both a tar archive and a wheel
3. Uploads to PyPI using `twine`. Be sure to have a `.pypirc` file configured to avoid the need for manual input at this
   step
4. Push to GitHub. You'll need to make a release going with the commit where the version was bumped.
5. Bump the version to the next patch. If you made big changes and want to bump the version by minor, you can
   use `tox -e bumpversion minor` after.
