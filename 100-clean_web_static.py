#!/usr/bin/python3

"""
This script is used to clean up old releases of a web application deployed
on multiple servers.
It connects to the servers specified in the `env.hosts` list and deletes the
specified number of old releases.

Usage:
  python3 100-clean_web_static.py [number]

Arguments:
  number (optional): The number of old releases to keep. If not provided,
  all releases except the current one will be deleted.

Example:
  python3 100-clean_web_static.py 3
    - This will keep the 3 most recent releases and delete all others.

Note:
  - The script assumes that the web application is deployed in the
  '/data/web_static' directory on the remote servers.
  - The script requires the 'fabric' library to be installed.
"""

from fabric.api import *
from fabric.operations import run, put
import os

env.hosts = ['54.234.100.117', '35.153.79.92']


def do_clean(number=0):
    """
    Clean up old releases of the web application.

    Args:
      number (int, optional): The number of old releases to keep.
      If not provided, all releases except the current one will be deleted.

    Returns:
      None
    """
    number = 1 if int(number) == 0 else int(number)

    archives = sorted(os.listdir("versions"))
    [archives.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]
