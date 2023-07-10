import os
import tarfile
import docker
import time
import gzip
from io import BytesIO, TextIOWrapper, StringIO

def copy_to_docker_container(src, dst):
    client = docker.from_env()
    filename = os.path.basename(src)
    container_name, _ = dst.split(':')
    container = client.containers.get(container_name)
    with open(src, "rb") as file:
        data = file.read()
        bytesIO_data = BytesIO(data)
    tarstream = BytesIO()
    tar = tarfile.TarFile(fileobj=tarstream, mode='w')
    tarinfo = tarfile.TarInfo(name=filename)
    tarinfo.size = len(data)
    tarinfo.mtime = time.time()
    tar.addfile(tarinfo, bytesIO_data)
    tar.close()
    tarstream.seek(0)
    container.put_archive('/root/', tarstream)

def copy_from_docker_container(src):
    client = docker.from_env()
    filename = os.path.basename(src)
    container_name, _ = src.split(':')
    container = client.containers.get(container_name)
    bits, stat = container.get_archive('/root/planner_output.pddl')
    file_obj = BytesIO()
    for i in bits:
        file_obj.write(i)
    file_obj.seek(0)
    tar = tarfile.open(mode='r', fileobj=file_obj)
    text = tar.extractfile('planner_output.pddl')
    text = text.read().decode()
    with open('gpt_generated_files/planner_output.pddl', 'w+') as f:
        f.write(text)

def execute_planner(dst, planner_type):
    client = docker.from_env()
    container_name, _ = dst.split(':')
    container = client.containers.get(container_name)
    planner_exec_bash_cmd = 'bash exec_' + planner_type + '.bash'
    container.exec_run(['sh', '-c', planner_exec_bash_cmd])

# src = 'crazy_yalow:/'
# dst = 'gpt_generated_files/planner_output.pddl'

# copy_from_docker_container(src)
