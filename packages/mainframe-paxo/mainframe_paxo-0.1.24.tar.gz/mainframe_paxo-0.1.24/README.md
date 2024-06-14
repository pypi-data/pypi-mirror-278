# ![PaxDeiLogo](https://playpaxdei.com/_next/image?url=%2Fstatic%2Fimages%2Fpaxdei-monogram-silver.png&w=64&q=75 "Get it?") Paxo - development utilities for PaxDei

## Introduction

This is a collection of scripts and tools to facilitate the development process
of PaxDei using a command line utility.  The philosophy is that a regular developer can perform most complex development tasks using a single command
line utility.  The utility can then be updated and expanded as needs arise.

Tasks that can be performed include

- *initial-setup*:  Installing necessary tools, p4, setting up workspaces, syncing
- *sync*: perforce sync of a branch
- *work-in*: switching branches
- *update*: update the utility

## Installing

The only pre-requisite for running paxo is having a recent Python ryeinstalled, along with [pipx](https://github.com/pypa/pipx).  To install, simply type

`pipx install mainframe-paxo`

This installation can be automated by a script which exists on `g:\dev\basic-install.bat` which will install the necessary pre-requisites, fetch paxo and run `paxo basic-install`.
the `basic-install.cmd` script is also available here, in `scripts/basic-install.cmd`.

## Usage

type `paxo --help` for instructions.

## Development

We use [rye](https://rye.astral.sh/) for development.  Install rye as per instructions on site.

### set up

run `rye sync` to set up a develoment env.

### publishing

To publish, the package version needs to be upgraded.  You then
run `poetry build` and `poetry publish` to publish this to PyPI.
First, though, you need to configure the PyPI access token:

`poetry config pypi-token.pypi <my-token>`

The token is in Onepass.

The steps are:

1. update the version in `pyproject.toml`, using `rye version --bump patch`. Commit and push.
2. `rye build`
4. `rye publish --skip-existing`


### updating

To update a client to the latest version, type
`rye tools install -f mainframe-paxo`