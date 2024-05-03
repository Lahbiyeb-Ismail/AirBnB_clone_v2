#!/usr/bin/python3

"""
This script contains a function called `do_deploy` that deploys a compressed
archive to a web server. The archive is uploaded to the `/tmp/` directory of
the web server, then uncompressed to the folder
`/data/web_static/releases/<archive filename without extension>`. After
uncompressing, the script creates a symbolic link `/data/web_static/current`
that points to the new version of the code.

Usage:
  To use this script, call the `do_deploy` function and pass the path to the
  compressed archive as an argument.

Example:
  do_deploy('/path/to/archive.tar.gz')

Requirements:
  - The `fabric` library must be installed.
  - The web server must be configured to serve the code from the
    `/data/web_static/current` directory.

Returns:
  - Returns `True` if the deployment is successful.
  - Returns `False` if the deployment fails or the archive path does not exist.
"""

from fabric.api import env, put, run
import os

env.hosts = ['54.234.100.117', '35.153.79.92']


def do_deploy(archive_path):
    """
    This script contains a function called `do_deploy` that deploys a compress
    archive to a web server
    """
    if not os.path.exists(archive_path):
        return False

    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
    except Exception as e:
        print(e)
        return False

    return True
