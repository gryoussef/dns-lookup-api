import os
import socket
from pydantic import IPvAnyAddress
from abc import ABC, abstractmethod
from typing import List

class IUtils(ABC):
    @abstractmethod
    def is_running_in_kubernetes(self) -> bool:
        pass

    @abstractmethod
    def get_ip_addresses(self, domain: str) -> List[str]:
        pass

    @abstractmethod
    def is_valid_ip(self, ip: str) -> bool:
        pass

class Utils(IUtils):
    def is_running_in_kubernetes(self) -> bool:
        return os.path.exists("/var/run/secrets/kubernetes.io")

    def get_ip_addresses(self, domain: str):
        return socket.gethostbyname_ex(domain)[2]

    def is_valid_ip(self, ip: str):
        try:
            IPvAnyAddress(ip)
            return True
        except ValueError:
            return False