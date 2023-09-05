import time

import click

from dmxcontroller import Universe
from fixture import Fixture, FIXTURE_SPECS

from serial.tools.list_ports import comports
from tqdm import tqdm


FIXTURES = [
    Fixture(1, FIXTURE_SPECS["BBP93"]),
]


def check_fixture(dmx: Universe, fixture: Fixture) -> None:
    for fun in tqdm(fixture.spec.functions):
        print(fun)
        dmx.set_channel()
        fun
    fixture.dimmer
    fixture


@click.group()
def cli():
    pass


@cli.command()
def list_devices():
    ports = comports()
    for port, desc, hwid in ports:
        click.echo(f"{port}")


@cli.command()
def demo():
    pass


if __name__ == "__main__":
    cli()
