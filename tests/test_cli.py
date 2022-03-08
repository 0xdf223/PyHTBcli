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