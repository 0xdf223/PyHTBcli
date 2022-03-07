from htbcli.cli import cli
import hackthebox
import mock_hackthebox as mock_hackthebox


def test_box_list_active(runner):
    """Test `htb box list competitive`"""
    res = runner.invoke(cli, ["box", "list", "competitive"])
    assert len(res.output.split("\n")) == 21
    assert "Stacked" in res.output
    assert res.output.count("\uf091") == 20
    assert res.output.count("\uf7d0") == 9


def test_box_list_all(runner):
    """Test `htb box list all`"""
    res = runner.invoke(cli, ["box", "list", "all"])
    assert len(res.output.split("\n")) == 31
    assert res.output.count("\uf091") == 20
    assert res.output.count("\uf7d0") == 10


def test_box_list_todo(runner):
    """Test `htb box list todo --force-pager`"""
    res = runner.invoke(cli, ["box", "list", "todo", "--force-pager"])
    assert len(res.output.split("\n")) == 11
    assert res.output.count("\uf091") == 9
    assert res.output.count("\uf7d0") == 10


def test_box_list_unowned(runner):
    """Test `htb box list unowned --no-pager`"""
    res = runner.invoke(cli, ["box", "list", "unowned", "--no-pager"])
    assert len(res.output.split("\n")) == 13
    assert res.output.count("\uf091") == 11
    assert res.output.count("\uf7d0") == 9


# def test_box_list_from(runner):
#     """Test `htb box list from 0xdf`"""
#     res = runner.invoke(cli, ["box", "list", "from", "0xdf"])
#     assert len(res.output.splitlines()) == 3


def test_box_status(monkeypatch, runner):
    """Test `htb box status`, both with and without a current box"""
    res = runner.invoke(cli, ["box", "status"])
    assert "Acute" in res.output
    assert "RouterSpace" in res.output
    assert "10.10.11.145" in res.output
    assert "10.129.177.81" in res.output

    orig_func = hackthebox.HTBClient.get_active_machine
    monkeypatch.setattr(
        hackthebox.HTBClient,
        "get_active_machine",
        mock_hackthebox.mock_client.get_active_machine_none_alt,
    )
    res = runner.invoke(cli, ["box", "status"])
    assert (
        res.output == "[*] Current lab machine: None\n[*] Current RA machine:  None\n"
    )

    monkeypatch.setattr(hackthebox.HTBClient, "get_active_machine", orig_func)


def test_box_query(runner):
    """Test `htb box query` commands"""
    res = runner.invoke(cli, ["box", "query"])
    assert res.output.startswith("Usage: cli box")

    res = runner.invoke(cli, ["box", "query", "--todo", "--competitive", "--diff", "e"])
    assert len(res.output.split("\n")) == 4
    assert res.output.count("\uf091") == 3
    assert res.output.count("\uf7d0") == 3

    res = runner.invoke(
        cli, ["box", "query", "--todo", "--non-competitive", "--diff", "e"]
    )
    assert len(res.output.split("\n")) == 2
    assert res.output.count("\uf091") == 0
    assert res.output.count("\uf7d0") == 1
