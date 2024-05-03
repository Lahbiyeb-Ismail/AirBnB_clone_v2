#!/usr/bin/python3
"""
Fabric script based on the file 2-do_deploy_web_static.py that creates and
distributes an archive to the web servers

execute: fab -f 3-deploy_web_static.py deploy -i ~/.ssh/id_rsa -u ubuntu
"""

from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists, makedirs
env.hosts = ['54.160.77.90', '10.25.190.21']


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder"""
    # Create the versions folder if it doesn't exist
    if not exists("versions"):
        makedirs("versions")

    # Create the archive path
    now = datetime.now()
    time_format = now.strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(time_format)

    # Compress the web_static folder into the archive
    compress_file = local("tar -czvf {} web_static".format(archive_path))

    if compress_file is not None:
        return archive_path

    return None


def do_deploy(archive_path):
    """
    This script contains a function called `do_deploy` that deploys a compress
    archive to a web server
    """
    if not exists(archive_path):
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


def deploy():
    """creates and distributes an archive to the web servers"""
    archive_path = do_pack()

    if archive_path is None:
        return False

    return do_deploy(archive_path)
