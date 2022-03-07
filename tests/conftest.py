from click.testing import CliRunner
from pytest import fixture
import inspect
import hackthebox
import subprocess
import time
from mock_hackthebox import (
    mock_client,
    mock_machine,
    mock_machine_instance,
    mock_vpn_server,
    mock_search,
)
from mock_nm_output import *


@fixture(scope="session")
def runner():
    return CliRunner()


@fixture(autouse=True)
def patch_htb_client(monkeypatch):
    for name, func in inspect.getmembers(mock_client, predicate=inspect.isfunction):
        if name.endswith("_alt"):
            continue
        monkeypatch.setattr(hackthebox.HTBClient, name, func)
    for name, func in inspect.getmembers(mock_machine, predicate=inspect.isfunction):
        if name.endswith("_alt"):
            continue
        monkeypatch.setattr(hackthebox.Machine, name, func)
    for name, func in inspect.getmembers(
        mock_machine_instance, predicate=inspect.isfunction
    ):
        if name.endswith("_alt"):
            continue
        monkeypatch.setattr(hackthebox.MachineInstance, name, func)
    for name, func in inspect.getmembers(mock_vpn_server, predicate=inspect.isfunction):
        if name.endswith("_alt"):
            continue
        monkeypatch.setattr(hackthebox.VPNServer, name, func)
    for name, func in inspect.getmembers(mock_search, predicate=inspect.isfunction):
        if name.endswith("_alt"):
            continue
        monkeypatch.setattr(hackthebox.Search, name, func)


@fixture(autouse=True)
def patch_sleep(monkeypatch):
    monkeypatch.setattr(time, "sleep", lambda x: True)


# @fixture(autouse=True)
# def patch_subprocess(fp):
#     fp.keep_last_process(True)
#     fp.register(
#         "nmcli connection export htbcli".split(), stdout=NMCLI_CONNECTION_EXPORT_HTBCLI
#     )
#     fp.register(
#         "nmcli connection show --active".split(), stdout=NMCLI_CONNECTION_SHOW_ACTIVE
#     )
#     fp.register(
#         "nmcli -g ip4.address connection show htbcli".split(), stdout="10.10.14.18/23\n"
#     )
#     fp.register("nmcli connection show".split(), stdout=NMCLI_CONNECTION_SHOW)
#     fp.register(
#         "nmcli connection delete htbcli".split(),
#         stdout="Connection 'htbcli' (34bde648-0a9a-4dc0-abb4-e72b0c527cfd) successfully deleted.",
#     )
#     fp.register("nmcli connection import type openvpn file".split() + [fp.any()])
#     fp.register("nmcli connection modify htbcli ipv4.never-default true".split())
#     fp.register("nmcli connection down id htbcli".split())
