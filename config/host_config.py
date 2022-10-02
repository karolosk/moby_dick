from docker.types import LogConfig
import docker
from services.moby_dick_docker import docker_low_level_client

log_configuration = LogConfig(type=LogConfig.types.GELF, config={
        "gelf-address": "udp://127.0.0.1:12201"
})

host_configuration = docker_low_level_client.create_host_config(log_config=log_configuration, port_bindings={
        5000: None
})