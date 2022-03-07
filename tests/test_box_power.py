from pytest import raises
from htbcli.cli import cli
import hackthebox
import mock_hackthebox


def test_box_power_on(monkeypatch, runner):
    """Test various `htb box power on` commands"""
    res = runner.invoke(cli, ["box", "power", "on", "steamcloud", "-f"])
    assert res.output.startswith("[*] Powering off Acute")
    res = runner.invoke(cli, ["box", "power", "on", "steamcloud"], input="N\n")
    assert res.output.startswith("[*] Account has an active machine: ")
    res = runner.invoke(cli, ["box", "power", "on", "xxxxxxxx"])
    assert "[-] Unable to find machine named xxxxxxxx\n" == res.output
    res = runner.invoke(cli, ["box", "power", "on", "acute"])
    assert res.output.startswith("[*] Acute is already active in")

    orig_func = hackthebox.Machine.spawn
    monkeypatch.setattr(
        hackthebox.Machine,
        "spawn",
        mock_hackthebox.mock_machine.spawn_too_many_alt,
    )

    res = runner.invoke(cli, ["box", "power", "on", "steamcloud", "-f"])
    assert "[*] Powering off Acute..." in res.output
    assert "[*] Powering on SteamCloud..." in res.output
    assert (
        "[-] Failed to spawn: You need to wait 2 minutes before spawning another machine."
        in res.output
    )

    monkeypatch.setattr(hackthebox.Machine, "spawn", orig_func)


def test_box_power_off_and_reset(monkeypatch, runner):

    res = runner.invoke(cli, ["box", "power", "off"])
    assert "Powering off Acute..." in res.output

    res = runner.invoke(cli, ["box", "power", "reset"])
    assert "[*] Resetting Acute" in res.output

    orig_func = hackthebox.HTBClient.get_active_machine
    monkeypatch.setattr(
        hackthebox.HTBClient,
        "get_active_machine",
        mock_hackthebox.mock_client.get_active_machine_none_alt,
    )

    res = runner.invoke(cli, ["box", "power", "off"])
    assert res.output.startswith("[-] No active box")

    res = runner.invoke(cli, ["box", "power", "reset"])
    assert res.output.startswith("[-] No active box")

    monkeypatch.setattr(hackthebox.HTBClient, "get_active_machine", orig_func)
