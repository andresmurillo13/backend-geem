class IpRequest:
    _instance = None
    _ip = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def set_ip(self, ip):
        self._ip = ip

    def get_ip(self):
        return self._ip
