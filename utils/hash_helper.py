from typing import Optional

from cryptography.fernet import Fernet
from infra.config import config


class ContragentHasher:
    def __init__(self, key: bytes) -> None:
        self.fernet = Fernet(key)

    def encrypt(self, value: str) -> Optional[str]:
        if not value:
            return None
        return self.fernet.encrypt(value.encode()).decode()

    def decrypt(self, value: str) -> Optional[str]:
        if not value:
            return None
        return self.fernet.decrypt(value.encode()).decode()


contragent_hasher = ContragentHasher(config.KEY.encode())
