"""VPN utility functions"""


def format_name(name: str) -> str:
    """Format the name of the VPN server"""
    return name.lower().replace(" ", "-")
