"""Functions to print box information"""
import click
from typing import List, Tuple
from hackthebox import HTBClient
from hackthebox.machine import Machine
from .. import output


OSICON = {
    "linux": "\ue712 ",
    "windows": "\ue70f ",
    "openbsd": "🐡",
    "freebsd": "😈",
    "solaris": "🌞",
    "other": "❓",
}

DIFFCOLOR = {
    "easy": "green",
    "medium": "yellow",
    "hard": "red",
    "insane": "white",
}


DIFF = {
    "very easy": 10,
    "easy": 20,
    "medium": 30,
    "hard": 40,
    "insane": 50,
}


def print_machine_table(
    machines: List[Machine], pager: bool, todo: list = [], actives: Tuple = (None, None)
):
    """Print a table of machines"""
    # ["OS", "Name", "IP", "Rating", "User Owns", "Root Owns"]
    lines = []
    for machine in machines:
        os = click.style(
            OSICON.get(machine.os.lower(), OSICON.get("other")), fg="white"
        )
        name = click.style(
            machine.name, fg=DIFFCOLOR.get(machine.difficulty.lower(), "blue")
        )
        ip = machine.ip if machine.ip else "-----------"
        stars = click.style(f"{machine.stars:.1f}⭐", fg="yellow")
        user = click.style(
            f"{machine.user_owns:>5}\uf2c0", fg="cyan" if machine.user_owned else ""
        )
        root = click.style(
            f"{machine.root_owns:>5}\uf292", fg="red" if machine.root_owned else ""
        )
        retired = " " if machine.retired else click.style("\uf091", fg="yellow")
        todo_indicator = click.style("\uf7d0", fg="red") if machine.id in todo else " "
        lines.append(
            f"{os:<5} {name:<23} {ip:<14} {stars} {user} {root}   {retired} {todo_indicator}"
        )

    output = "\n".join(lines)
    if pager == True:
        click.echo_via_pager(output)
    elif pager == False:
        click.echo(output)
    elif len(machines) > 20:
        click.echo_via_pager(output)
    else:
        click.echo(output)


@click.pass_obj
def print_status(client: HTBClient, lab_only: bool = False, ra_only: bool = False):
    """Print the current machine status"""
    active = client.get_active_machine() if not ra_only else None
    ra = client.get_active_machine(release_arena=True) if not lab_only else None
    if active:
        output.info(
            "Current lab machine:\n        "
            + f"Name:            {active.machine.name}\n        "
            + f"IP:              {active.machine.ip}"
        )
    else:
        output.info("Current lab machine: None")
    if ra:
        output.info(
            "Current RA machine:\n        "
            + f"Name:            {ra.machine.name}\n        "
            + f"IP:              {ra.machine.ip}"
        )
    else:
        output.info("Current RA machine:  None")
