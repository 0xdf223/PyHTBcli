from pydoc import cli
import click
from hackthebox import HTBClient, VPNServer
from . import util


@click.pass_obj
def get_server(client: HTBClient, server: str) -> VPNServer:
    """Get a VPNServer object by name"""

    servers = client.get_all_vpn_servers()
    filtered = [
        s for s in servers if server.lower() == util.format_name(s.friendly_name)
    ]
    if not filtered:
        return None
    assert len(filtered) == 1
    return filtered[0]


@click.pass_obj
def get_current(client: HTBClient, ra: bool = False) -> VPNServer:
    """Get the user's current VPNServer object"""
    return client.get_current_vpn_server(release_arena=ra)


@click.pass_obj
def get_labs(client: HTBClient, ra=False):
    """Get a list of all the VPN lab servers"""
    return client.get_all_vpn_servers(release_arena=ra)
