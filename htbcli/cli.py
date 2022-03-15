#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
HackTheBox Command Line Interface

.. currentmodule:: htbcli.cli
.. moduleauthor:: 0xdf <0xdf@hackthebox.eu>
"""
from email.policy import default
from json.decoder import JSONDecodeError
import click
from click_shell import shell
from hackthebox import HTBClient
import os
from .version import __version__
from . import output
from .vpn.commands import vpn
from .box.commands import box
from .vpn.commands import print_status as print_vpn_status
from .box.formatter import print_status as print_box_status


banner = r"""
            .-⁻⁻-._
        .-⁻`        `⁻-.
    .-⁻`                `⁻-_   __  __  ______  ____            ___
    |`⁻-.                 .-|/\ \/\ \/\__  _\/\  _`\         /\_ \   __
    |    `⁻-.         .-⁻`  |\ \ \_\ \/_/\ \/\ \ \L\ \    ___\//\ \ /\_\
    |        `⁻-...-⁻`      | \ \  _  \ \ \ \ \ \  _ <'  /'___\\ \ \\/\ \
    |            |          |  \ \ \ \ \ \ \ \ \ \ \L\ \/\ \__/ \_\ \\ \ \
    |            |          |   \ \_\ \_\ \ \_\ \ \____/\ \____\/\____\ \_\
    |            |          |    \/_/\/_/  \/_/  \/___/  \/____/\/____/\/_/
    `⁻-.         |       .-`
        `⁻-.     |   .-⁻`
            `⁻-..|-⁻`
"""
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@shell(prompt="HackTheBox> ", intro=banner, context_settings=CONTEXT_SETTINGS)
@click.option(
    "--cache-cred",
    type=click.Choice(["None", "Short", "Long"], case_sensitive=False),
    default="Long",
    help="Cache access token and refresh token. Short tokens are valid for 1 day, Long for 30 days.",
)
@click.option(
    "--cache-location",
    type=click.Path(),
    default="~/.config/hackthebox",
    help="Location of file that stores the cached credential.",
)
@click.pass_context
def cli(ctx, cache_cred, cache_location):
    """HackTheBox Shell"""
    if cache_cred == "None":
        client = HTBClient()
    else:
        try:
            client = HTBClient(
                cache=os.path.expanduser(cache_location),
                remember=(cache_cred == "Long"),
            )
        except JSONDecodeError:
            client = HTBClient()
    ctx.obj = client


@cli.command()
def version():
    """Get the library version."""
    output.info(f"{__version__}")


@cli.command()
def status():
    """Print comprehensive status"""
    print_vpn_status()
    print_box_status()


cli.add_command(vpn)
cli.add_command(box)
