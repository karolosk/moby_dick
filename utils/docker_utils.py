from services.moby_dick_docker import docker_low_level_client


def get_container_cpu_percent(container_name):
    return round(calculate_cpu_percent(get_container_stats(container_name)), 2)


def get_container_memory_usage(container_name):
    return humanize_bytes(get_container_stats(container_name)['memory_stats']['usage'])


def get_container_memory_max_usage(container_name):
    return humanize_bytes(get_container_stats(container_name)['memory_stats']['max_usage'])


def get_container_stats(container_name, stream=False):
    return docker_low_level_client.stats(container=container_name, stream=stream)


# As provided from docker package
def calculate_cpu_percent(client):
    cpu_count = len(client["cpu_stats"]["cpu_usage"]["percpu_usage"])
    cpu_percent = 0.0
    cpu_delta = float(client["cpu_stats"]["cpu_usage"]["total_usage"]) - float(client["precpu_stats"]["cpu_usage"]["total_usage"])
    system_delta = float(client["cpu_stats"]["system_cpu_usage"]) - float(client["precpu_stats"]["system_cpu_usage"])
    if system_delta > 0.0:
        cpu_percent = cpu_delta / system_delta * 100.0 * cpu_count
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

    if '5000/tcp' in port_data.keys():
        # if 'graylog' not in port_data2['Name']:
        host_ip = port_data['5000/tcp'][0]['HostIp']
        host_port = port_data['5000/tcp'][0]['HostPort']
        return {"host_ip": host_ip, "host_port": host_port}
    return {"host_ip": "n/a", "host_port": "n/a"}


def retrive_containert_state_data(container_id):
    container_state = docker_low_level_client.inspect_container(container_id)['State']
    status = container_state['Status']
    running = container_state['Running']
    return {"status": status, "running": running}
