"""Box Power commands"""
import click
from hackthebox import HTBClient
from hackthebox.errors import NotFoundException
from .formatter import print_status
from .. import output


@click.group()
def power():
    """Information and interaction with Boxes having to do with powering"""
    pass


@power.command()
@click.pass_obj
@click.option(
    "-f",
    "--force",
    is_flag=True,
    help="If you already have a powered on machine, power it off and power new machine on",
)
@click.argument("Box_Name")
def on(client: HTBClient, force: bool, box_name: str):
    """Search for a box with the given name and power it on"""
    try:
        box = client.get_machine(box_name)
    except NotFoundException:
        output.error(f"Unable to find machine named {box_name}")
        return False

    active = client.get_active_machine(release_arena=box.is_release)

    if active:
        if active.machine.id == box.id:
            output.info(
                f"{box.name} is already active in {active.server.friendly_name}."
            )
            return
        if not force:
            output.info(f"Account has an active machine: {active.machine.name}")
            if not click.confirm("Power off in order to continue?"):
                return False

        output.info(f"Powering off {active.machine.name}...")
        active.stop()

    try:
        output.info(f"Powering on {box.name}...")
        box.start(release_arena=box.is_release)
    except Exception as e:
        output.error(str(e))
    print_status()


@power.command()
@click.pass_obj
@click.option("--release-arena", "--ra", is_flag=True, default=False)
def off(client: HTBClient, release_arena: bool):
    """Power off active machine, lab or release arena"""

    box = client.get_active_machine(release_arena=release_arena)
    if box:
        output.info(f"Powering off {box.machine.name}...")
        box.stop()
    else:
        output.error("No active box")
    print_status()


@power.command()
@click.pass_obj
@click.option("--release-arena", "--ra", is_flag=True)
def reset(client: HTBClient, release_arena: bool):
    """Reset current active machine, lab or release arena"""

    box = client.get_active_machine(release_arena=release_arena)
    if box:
        output.info(f"Resetting {box.machine.name}")
        box.reset()
    else:
        output.error("No active box")
    print_status()
