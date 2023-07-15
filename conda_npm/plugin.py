import argparse

import conda.plugins
from ruamel.yaml import YAML


def add_package(package_spec: str)->None:
    print(f"Adding package {package_spec}")
    yaml = YAML(typ='safe')  # default, if not specfied, is 'rt' (round-trip)
    env_doc = yaml.load(open('environment.yml').read())
    env_doc['dependencies'].append(package_spec)
    with open('environment.yml', 'w') as f:
        yaml.dump(env_doc, f)
    print(f"Added package {package_spec} to environment.yml")


def handle_install(args: list[str]):
    add_package(args[0])


def conda_npm(args: list[str]):
    if args[0] == "install":
        print('handling install')
        handle_install(args[1:])


@conda.plugins.hookimpl
def conda_subcommands():
    yield conda.plugins.CondaSubcommand(
        name="npm",
        summary="An opinionated subcommand inspired by npm",
        action=conda_npm,
    )
