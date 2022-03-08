from htbcli.cli import cli
import hackthebox
import mock_hackthebox
from mock_nm_output import *


def test_vpn_connect_server(fp, monkeypatch, runner):
    """Test `htb vpn connect -s ` to various servers"""

    # `vpn connect -s eu-vip-5`, when current is us-vip-7
    fp_disconnect(fp)
    fp_get_vpn_server(fp)
    fp_add_connection(fp)
    fp_get_active_connection_name(fp, disconnected=True)
    fp_connect_to(fp)
    fp_print_status(fp)
    result = runner.invoke(cli, ["vpn", "connect", "-s", "eu-vip-6"])
    assert "Local connection" in result.output
    assert "Current HTB Lab" in result.output
    assert "Current RA" in result.output
    assert len(fp.definitions) == 0

    # fail on import
    fp_disconnect(fp)
    fp_get_vpn_server(fp)
    fp_add_connection(fp, fail_import=True)
    result = runner.invoke(cli, ["vpn", "connect", "-s", "eu-vip-5"])
    assert "[-] Unable to add connection for " in result.output
    assert len(fp.definitions) == 0

    # bad server
    result = runner.invoke(cli, ["vpn", "connect", "-s", "not-a-real-server"])
    assert result.output.startswith(
        "[-] Unable to find vpn server named not-a-real-server"
    )
    assert len(fp.definitions) == 0

    # fail to switch
    orig_func = hackthebox.VPNServer.switch
    monkeypatch.setattr(
        hackthebox.VPNServer,
        "switch",
        mock_hackthebox.mock_vpn_server.switch_fail_alt,
    )

    fp_disconnect(fp)
    result = runner.invoke(cli, ["vpn", "connect", "-s", "eu-vip-6"])
    assert result.output == "[-] Switch to eu-vip-6 failed\n"
    assert len(fp.definitions) == 0

    monkeypatch.setattr(
        hackthebox.VPNServer, "switch", mock_hackthebox.mock_vpn_server.switch_raise_alt
    )

    fp_disconnect(fp)
    result = runner.invoke(cli, ["vpn", "connect", "-s", "eu-vip-5"])
    assert (
        result.output
        == "[-] Unable to switch with active machine. Power down current machine first\n"
    )
    assert len(fp.definitions) == 0
    monkeypatch.setattr(hackthebox.Machine, "spawn", orig_func)

    # fail to disconnect
    fp_disconnect(fp, success=False)
    result = runner.invoke(cli, ["vpn", "connect", "-s", "eu-vip-6"])
    assert len(fp.definitions) == 0
    assert result.output == "[-] Failed to disconnect VPN. Cannot continue.\n"


def test_vpn_connect(fp, runner):
    """Test `htb vpn connect`"""
    fp_get_vpn_server(fp)
    fp_add_connection(fp)
    fp_get_active_connection_name(fp)
    fp_print_status(fp)
    result = runner.invoke(cli, ["vpn", "connect"])
    assert "Local connection" in result.output
    assert "Current HTB Lab" in result.output
    assert "Current RA" in result.output
    assert len(fp.definitions) == 0


def test_vpn_connect_fail(fp, runner):
    """Test `htb vpn connect`"""
    fp_get_vpn_server(fp)
    fp_add_connection(fp)
    fp_get_active_connection_name(fp, disconnected=True)
    fp_connect_to(fp, success=False)
    result = runner.invoke(cli, ["vpn", "connect"])
    assert result.output == "[-] Failed to connect to htbcli\n"
    assert len(fp.definitions) == 0


def test_vpn_status(fp, runner):
    """Test `htb vpn status`"""
    fp_print_status(fp)
    result = runner.invoke(cli, ["vpn", "status"])
    assert "Local connection" in result.output
    assert "Current HTB Lab" in result.output
    assert "Current RA" in result.output
    assert len(fp.definitions) == 0


