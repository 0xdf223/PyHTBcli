"""functions for interacting with NetworkManager"""
import click
import subprocess
import time
from typing import Optional


def connect_to(name: str):
    """Connect hte VPN to a given profile"""
    disconnect()
    proc = subprocess.run(
        "nmcli connection up id".split() + [name], capture_output=True
    )
    if proc.stderr:
        return False
    return True


def disconnect():
    """Disconnect the active local VPN connections"""
    active = get_active_connection_name()
    if active:
        proc = subprocess.run(
            "nmcli connection down id".split() + [active], capture_output=True
        )
        if not proc.stderr:
            return True
    return False


def get_active_connection_name() -> Optional[str]:
    """Get the name of the current connected profile"""
    active = subprocess.run(
        "nmcli connection show --active".split(), capture_output=True
    )
    for line in active.stdout.decode().split("\n"):
        if not line:
            continue
        name, _, type, _ = line.rsplit(None, 3)
        if name.startswith("htb") and type == "vpn":
            return name
    return None


def get_connection_ip() -> Optional[str]:
    """Get the current VPN IP"""
    conn_name = get_active_connection_name()
    if not conn_name:
        return None
    res = subprocess.run(
        "nmcli -g ip4.address connection show".split() + [conn_name],
        capture_output=True,
    )
    return res.stdout.decode().strip() if res.stdout else ""


def connection_exists(name: str) -> bool:
    """Check if a given connection profile already exists"""
    connections = subprocess.run(["nmcli", "connection", "show"], capture_output=True)
    for line in connections.stdout.decode().split("\n"):
        if " " in line and line.split()[0] == name:
            return True
    return False


def add_connection(name: str, ovpn_path: str, force: bool = False) -> bool:
    """Add a new connection profile"""
    if connection_exists(name):
        if not force and not click.confirm(f"{name} already exists. Overwrite?"):
            return False
        subprocess.run(["nmcli", "connection", "delete", name], capture_output=True)
    res = subprocess.run(
        "nmcli connection import type openvpn file ".split() + [ovpn_path],
        capture_output=True,
    )
    if res.stderr:
        return False
    time.sleep(1)
    res = subprocess.run(
        ["nmcli", "connection", "modify", name, "ipv4.never-default", "true"]
    )
    if res.stderr:
        return False
    return True


# def get_vpn_list() -> tuple:
#     active, vpns = [], []
#     res = subprocess.run(
#         "nmcli -f name,type,device connection show".split(), capture_output=True
#     )
#     for line in res.stdout.decode().split("\n"):
#         if not line:
#             continue
#         name, ctype, dev = line.rsplit(None, 2)
#         if ctype != "vpn":
#             continue
#         if dev != "--":
#             active.append(name)
#         else:
#             vpns.append(name)
#     return (vpns, active)


def get_vpn_server(connection: str) -> Optional[str]:
    """Get the server associated with a given VPN profile"""
    res = subprocess.run(
        "nmcli connection export".split() + [connection], capture_output=True
    )
    if res.stderr:
        return None

    remote = next(
        (l for l in res.stdout.decode().split("\n") if l.startswith("remote")), None
    )
    if not remote:
        return None

    return "-".join(remote.split("'")[1].split(".")[0].split("-")[1:])
