from services.moby_dick_docker import docker_low_level_client


def get_container_cpu_percent(container_name):
    return round(calculate_cpu_percent(get_container_stats(container_name)), 2)


def get_container_memory_usage(container_name):
    return humanize_bytes(get_container_stats(container_name)['memory_stats']['usage'])


def get_container_memory_percent(container_name):
    stats = get_container_stats(container_name)
    limit = stats.get('memory_stats').get('limit')
    usage = stats.get('memory_stats').get('usage')
    return round(usage / limit * 100.0, 2)


def get_container_stats(container_name, stream=False):
    return docker_low_level_client.stats(container=container_name, stream=stream)


# CONTAINER ID   NAME      CPU %     MEM USAGE / LIMIT     MEM %     NET I/O         BLOCK I/O        PIDS
# e2f60fd66af9   sql1      2.10%     1.356GiB / 15.32GiB   8.85%     1.8MB / 370kB   1.2GB / 45.4MB   225

# As provided from docker package
def calculate_cpu_percent(client):

    cpu_percent = 0.0
    cpu_delta = float(client.get('cpu_stats').get('cpu_usage').get('total_usage')) - float(
        client.get('precpu_stats').get('cpu_usage').get('total_usage'))
    system_delta = float(client.get('cpu_stats').get('system_cpu_usage')) - float(client.get('precpu_stats').get('system_cpu_usage'))
    if system_delta > 0.0:
        cpu_percent = cpu_delta / system_delta * 100.0
    return cpu_percent


# As provided from docker package
def humanize_bytes(bytesize, precision=2):
    """
    Humanize byte size figures
    https://gist.github.com/moird/3684595
    """
    abbrevs = (
        (1 << 50, 'PB'),
        (1 << 40, 'TB'),
        (1 << 30, 'GB'),
        (1 << 20, 'MB'),
        (1 << 10, 'kB'),
        (1, 'bytes')
    )
    if bytesize == 1:
        return '1 byte'
    for factor, suffix in abbrevs:
        if bytesize >= factor:
            break
    if factor == 1:
        precision = 0
    return '%.*f %s' % (precision, bytesize / float(factor), suffix)


def retrieve_container_host_data(container_id):
    port_data = docker_low_level_client.inspect_container(container_id)['NetworkSettings']['Ports']

    for key in port_data.keys():
        if 'tcp' in key:
            host_ip = port_data.get(key)[0]['HostIp']
            host_port = port_data.get(key)[0]['HostPort']
            return {"host_ip": host_ip, "host_port": host_port}

    return {"host_ip": "n/a", "host_port": "n/a"}


def retrieve_container_state_data(container_id):
    container_state = docker_low_level_client.inspect_container(container_id)['State']
    status = container_state['Status']
    running = container_state['Running']
    return {"status": status, "running": running}
