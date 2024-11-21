from typing import Optional

from cryptography.fernet import Fernet
from loguru import logger

import base64


class ContragentHasher:
    def __init__(self, key: bytes):
        self.fernet = Fernet(key)

    def encrypt(self, value: str) -> Optional[str]:
        if not value:
            return None
        return self.fernet.encrypt(value.encode()).decode()

    def decrypt(self, value: str) -> Optional[str]:
        if not value:
            return None
        return self.fernet.decrypt(value.encode()).decode()


from infra.config import config


contragent_hasher: ContragentHasher = ContragentHasher(config.KEY.encode())
