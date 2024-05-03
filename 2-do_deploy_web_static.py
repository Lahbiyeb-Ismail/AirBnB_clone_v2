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
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Get the filename without extension
        file_n = os.path.basename(archive_path)
        file_no_ext = os.path.splitext(file_n)[0]

        # Uncompress the archive to the folder
        # /data/web_static/releases/<archive
        # filename without extension> on the web server
        run('mkdir -p /data/web_static/releases/{}'.format(file_no_ext))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}\
          '.format(file_n, file_no_ext))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(file_n))

        # Delete the symbolic link /data/web_static/current from the web server
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link /data/web_static/current on the
        # web server, linked to the new version of your code
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current\
          '.format(file_no_ext))

        return True
    except:
        return False
