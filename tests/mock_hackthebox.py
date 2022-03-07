from distutils.spawn import spawn
from platform import machine
from hackthebox import Machine, MachineInstance, VPNServer, HTBClient, Search, User
from hackthebox.errors import (
    NotFoundException,
    CannotSwitchWithActive,
    IncorrectFlagException,
)
from mock_data import *


class mock_client(HTBClient):
    def __init__(
        self,
        email=None,
        password=None,
        otp=None,
        cache=None,
        api_base="",
        remember=False,
        app_token=None,
    ):
        if not cache:
            print("Email: ")
            input()
            print("Password: ")
            input()

    def do_login(
        self,
        email=None,
        password=None,
        otp=None,
        remember=False,
        app_token=None,
    ):
        assert False

    def do_request(
        self,
        endpoint,
        json_data=None,
        data=None,
        authorized=True,
        download=False,
        post=False,
    ):
        print("Tried to call do_request")

    def get_machines(self, retired=False):

        if retired:
            data = GET_MACHINES_DATA_RETIRED
        else:
            data = GET_MACHINES_DATA
        machines = [Machine(m, self, summary=True) for m in data]
        for machine in machines:
            machine.retired = retired
        return machines

    def get_todo_machines(self):
        return GET_TODO_MACHINES_IDS

    def get_active_machine(self, release_arena=False):
        """Returns an active machine"""
        if release_arena:
            active_id = 444
        else:
            active_id = 438
        box = self.get_machine(active_id)
        server = self.get_current_vpn_server(release_arena=release_arena)
        return MachineInstance(box.ip, server, box, self)

    def get_active_machine_none_alt(self, release_arena=False):
        """Returns no active machine"""
        return None

    def get_machine(self, machine_id):
        box = None
        if machine_id == 438 or str(machine_id).lower() == "acute":
            box = Machine(GET_MACHINE_DATA_ACUTE, self)
            box._is_release = False
        elif machine_id == 444 or str(machine_id).lower() == "routerspace":
            box = Machine(GET_MACHINE_DATA_ROUTERSPACE_RA, self)
            box._is_release = True
        elif machine_id == 443 or str(machine_id).lower() == "steamcloud":
            box = Machine(GET_MACHINE_DATA_STEAMCLOUD, self)
            box._is_release = False

        if box:
            return box
        raise NotFoundException

    def get_current_vpn_server(self, release_arena=False):
        connections = GET_CURRENT_VPN_SERVER_DATA
        if release_arena:
            if "assigned_server" not in connections["release_arena"]:
                return None
            data = connections["release_arena"]["assigned_server"]
        else:
            if "assigned_server" not in connections["lab"]:
                return None
            data = connections["lab"]["assigned_server"]
        return VPNServer(data, self)

    def get_all_vpn_servers(self, release_arena=False):
        if release_arena:
            data = GET_ALL_RA_VPN_SERVER_DATA
        else:
            data = GET_ALL_VPN_SERVER_DATA
        servers = []
        for location in data.keys():  # 'EU'
            for location_role in data[location].keys():  # 'EU - Free'
                for server in data[location][location_role]["servers"].values():
                    servers.append(VPNServer(server, self))
        return servers

    def get_all_vpn_servers_none_alt(self, release_arena=False):
        return []

    def search(self, search_term: str) -> "Search":
        return Search("0xdf", self)

    def get_user(self, user_id: int) -> "User":
        # this may not work
        return User(USER_0xdf, self)


box_to_ip = {"SteamCloud": ""}


class mock_machine:
    def spawn(self, release_arena=False) -> "MachineInstance":
        if release_arena:
            ip = self.ip
            server = self._client.get_current_vpn_server(release_arena=True)
        else:
            ip = self.ip
            server = self._client.get_current_vpn_server()
        return MachineInstance(ip, server, self, self._client)

    def spawn_too_many_alt(self, release_arena=False) -> "MachineInstance":
        raise Exception(
            f"Failed to spawn: You need to wait 2 minutes before spawning another machine."
        )

    def submit(self, flag: str, difficulty: int):
        if flag == "3a0478e0e11a50592b9799fb7d357483":
            return True
        raise IncorrectFlagException


class mock_machine_instance:
    def stop(self):
        pass

    def reset(self):
        pass


class mock_vpn_server(VPNServer):
    def download(self, path=None, tcp=False) -> str:
        pass

    def switch(self):
        return True

    def switch_fail_alt(self):
        return False

    def switch_raise_alt(self):
        raise CannotSwitchWithActive


class mock_search(Search):
    def __init__(self, search: str, client: HTBClient, _tags=None):
        if _tags is None:
            _tags = []
        self._term = search
        self._client = client
        # Ignoring tags - they seem to currently not work on the API level
        search_data = SEARCH_OXDF
        self._user_ids = [x["id"] for x in search_data.get("users", [])]
        self._machine_ids = [x["id"] for x in search_data.get("machines", [])]
        self._team_ids = [x["id"] for x in search_data.get("teams", [])]
        self._challenge_ids = [x["id"] for x in search_data.get("challenges", [])]
