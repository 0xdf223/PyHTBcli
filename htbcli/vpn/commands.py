"""VPN commands"""
import click
import os
from tempfile import TemporaryDirectory
from hackthebox.errors import CannotSwitchWithActive
from . import nm, htb, util
from .. import output
from ..common_options import pager_option


VPN_PROFILE_NAME = "htbcli"
VPN_PROFILE_NAME_RA = "htbcli-ra"


@click.group()
def vpn():
    """VPN Connection Commands"""
    pass


@vpn.command()
@click.option("-s", "--server", "server_str", help="Specify server to connect to")
@click.option(
    "--refresh-key",
    is_flag=True,
    help="Download fresh VPN key from HTB even if the local one is for the same lab. Try if connection is hanging.",
)
def connect(server_str: str, refresh_key: bool):
    """
    Connect local system to HTB Labs over VPN

    Servers arecase-insensitive and typically of the format [Region]-[Type]-[Num].
    Can use spaces or - between.

    \b
    Examples:
      $ htb vpn connect -s us-free-2
      $ htb vpn connect --server au-vip-1
      HackTheBox> vpn connect -s 'EU vIp 20'
      $ htb vpn connect -s 'eu vip+ 1'
    """

    # Make sure HTB has requested server as "active" for user
    htb_current_server = htb.get_current()
    if server_str:
        server_name = util.format_name(server_str)
        if util.format_name(htb_current_server.friendly_name) != server_name:
            vpn_server = htb.get_server(server_name)
            if not vpn_server:
                output.error(
                    f"Unable to find vpn server named {server_str}\n"
                    + "    Use `htb vpn labs` command to list labs"
                )
                return
            # always disconnect before switching server or API may break
            if not nm.disconnect():
                output.error("Failed to disconnect VPN. Cannot continue.")
                return
            try:
                if vpn_server.switch():
                    htb_current_server = vpn_server
                else:
                    output.error(f"Switch to {server_name} failed")
                    return
            except CannotSwitchWithActive:
                output.error(
                    f"Unable to switch with active machine. Power down current machine first"
                )
                return

    # see if current VPN_PROFILE_NAME matches target
    current_htbcli_server = nm.get_vpn_server(VPN_PROFILE_NAME)
    if refresh_key or current_htbcli_server != util.format_name(
        htb_current_server.friendly_name
    ):
        tempdir = TemporaryDirectory()
        ovpn_path = os.path.join(tempdir.name, f"{VPN_PROFILE_NAME}.ovpn")
        htb_current_server.download(path=ovpn_path)
        if not nm.add_connection(VPN_PROFILE_NAME, ovpn_path, force=True):
            output.error(f"Unable to add connection for {VPN_PROFILE_NAME}")
            tempdir.cleanup()
            return
        tempdir.cleanup()

    # connect if not already
    if nm.get_active_connection_name() != VPN_PROFILE_NAME:
        if not nm.connect_to(VPN_PROFILE_NAME):
            output.error(f"Failed to connect to {VPN_PROFILE_NAME}")
            return

    print_status()


@vpn.command()
@click.option(
    "-r",
    "--region",
    type=click.Choice(["US", "EU"], case_sensitive=False),
    help="Region to connect to. Without specifying, will connect to most recent lab on HTB.",
)
@click.option(
    "--refresh-key",
    is_flag=True,
    help="Download fresh VPN key from HTB even if the local one is for the same lab. Try if connection is hanging.",
)
def connect_ra(region: str, refresh_key: bool):
    """Connect to Release Arena network"""
    current = htb.get_current(ra=True)
    if not region:
        region = current.friendly_name if current else "EU"

    ra_servers = htb.get_labs(ra=True)
    try:
        vpn_server = next(
            s
            for s in sorted(ra_servers, key=lambda x: x.current_clients)
            if s.friendly_name.lower().startswith(region.lower())
        )
    except StopIteration:
        output.error(
            f"Unable to find vpn server in {region}\n"
            + "    Use `htb vpn labs` command to list labs"
        )
        return
    # always disconnect before switching server or API may break
    if not nm.disconnect():
        output.error("Failed to disconnect VPN. Cannot continue.")
        return
    try:
        if vpn_server.switch():
            htb_current_server = vpn_server
        else:
            output.error(f"Switch to {vpn_server.friendly_name} failed")
            return
    except CannotSwitchWithActive:
        output.error(
            f"Unable to switch with active machine. Power down current machine first"
        )
        return

    # see if current VPN_PROFILE_NAME matches target
    current_htbcli_ra_server = nm.get_vpn_server(VPN_PROFILE_NAME_RA)
    if refresh_key or current_htbcli_ra_server != util.format_name(
        vpn_server.friendly_name
    ):
        tempdir = TemporaryDirectory()
        ovpn_path = os.path.join(tempdir.name, f"{VPN_PROFILE_NAME_RA}.ovpn")
        htb_current_server.download(path=ovpn_path)
        if not nm.add_connection(VPN_PROFILE_NAME_RA, ovpn_path, force=True):
            output.error(f"Unable to add connection for {VPN_PROFILE_NAME_RA}")
            tempdir.cleanup()
            return
        tempdir.cleanup()

    if nm.get_active_connection_name() != VPN_PROFILE_NAME_RA:
        if not nm.connect_to(VPN_PROFILE_NAME_RA):
            output.error(f"Failed to connect to {VPN_PROFILE_NAME_RA}")
            return

    print_status()


