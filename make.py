"""
Install:
  pipenv install --dev
  pipenv run python make.py

Usage:
  make.py build
  make.py push
  make.py test
  make.py bump
  make.py -h | --help

Commands
  build     Build pyhton wheel.
  push      Push wheel to pypi.
  test      Run tests.
  bump      Run bump sequence.

Options:
  -h, --help    Show this screen.
"""
import prmt
import subprocess as sp
from docopt import docopt
from cmdi import print_summary
from buildlib import wheel, project, yaml

proj = yaml.loadfile("Project")


class Cfg:
    version = proj["version"]
    registry = "pypi"


def build_wheel(cfg: Cfg):
    return wheel.cmd.build(cleanup=True)


def push(cfg: Cfg):
    w = wheel.find_wheel("./dist", semver_num=cfg.version)
    return wheel.cmd.push(f"./dist/{w}")


def test(cfg: Cfg):
    sp.run(["python", "tests/timelog"])


def bump(cfg: Cfg):

    results = []

    if prmt.confirm("Do you want to BUMP VERSION number?", "n"):
        result = project.cmd.bump_version()
        cfg.version = result.val
        results.append(result)

    if prmt.confirm("Do you want to BUILD WHEEL?", "n"):
        results.append(build_wheel(cfg))

    if prmt.confirm("Do you want to PUSH WHEEL to PYPI?", "n"):
        results.append(push(cfg))

    new_release = cfg.version != proj["version"]

    return results


def run():

    cfg = Cfg()
    args = docopt(__doc__)
    results = []

    if args["build"]:
        results.append(build_wheel(cfg))

    if args["push"]:
        results.append(push(cfg))

    if args["test"]:
        test(cfg)

    if args["bump"]:
        results.extend(bump(cfg))

    if results:
        print_summary(results)


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\n\nScript aborted by user.")
