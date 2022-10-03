from models.container import ContainerModel
from utils import docker_utils
from services.moby_dick_docker import docker_client, docker_low_level_client
from config import host_config as hc


def retrieve_containers():
    cont_list = []
    for container in docker_client.containers.list(all=True):
        cont = ContainerModel()

        cont.name = container.name
        cont.status = container.status
        cont.short_id = container.short_id
        cont.cpu_usage = set_cpu_percent(cont.name, cont.status)
        cont.memory_usage = set_memory_usage(cont.name, cont.status)
        cont.memory_percent = set_memory_percent(cont.name, cont.status)
        cont.host = set_host(cont.status, container.id)
        cont_list.append(cont.to_json())

    return cont_list


# Method to run container currently runs for a specific image.
# Used the low level client in order to be able to setup the logging configuration.
# SDK does not seem to provide this option at the moment or I missed it :)
def run_container():
    new_container = docker_low_level_client.create_container("fk", ports=[5000], host_config=hc.host_configuration)
    new_container_id = new_container.get('Id')
    docker_low_level_client.start(new_container_id)
    return {"created": "OK", "info": retrieve_container_info_by_id(new_container_id)}


def start_container(id):
    docker_low_level_client.start(id)
    return {"created": "OK", "info": retrieve_container_info_by_id(id)}


def stop_container(id):
    container = docker_client.containers.get(id)
    container.stop()
    return {"created": "OK"}


def remove_container(id):
    container = docker_client.containers.get(id)
    container.remove()
    return {"created": "OK"}


def retrieve_container_info_by_id(container_id):
    host = docker_utils.retrieve_container_host_data(container_id)
    state = docker_utils.retrieve_container_state_data(container_id)
    return {"host": host, "state": state}


### Helpers ###

# Have to check the status for each of those setters. In the case a container is not running the dictionary keys cannot be found
# and this is light way to handle it
def set_cpu_percent(container_name, status):
    if status == "running":
        return str(docker_utils.get_container_cpu_percent(container_name)) + "%"
    return "n/a"


def set_memory_usage(container_name, status):
    if status == "running":
        return str(docker_utils.get_container_memory_usage(container_name))
    return "n/a"


def set_memory_percent(container_name, status):
    if status == "running":
        return str(docker_utils.get_container_memory_percent(container_name)) + "%"
    return "n/a"


def set_host(status, id):
    if status == "running":
        host = docker_utils.retrieve_container_host_data(id)
        return host['host_ip'] + ":" + host['host_port']
    return "n/a"