def test_vpn_connect_ra(fp, runner):
    """Test `htb vpn connect-ra`"""
    fp_disconnect(fp)
    fp_get_vpn_server(fp)
    fp_add_connection(fp)
    fp_get_active_connection_name(fp, disconnected=True)
    fp_connect_to(fp)
    fp_print_status(fp, disconnected=True)
    result = runner.invoke(cli, ["vpn", "connect-ra"])
    assert "[*] Local connection" in result.output
    assert len(fp.definitions) == 0


def test_vpn_connect_ra_fail_disconnect(fp, runner):
    """Test `htb vpn connect-ra`"""
    fp_disconnect(fp, success=False)
    result = runner.invoke(cli, ["vpn", "connect-ra"])
    assert result.output == "[-] Failed to disconnect VPN. Cannot continue.\n"
    assert len(fp.definitions) == 0


def test_vpn_connect_ra_no_servers(fp, monkeypatch, runner):
    """Test `htb vpn connect-ra` when no valid servers return"""
    orig_func = hackthebox.HTBClient.get_all_vpn_servers
    monkeypatch.setattr(
        hackthebox.HTBClient,
        "get_all_vpn_servers",
        mock_hackthebox.mock_client.get_all_vpn_servers_none_alt,
    )
    result = runner.invoke(cli, ["vpn", "connect-ra"])
    assert result.output.startswith("[-] Unable to find vpn server in ")
    assert len(fp.definitions) == 0
    monkeypatch.setattr(hackthebox.Machine, "spawn", orig_func)


def test_vpn_connect_ra_switch_fails(fp, monkeypatch, runner):
    # fail to switch
    orig_func = hackthebox.VPNServer.switch
    monkeypatch.setattr(
        hackthebox.VPNServer,
        "switch",
        mock_hackthebox.mock_vpn_server.switch_fail_alt,
    )

    fp_disconnect(fp)
    result = runner.invoke(cli, ["vpn", "connect-ra"])
    assert result.output == "[-] Switch to EU Release Lab 1 failed\n"
    assert len(fp.definitions) == 0

    monkeypatch.setattr(
        hackthebox.VPNServer, "switch", mock_hackthebox.mock_vpn_server.switch_raise_alt
    )

    fp_disconnect(fp)
    result = runner.invoke(cli, ["vpn", "connect-ra"])
    assert (
        result.output
        == "[-] Unable to switch with active machine. Power down current machine first\n"
    )
    assert len(fp.definitions) == 0
    monkeypatch.setattr(hackthebox.Machine, "spawn", orig_func)


def test_vpn_connect_ra_add_connection_fail(fp, runner):
    fp_disconnect(fp)
    fp_get_vpn_server(fp)
    fp_add_connection(fp, fail_import=True)
    result = runner.invoke(cli, ["vpn", "connect-ra"])
    assert result.output == "[-] Unable to add connection for htbcli-ra\n"
    assert len(fp.definitions) == 0


def test_vpn_connect_ra_failed_connection(fp, runner):
    """Test failure of `connect_to` in `vpn connect-ra`"""
    fp_disconnect(fp)
    fp_get_vpn_server(fp)
    fp_add_connection(fp, connection_exists=False)
    fp_get_active_connection_name(fp, disconnected=True)
    fp_connect_to(fp, success=False)
    result = runner.invoke(cli, ["vpn", "connect-ra"])
    assert result.output == "[-] Failed to connect to htbcli-ra\n"
    assert len(fp.definitions) == 0


def test_vpn_disconnect(fp, runner):
    fp_disconnect(fp)
    fp_print_status(fp)
    result = runner.invoke(cli, ["vpn", "disconnect"])
    assert "[*] Local connection" in result.output
    assert len(fp.definitions) == 0

    fp_disconnect(fp, success=False)
    result = runner.invoke(cli, ["vpn", "disconnect"])
    assert result.output == "[-] Failed to disconnect VPN.\n"
    assert len(fp.definitions) == 0


