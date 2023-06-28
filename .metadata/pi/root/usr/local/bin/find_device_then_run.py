#!/usr/bin/env python3

# This file is generated automatically from metadata
# File edits may be overwritten!

import os
import click
import docker
from pathlib import Path
import filelock

lock_path = 'docker_controller.lock'
lock = filelock.FileLock(lock_path, timeout=1)

class DockerController(object):

    def __init__(self,dry_run,*args,**kwargs):
        self.dry_run = dry_run
        self.client = docker.from_env()

    def _run(self,**kwargs):
        if not self.dry_run:
            self.client.containers.run(**kwargs)
        else:
            for key,value in kwargs.items():
                print('docker run')
                print(key,value)

    def stop_all(self):
        for container in self.client.containers.list():
            if not self.dry_run:
                container.stop()
            else:
                print('docker stop {0}'.format(container.name))

    def run(self):
        image = 'weigher:humble'
        command = ['ros2','launch','weigher','weigher_launch.py']
        detach = True
        devs = sorted(Path('/dev').glob('ttyUSB*'))
        devices = ['{0}:{0}'.format(dev) for dev in devs]
        network_mode = 'host'
        pid_mode = 'host'
        restart_policy = {'Name':'on-failure', "MaximumRetryCount": 5}
        volumes = {'/dev':{'bind':'/dev'}}
        self._run(image=image,
                  command=command,
                  detach=detach,
                  devices=devices,
                  network_mode=network_mode,
                  pid_mode=pid_mode,
                  restart_policy=restart_policy,
                  volumes=volumes)

@click.command()
@click.option('-d','--dry-run', is_flag=True)
def cli(dry_run):
    try:
        with lock.acquire(timeout=1):
            if dry_run:
                print('Dry Run')
            docker_controller = DockerController(dry_run)
            docker_controller.stop_all()
            docker_controller.run()
    except filelock.Timeout:
        print('Another instance of find_device_then_run currently holds the lock')

# -----------------------------------------------------------------------------------------
if __name__ == '__main__':
    cli()
