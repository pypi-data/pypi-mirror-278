"""CLI entrypoints for hikrobotcamlib"""
import logging

import click
from libadvian.logging import init_logging

from hikrobotcamlib import __version__, DeviceList
from hikrobotcamlib.types import DeviceTransport

LOGGER = logging.getLogger(__name__)


@click.command()
@click.version_option(version=__version__)
@click.option("-l", "--loglevel", help="Python log level, 10=DEBUG, 20=INFO, 30=WARNING, 40=CRITICAL", default=30)
@click.option("-v", "--verbose", count=True, help="Shorthand for info/debug loglevel (-v/-vv)")
@click.option("--usb", is_flag=True, help="Use USB transport")
@click.option("--gige/--no-gige", is_flag=True, help="Use GigE transport", default=True)
def hikrobotcamlib_cli(loglevel: int, verbose: int, usb: bool, gige: bool) -> None:
    """List cameras"""
    if verbose == 1:
        loglevel = 20
    if verbose >= 2:
        loglevel = 10
    init_logging(loglevel)
    LOGGER.setLevel(loglevel)
    transports = 0
    if usb:
        transports |= DeviceTransport.USB
    if gige:
        transports |= DeviceTransport.GIGE

    for dev in DeviceList(transports):
        click.echo("Found {}".format(dev))
