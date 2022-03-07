from pytest import raises
from htbcli.cli import cli
import hackthebox
import mock_hackthebox


def test_box_submit_flag(monkeypatch, runner):
    """Test various `htb box submit` commands"""
    result = runner.invoke(
        cli, ["box", "submit", "routerspace", "3a0478e0e11a50592b9799fb7d357483", "8"]
    )
    assert "Correct!" in result.output

    result = runner.invoke(cli, ["box", "submit", "routerspace", "wrong flag", "8"])
    assert "Incorrect" in result.output
