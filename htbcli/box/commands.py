"""Box commands"""
import click
from hackthebox import HTBClient
from hackthebox.errors import (
    IncorrectFlagException,
    UserAlreadySubmitted,
    RootAlreadySubmitted,
)
from .lister import lister
from .power import power
from .formatter import print_machine_table, print_status
from .. import output
from ..common_options import pager_option


@click.group()
def box():
    """Information and interaction with Boxes"""
    pass


box.add_command(lister)
box.add_command(power)


@box.command()
@click.pass_obj
def status(client: HTBClient):
    """Print current active machine"""

    print_status()


@box.command()
@click.pass_obj
@pager_option
@click.option(
    "--competitive",
    "competitive",
    is_flag=True,
    help="Limit search to competitive machines only",
)
@click.option(
    "--non-competitive",
    "non_competitive",
    is_flag=True,
    help="Limit search to non-competitive (retired) only",
)
@click.option("-d", "--diff", type=click.Choice("EMHI", case_sensitive=False))
@click.option("--todo", is_flag=True, help="Limit search to todo list")
def query(
    client: HTBClient,
    pager: bool,
    competitive: bool,
    non_competitive: bool,
    diff: str,
    todo: bool,
):
    """Use more complex criteria to search for boxes"""
    if not any([competitive, non_competitive, diff, todo]):
        click.echo(click.get_current_context().get_help())
        return

    todo_ids = client.get_todo_machines()

    boxes = []
    if not non_competitive:
        boxes += client.get_machines()
    if not competitive:
        boxes += client.get_machines(retired=True)

    if diff:
        boxes = [b for b in boxes if b.difficulty.startswith(diff)]
    if todo:
        boxes = [b for b in boxes if b.id in todo_ids]

    print_machine_table(boxes, pager, todo_ids)


@box.command()
@click.pass_obj
@click.argument("machine")
@click.argument("flag")
@click.argument("difficulty", type=click.IntRange(min=1, max=10))
def submit(client: HTBClient, machine, flag, difficulty):
    """
    Submit a flag for a box

    \b
    MACHINE - The name of the machine to submit for (case insensitive)
    FLAG - The flag from `user.txt` or `root.txt`
    DIFFICULTY - An integer from 1 to 10, where 10 is the hardest
    """
    box = client.get_machine(machine)
    try:
        box.submit(flag, difficulty * 10)
        output.success("Correct!")
    except IncorrectFlagException:
        output.error("Incorrect flag!")
    except UserAlreadySubmitted:
        output.error(f"User flag already accepted for {box.name}")
    except RootAlreadySubmitted:
        output.error(f"Root flag already accepted for {box.name}")