@vpn.command()
def disconnect():
    """Disconnect from VPN"""
    if not nm.disconnect():
        output.error("Failed to disconnect VPN.")
        return
    print_status()


@vpn.command()
def status():
    """
    Print current status, showing current HTB lab and connection details.

    The HTB lab is the lab that the HTB system expects you to connect to. If
    this is out of sync with what you are connected to, submitted flags and power
    commands won't work.
    """
    print_status()


def print_status():
    htb_current_server = htb.get_current()
    htb_current_ra = htb.get_current(ra=True)
    active_connection = nm.get_active_connection_name()
    if active_connection:
        ip = nm.get_connection_ip()
        vpn_server = nm.get_vpn_server(active_connection)
        output.info(
            f"Local connection:\n"
            + f"        IP:              {ip}\n"
            + f"        VPN Profile:     {active_connection}\n"
            + f"        VPN Server:      {vpn_server}"
        )
    else:
        output.info("Local connection:    Not connected")
    output.info(
        f"Current HTB Lab:     {htb_current_server}\n"
        + f"    Current RA:          {htb_current_ra}"
    )


@vpn.command()
@click.option(
    "-t",
    "--type",
    "lab_filter",
    type=click.Choice(["Free", "VIP", "VIP+", "RA"], case_sensitive=False),
    help="Filter by Lab type",
)
@click.option(
    "-r",
    "--region",
    "region_filter",
    type=click.Choice(["US", "EU", "AU", "SG"], case_sensitive=False),
    help="Filter by region",
)
@pager_option
def labs(lab_filter, region_filter, pager):
    """Show the HTB labs available to the user, and how many players are in each"""

    # clean up strings for comparison
    if not region_filter:
        region_filter = ""
    if not lab_filter:
        lab_filter = ""
    elif lab_filter == "RA":
        lab_filter = "Release"

    # fetch labs
    labs = htb.get_labs() + htb.get_labs(ra=True)

    # get current lab and connection info
    current_lab = htb.get_current()
    current_connection_profile = nm.get_active_connection_name()
    if current_connection_profile:
        current_ip = nm.get_connection_ip()
        current_server = nm.get_vpn_server(current_connection_profile)
    else:
        current_server = None

    # build table
    header = ["Lab", "Current Users", "Status"]
    rows = []
    for lab in labs:
        lab_region, lab_type = lab.friendly_name.split()[:2]
        if lab_region.startswith(region_filter) and lab_type.startswith(lab_filter):
            status = ""
            if lab.friendly_name == current_lab.friendly_name:
                status = "\uf2c0"
                if not current_server or current_server != util.format_name(
                    lab.friendly_name
                ):
                    status += f" Not Connected"
            if current_server and current_server == util.format_name(lab.friendly_name):
                status += f" {current_ip}"

            rows.append([lab.friendly_name, lab.current_clients, status])

    if rows:
        if not any(r[2] for r in rows):
            header = header[:2]
            rows = [row[:2] for row in rows]
        output.table(header, rows, pager=pager)
    else:
        output.error("No labs matched that criteria")
