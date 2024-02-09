import hashlib


class HashHelper:
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha1(password.encode()).hexdigest()

