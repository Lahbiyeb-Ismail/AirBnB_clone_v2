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
    number = int(number)

    if number < 0:
        number = 0
    elif number == 1:
        number = 2

    with cd('/data/web_static/releases'):
        releases = run('ls -1t').split('\n')
        to_delete = releases[number:]
        for release in to_delete:
            run('rm -rf {}'.format(release))

    with cd('/data/web_static/current'):
        current_release = run('ls -l | grep web_static | awk \'{print $11}\'')
        current_release = os.path.basename(current_release)
        releases = run('ls -1t ../releases').split('\n')
        to_delete = releases[number:]

        for release in to_delete:
            if release != current_release:
                run('rm -rf ../releases/{}'.format(release))
