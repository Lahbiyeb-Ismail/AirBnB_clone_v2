#!/usr/bin/python3
"""
Fabric script based on the file 2-do_deploy_web_static.py that creates and
distributes an archive to the web servers

execute: fab -f 3-deploy_web_static.py deploy -i ~/.ssh/id_rsa -u ubuntu
"""

from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists, isdir
env.hosts = ['54.160.77.90', '10.25.190.21']


def do_pack():
    """generates a tgz archive"""
    date = datetime.now().strftime("%Y%m%d%H%M%S")

    if isdir("versions") is False:
        local("mkdir versions")

    file = "versions/web_static_{}.tgz".format(date)

    if local("tar -cvzf {} web_static".format(file)).failed is True:
        return None

    return file


def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if exists(archive_path) is False:
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
