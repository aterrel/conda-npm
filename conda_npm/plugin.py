import argparse

import conda.plugins


def conda_npm(args: list[str]):
    print('I ran!')


@conda.plugins.hookimpl
def conda_subcommands():
    yield conda.plugins.CondaSubcommand(
        name="npm",
        summary="An opinionated subcommand inspired by npm",
        action=conda_npm,
    )
