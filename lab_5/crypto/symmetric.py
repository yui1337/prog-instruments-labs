import os

from cryptography.hazmat.decrepit.ciphers import algorithms
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, modes

from fileshandler import FilesHandler


class Symmetric:
    """
    Class that handles CAST5 cipher algorithm.
    """
    def __init__(self):
        self.key = None

    def generate_key(self, key_len: int) -> None:
        """
        Generates random key with given length (key_len in bits, self.key in bytes).
        :param key_len: Length of key in bits
        :return: None
        """
        if not(40 <= key_len <= 128):
            raise ValueError("Wrong key length!")
        self.key = os.urandom(key_len // 8)

    def serialization_symmetric_key(self, save_path: str) -> None:
        """
        Writes key to the file.
        :param save_path: Path to save the key
        :return: None
        """
        FilesHandler.write_bytes(save_path, self.key)

    def deserialization_symmetric_key(self, file_name: str) -> bytes:
        """
        Reads key from the file.
        :param file_name: Path to the file with key
        :return: None
        """
        self.key = FilesHandler.get_bytes(file_name)
        return FilesHandler.get_bytes(file_name)

    def encrypt_text(self, file_name: str, save_path: str) -> None:
        """
        Encrypts text using CAST5 algorithm and saves encrypted
        text to the file.
        :param file_name: Path to file with plain text
        :param save_path: Path to save encrypted text
        :return: None
        """
        text = FilesHandler.get_bytes(file_name)
        padder = padding.PKCS7(64).padder()
        padded_text = padder.update(text) + padder.finalize()
        iv = os.urandom(8)
        cipher = Cipher(algorithms.CAST5(self.key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        c_text = encryptor.update(padded_text) + encryptor.finalize()
        c_text = iv + c_text
        FilesHandler.write_bytes(save_path, c_text)


    def decrypt_text(self, encrypted_path: str, save_path: str) -> str:
        """
        Decrypts text, that encrypted using CAST5 algorithm, and
        saves it to the file
        :param encrypted_path: Path to the file with encrypted text
        :param save_path: Path so save file with decrypted text
        :return: Decrypted text
        """
        encrypted_text = FilesHandler.get_bytes(encrypted_path)
        iv = encrypted_text[:8]
        cipher = Cipher(algorithms.CAST5(self.key), modes.CBC(iv))
        encrypted_text = encrypted_text[8:]
        decryptor = cipher.decryptor()
        decrypted_text = decryptor.update(encrypted_text) + decryptor.finalize()
        unpadder = padding.PKCS7(64).unpadder()
        unpadder_dc_text = unpadder.update(decrypted_text) + unpadder.finalize()
        FilesHandler.write_txt(save_path, unpadder_dc_text.decode('UTF-8'))

        return unpadder_dc_text.decode('UTF-8')

