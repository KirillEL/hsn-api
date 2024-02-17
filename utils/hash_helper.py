import hashlib
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from infra import config



class AESCipher:
    def __init__(self, key):
        self.key = key
        self.iv = os.urandom(16)

    def encrypt(self, field: str):
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(field.encode()) + padder.finalize()

        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=default_backend())
        encryptor = cipher.encryptor()

        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return ciphertext

    def decrypt(self, field: bytes):
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=default_backend())
        decryptor = cipher.decryptor()

        # Дешифруем данные
        decrypted_padded_data = decryptor.update(field) + decryptor.finalize()

        # Удаляем padding
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

        return decrypted_data.decode()


cipher = AESCipher(config.AES_KEY)
