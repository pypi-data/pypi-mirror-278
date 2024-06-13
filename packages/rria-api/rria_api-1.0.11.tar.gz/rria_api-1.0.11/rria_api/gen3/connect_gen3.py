from rria_api.gen3.api_gen3.device_connection import DeviceConnection


class ConnectGen3:
    route = None

    def __init__(self, ip_address, credentials):
        self.ip_address = ip_address
        self.credentials = credentials

        self.connect_instance = DeviceConnection(ip_address=self.ip_address,
                                                 credentials=(credentials[0], credentials[1]))

    def connect_robot(self):
        self.route = self.connect_instance.connect()

        return self.route

    def disconnect_robot(self):
        self.connect_instance = self.connect_instance.disconnect()
