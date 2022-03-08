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
