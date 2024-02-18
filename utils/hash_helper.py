from cryptography.fernet import Fernet
from infra.config import config
import base64

class ContragentHasher:
    def __init__(self, key: bytes):
        self.fernet = Fernet(key)

    def encrypt(self, value: str) -> str:
        return self.fernet.encrypt(value.encode()).decode()

    def decrypt(self, value: str) -> str:
        return self.fernet.decrypt(value.encode()).decode()


contragent_hasher = ContragentHasher(config.KEY.encode())
