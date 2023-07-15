import pathlib
import argparse
import subprocess

import conda.plugins
from ruamel.yaml import YAML


def add_package(package_spec: str)->None:
    environment_filename = pathlib.Path('environment.yml')

    print(f"Adding package {package_spec}")
    yaml = YAML(typ='safe')  # default, if not specfied, is 'rt' (round-trip)

    if environment_filename.is_file():
        with environment_filename.open() as f:
            env_doc = yaml.load(f)
    else:
        pathlib.Path.cwd().name
        env_doc = {
            'name': pathlib.Path.cwd().stem,
            'channels': ['conda-forge'],
            'dependencies': []
        }

    env_doc['dependencies'].append(package_spec)

    with open('environment.yml', 'w') as f:
        yaml.dump(env_doc, f)

    print(f"Added package {package_spec} to environment.yml")



def solve_environment(
    # platforms=['osx-64', 'linux-64', 'win-64', 'osx-arm64'],
    platforms=['linux-64'],
    # channels=['conda-forge'],
    channels=['defaults'],
    lock_filename='environment.yml.lock',
):
    from conda.base.context import context
    if context.subdir not in platforms:
        platforms.append(context.subdir)

    command = [
        'conda-lock',
        'lock',
        '--lockfile', lock_filename,
    ]
    for platform in platforms:
        command += ['--platform', platform]

    for channel in channels:
        command += ['--channel', channel]

    subprocess.run(command, capture_output=False)


def install_environment(
    lock_filename='environment.yml.lock',
):
    environment_filename = pathlib.Path('environment.yml')
    yaml = YAML(typ='safe')  # default, if not specfied, is 'rt' (round-trip)
    with environment_filename.open() as f:
        env_doc = yaml.load(f)

    command = [
        'conda-lock',
        'install',
        '--name', env_doc['name'],
        str(lock_filename)
    ]
    subprocess.run(command, capture_output=False)


def handle_install(args: list[str]):
    add_package(args[0])
    solve_environment()
    install_environment()


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