def test_vpn_labs(fp, runner):
    fp_get_active_connection_name(fp)
    fp_get_connection_ip(fp)
    fp_get_vpn_server(fp)
    result = runner.invoke(cli, ["vpn", "labs"])
    lines = result.output.split("\n")
    assert len(lines) == 76
    assert len([l for l in lines if "US" in l]) == 32
    assert len([l for l in lines if "VIP " in l]) == 58
    assert len([l for l in lines if "VIP+" in l]) == 3
    assert len(fp.definitions) == 0

    fp_get_active_connection_name(fp, disconnected=True)
    result = runner.invoke(cli, ["vpn", "labs", "-t", "RA"])
    lines = result.output.split("\n")
    assert len(lines) == 7
    assert len([l for l in lines if "US" in l]) == 1
    assert len([l for l in lines if "Release " in l]) == 2
    assert len(fp.definitions) == 0

    fp_get_active_connection_name(fp, disconnected=True)
    result = runner.invoke(cli, ["vpn", "labs", "-t", "vip+", "-r", "sg"])
    assert result.output == "[-] No labs matched that criteria\n"
    assert len(fp.definitions) == 0


def test_status(runner, fp):
    """Test `htb status`"""
    fp_print_status(fp)
    res = runner.invoke(cli, ["status"])
    assert "US VIP 7" in res.output
    assert "EU Release Lab 1" in res.output
    assert "IP:              10.10.11.145" in res.output
    assert "Name:            RouterSpace" in res.output


# functions to patch subprocess calls
def fp_disconnect(fp, success=True):
    fp_get_active_connection_name(fp)
    if success:
        fp.register("nmcli connection down id htbcli".split())
    else:
        fp.register("nmcli connection down id htbcli", stderr="ERROR")


def fp_get_active_connection_name(fp, disconnected=False):
    if disconnected:
        stdout = NMCLI_CONNECTION_SHOW_ACTIVE_DISCONNECTED
    else:
        stdout = NMCLI_CONNECTION_SHOW_ACTIVE
    fp.register("nmcli connection show --active".split(), stdout=stdout)


def fp_connect_to(fp, success=True):
    fp_disconnect(fp)
    if success:
        fp.register(
            ["nmcli", "connection", "up", "id", fp.any()],
            stdout="Connection successfully activated (D-Bus active path: /org/freedesktop/NetworkManager/ActiveConnection/126)",
        )
    else:
        fp.register(["nmcli", "connection", "up", "id", fp.any()], stderr="ERROR")


def fp_get_connection_ip(fp):
    fp_get_active_connection_name(fp)
    fp.register(
        "nmcli -g ip4.address connection show htbcli".split(), stdout="10.10.14.18/23\n"
    )


def fp_connect_exists(fp, connection_exists=True):
    if connection_exists:
        fp.register("nmcli connection show".split(), stdout=NMCLI_CONNECTION_SHOW)
    else:
        fp.register("nmcli connection show", stdout=NMCLI_CONNECTION_SHOW_WO_HTBCLI)


def fp_add_connection(fp, fail_import=False, connection_exists=True):
    fp_connect_exists(fp, connection_exists=connection_exists)
    if connection_exists:
        fp.register(
            ["nmcli", "connection", "delete", fp.any()],
            stdout="Connection 'htbcli' (34bde648-0a9a-4dc0-abb4-e72b0c527cfd) successfully deleted.",
        )
    if fail_import:
        fp.register(
            "nmcli connection import type openvpn file".split() + [fp.any()],
            stderr="ERROR",
        )
    else:
        fp.register("nmcli connection import type openvpn file".split() + [fp.any()])
        fp.register(["nmcli", "connection", "modify", fp.any()], stdout="OK")


def fp_get_vpn_server(fp):
    fp.register(
        ["nmcli", "connection", "export", fp.any()],
        stdout=NMCLI_CONNECTION_EXPORT_HTBCLI,
    )


def fp_print_status(fp, disconnected=False):
    if disconnected:
        fp_get_active_connection_name(fp, disconnected=True)
    else:
        fp_get_active_connection_name(fp)
        fp_get_connection_ip(fp)
        fp_get_vpn_server(fp)
