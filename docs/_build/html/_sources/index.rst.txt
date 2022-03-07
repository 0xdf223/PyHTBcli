.. HTBCli documentation master file, created by
   sphinx-quickstart on Mon Mar  7 14:33:22 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PyHTBcli
==================================
``PyHTBcli`` is a Python command line interface for interacting with HackTheBox.

Installation
------------

Requirements
^^^^^^^^^^^^

Make sure ``nmcli`` is installed. Present on most Linux distros. Install with ``apt install network-manager``.

To make fonts print nicely, need a Nerd Font. Install::

    wget https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/Ubuntu.zip -O /tmp/Ubuntu.zip
    mkdir -p ~/.local/share/fonts
    unzip /tmp/Ubuntu.zip -d ~/.local/share/fonts
    fc-cache -fv

Install PyHTBcli
^^^^^^^^^^^^^^^^

``pip install pyHTBcli``

Running
-------

HTBShell
^^^^^^^^

From the command line, run ``htb``::

    $ htb
    
                .-⁻⁻-._
            .-⁻`        `⁻-.
        .-⁻`                `⁻-_   __  __  ______  ____            ___
        |`⁻-.                 .-|/\ \/\ \/\__  _\/\  _`\         /\_ \   __
        |    `⁻-.         .-⁻`  |\ \ \_\ \/_/\ \/\ \ \L\ \    ___\//\ \ /\_\
        |        `⁻-...-⁻`      | \ \  _  \ \ \ \ \ \  _ <'  /'___\\ \ \\/\ \
        |            |          |  \ \ \ \ \ \ \ \ \ \ \L\ \/\ \__/ \_\ \\ \ \
        |            |          |   \ \_\ \_\ \ \_\ \ \____/\ \____\/\____\ \_\
        |            |          |    \/_/\/_/  \/_/  \/___/  \/____/\/____/\/_/
        `⁻-.         |       .-`
            `⁻-.     |   .-⁻`
                `⁻-..|-⁻`
    
    HackTheBox> help
    
    Documented commands (type help <topic>):
    ========================================
    box  status  version  vpn
    
    Undocumented commands:
    ======================
    exit  help  quit
 

Single Commands
^^^^^^^^^^^^^^^

Single commands can be giving from the command line as well::

    $ htb -h
    Usage: htb [OPTIONS] COMMAND [ARGS]...
    
      HackTheBox Shell
    
    Options:
      --cache-cred [None|Short|Long]  Cache access token and refresh token. Short
                                      tokens are valid for 1 day, Long for 30
                                      days.
      --cache-location PATH           Location of file that stores the cached
                                      credential.
      -h, --help                      Show this message and exit.
    
    Commands:
      box      Information and interaction with Boxes
      status   Print comprehensive status
      version  Get the library version.
      vpn      VPN Connection Commands


.. toctree::
   :maxdepth: 2
   :caption: Contents:


Command Index
-------------

.. toctree::
   :maxdepth: 3
   :glob:

   box
   vpn
