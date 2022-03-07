"""Output functions"""
import click
from prettytable import PrettyTable

INFO = click.style("[*] ", "yellow")
ERROR = click.style("[-] ", "red")
SUCCESS = click.style("[+] ", "green")
DEBUG = click.style("[D] ", "blue")


def info(msg):
    """Print an information message"""
    click.echo(INFO + msg)


def error(msg):
    """Print an error message"""
    click.echo(ERROR + msg)


def success(msg):
    """Print success message"""
    click.echo(SUCCESS + msg)


# def debug(msg):
#     click.echo(DEBUG + msg)


def table(header, rows, pager=None):
    """Print a table"""
    t = PrettyTable()
    t.field_names = header
    t.add_rows(rows)
    if pager == True or (pager == None and len(rows) > 10):
        click.echo_via_pager(str(t))
    else:
        click.echo(t)
