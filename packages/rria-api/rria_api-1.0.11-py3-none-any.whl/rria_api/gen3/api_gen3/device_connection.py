from kortex_api.RouterClient import RouterClient, RouterClientSendOptions
from kortex_api.SessionManager import SessionManager
from kortex_api.autogen.messages import Session_pb2
from kortex_api.TCPTransport import TCPTransport


class DeviceConnection:
    TCP_PORT = 10000

    def __init__(self, ip_address, port=TCP_PORT, credentials=("", "")):
        self.ip_address = ip_address
        self.port = port
        self.credentials = credentials

        self.sessionManager = None

        # Setup API
        self.transport = TCPTransport()
        self.router = RouterClient(self.transport, RouterClient.basicErrorCallback)

    def connect(self):
        self.transport.connect(self.ip_address, self.port)

        session_info = Session_pb2.CreateSessionInfo()
        session_info.username = self.credentials[0]
        session_info.password = self.credentials[1]
        session_info.session_inactivity_timeout = 10000  # (milliseconds)
        session_info.connection_inactivity_timeout = 2000  # (milliseconds)

        self.sessionManager = SessionManager(self.router)
        print("Logging as", self.credentials[0], "on device", self.ip_address)
        self.sessionManager.CreateSession(session_info)

        return self.router

    def disconnect(self):
        if self.sessionManager is not None:
            router_options = RouterClientSendOptions()
            router_options.timeout_ms = 1000

            self.sessionManager.CloseSession(router_options)

        self.transport.disconnect()
