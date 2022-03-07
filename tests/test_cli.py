from htbcli.version import __version__
from htbcli.cli import cli, banner


def test_version(runner):
    """Test `htb version`"""
    result = runner.invoke(cli, ["version"])
    assert f"[*] {__version__}\n" == result.output


def test_no_cache(runner):
    """Test `htb --cache-cred None`"""
    res = runner.invoke(
        cli, ["--cache-cred", "None"], input="test@htb.htb\npassword!\n"
    )
    assert banner in res.output
    assert res.output.endswith("\n\nHackTheBox> \n")


def test_status(runner):
    """Test `htb status`"""
    res = runner.invoke(cli, ["status"])
    assert "US VIP 7" in res.output
    assert "EU Release Lab 1" in res.output
    assert "IP:              10.10.11.145" in res.output
    assert "Name:            RouterSpace" in res.output

