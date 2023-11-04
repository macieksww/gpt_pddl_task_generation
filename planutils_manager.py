import os
import tarfile
import docker
import time
import gzip
import signal
import inspect
import sys
import copy
from io import BytesIO, TextIOWrapper, StringIO
from exceptions import TimeoutException, ExectionHandlers, DockerAPIException

def copy_to_docker_container(src, dst):
    function_name = copy.deepcopy(sys._getframe().f_code.co_name)
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
    timeout_const = 60
    signal.signal(signal.SIGALRM, ExectionHandlers.timeout_handler)
    signal.alarm(timeout_const)
    try:  
        container.put_archive('/root/', tarstream)
    except TimeoutError as e:
        print(e)
    except docker.errors.APIError as e:
        print(e)
    else:
        signal.alarm(0)  

def copy_from_docker_container(src):
    function_name = copy.deepcopy(sys._getframe().f_code.co_name)
    client = docker.from_env()
    filename = os.path.basename(src)
    container_name, _ = src.split(':')
    container = client.containers.get(container_name)
    timeout_const = 60
    signal.signal(signal.SIGALRM, ExectionHandlers.timeout_handler)
    signal.alarm(timeout_const)
    try:  
        bits, stat = container.get_archive('/root/planner_output.pddl')
    except TimeoutError as e:
        print(e)
    except docker.errors.APIError as e:
        print(e)
    else:
        signal.alarm(0) 
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
    function_name = copy.deepcopy(sys._getframe().f_code.co_name)
    timeout_const = 20
    signal.signal(signal.SIGALRM, ExectionHandlers.timeout_handler)
    signal.alarm(timeout_const)
    try:  
        client = docker.from_env()
    except TimeoutError as e:
        print(e)
    except docker.errors.APIError as e:
        print(e)
    else:
        signal.alarm(0)  
    container_name, _ = dst.split(':')
    signal.alarm(timeout_const)
    try: 
        container = client.containers.get(container_name)
        planner_exec_bash_cmd = 'bash exec_' + planner_type + '.bash'
        container.exec_run(['sh', '-c', planner_exec_bash_cmd])
    except TimeoutError as e:
        print(e)
    except docker.errors.APIError as e:
        print(e)
    else:
        signal.alarm(0)