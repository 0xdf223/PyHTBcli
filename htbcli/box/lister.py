"""box list commands"""
import click
from hackthebox import HTBClient
from typing import Callable
from .formatter import print_machine_table
from ..common_options import pager_option


@click.group(name="list")
def lister():
    """Commands to list specific sets of boxes"""
    pass


@lister.command()
@pager_option
def competitive(pager):
    """Print competitive boxes"""
    print_boxes(active_only=True, filter_func=lambda x: True, pager=pager)


@lister.command()
@pager_option
def all(pager):
    """Print all boxes"""
    print_boxes(active_only=False, filter_func=lambda x: True, pager=pager)


@lister.command()
@click.option(
    "--active-only", "active", is_flag=True, help="Filter to only active boxes"
)
@pager_option
def unowned(active, pager):
    """Print unowned boxes"""
    filt = lambda b: not (b.user_owned and b.root_owned)
    print_boxes(active_only=active, filter_func=filt, pager=pager)


@lister.command()
@click.pass_obj
@pager_option
def todo(client: HTBClient, pager):
    """Print boxes on todo list"""
    todo_ids = client.get_todo_machines()
    filt = lambda b: b.id in todo_ids
    print_boxes(active_only=False, filter_func=filt, pager=pager)


@lister.command(name="from")
@click.pass_obj
@click.argument("author")
@pager_option
def _from(client: HTBClient, author, pager):
    """Get boxes from a given author"""
    author_user = client.search(author).users[0]
    box_ids = [m.id for m in author_user.get_content().machines]
    filt = lambda b: b.id in box_ids
    print_boxes(active_only=False, filter_func=filt, pager=pager)


@click.pass_obj
def print_boxes(client: HTBClient, active_only: bool, filter_func: Callable, pager):
    """Build the list of boxes to print and pass to `print_machine_table`"""
    todo_ids = client.get_todo_machines()

    boxes = client.get_machines()
    if not active_only:
        boxes += client.get_machines(retired=True)
    print_machine_table([b for b in boxes if filter_func(b)], pager, todo_ids)
