class ContainerModel(object):

    # Initialize with default values in order to be used as default constructor on the same time
    def __init__(self, status="", short_id="", name="", cpu_usage="", memory_usage="", memory_percent="", host=""):
        self.status = status
        self.short_id = short_id
        self.name = name
        self.cpu_usage = cpu_usage
        self.memory_usage = memory_usage
        self.memory_percent = memory_percent
        self.host = host

    def to_json(self):
        return {
            "status": self.status,
            "short_id": self.short_id,
            "name": self.name,
            "cpu_usage": self.cpu_usage,
            "memory_usage": self.memory_usage,
            "memory_percent": self.memory_percent,
            "host": self.host
        }

