import docker

docker_client = docker.from_env()
docker_low_level_client = docker.APIClient(base_url='unix://var/run/docker.sock')