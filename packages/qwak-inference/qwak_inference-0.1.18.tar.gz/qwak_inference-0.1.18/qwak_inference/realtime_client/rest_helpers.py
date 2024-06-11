import socket
from dataclasses import dataclass
from datetime import datetime

import requests

from qwak_inference.configuration import AuthClient
from qwak_inference.configuration.account import UserAccountConfiguration


def _get_authorization():
    user_account_configuration = UserAccountConfiguration()
    auth_client = AuthClient(api_key=user_account_configuration.get_user_apikey())

    return f"Bearer {auth_client.get_token()}", auth_client.token_expiration()


@dataclass
class SocketConfiguration:
    tcp_keepalive: bool = True
    tcp_keepidle: int = 120
    tcp_keepintvl: int = 75
    tcp_keepcnt: int = 9


class SocketAdapter(requests.adapters.HTTPAdapter):
    def __init__(self, *args, socket_params=None, **kwargs):
        self.socket_params = socket_params
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        if self.socket_params:
            kwargs["socket_options"] = self.socket_params
        super().init_poolmanager(*args, **kwargs)


# Configure only TCP attributes that are available in the OS
def validate_socket_config(socket_options):
    config = []
    for line in socket_options:
        if hasattr(socket, line[0]) and hasattr(socket, line[1]):
            config.append((getattr(socket, line[0]), getattr(socket, line[1]), line[2]))
    return config


class RestSession(requests.Session):
    def __init__(self, socket_configuration=SocketConfiguration()):
        super().__init__()
        self.headers.update({"Content-Type": "application/json"})
        socket_options = [
            ("SOL_SOCKET", "SO_KEEPALIVE", int(socket_configuration.tcp_keepalive)),
            ("SOL_TCP", "TCP_KEEPIDLE", socket_configuration.tcp_keepidle),
            ("SOL_TCP", "TCP_KEEPINTVL", socket_configuration.tcp_keepintvl),
            ("SOL_TCP", "TCP_KEEPCNT", socket_configuration.tcp_keepcnt),
        ]
        socket_options = validate_socket_config(socket_options)
        adapter = SocketAdapter(socket_params=socket_options)
        self.mount("https://", adapter)
        self.mount("http://", adapter)

    def prepare_request(self, request):
        if "Authorization" not in self.headers:
            (
                self.headers["Authorization"],
                self.jwt_expiration,
            ) = _get_authorization()
        else:
            if self.jwt_expiration <= datetime.utcnow():
                (
                    self.headers["Authorization"],
                    self.jwt_expiration,
                ) = _get_authorization()

        return super().prepare_request(request)
