from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from typing import Tuple

from fileshandler import FilesHandler

class Asymmetric:
    """
    Class that works with RSA algorithm
    """
    def __init__(self):
        self.public_key = None
        self.private_key = None

    def generate_asymmetric_keys(self) -> Tuple[rsa.RSAPublicKey, rsa.RSAPrivateKey]:
        """
        Generates a pair of public and private RSA keys
        :return: Tuple of public and private keys
        """
        keys = rsa.generate_private_key(
            public_exponent = 65537,
            key_size = 2048
        )
        self.private_key = keys
        self.public_key = keys.public_key()
        return self.public_key, self.private_key

    def serialization_public_key(self, save_path: str) -> None:
        """
        Serializes public key to the file
        :param save_path: Path to save the public key
        :return: None
        """
        FilesHandler.write_public_key(save_path, self.public_key)

    def serialization_private_key(self, save_path: str) -> None:
        """
        Serializes private key to the file
        :param save_path: Path to save the public key
        :return: None
        """
        FilesHandler.write_private_key(save_path, self.private_key)

    @staticmethod
    def deserialization_public_key(file_name: str) -> rsa.RSAPublicKey:
        """
        Deserializes public key from file
        :param file_name: Path to the file with public key
        :return: RSA public key
        """
        return FilesHandler.read_public_key(file_name)

    @staticmethod
    def deserialization_private_key(file_name: str) -> rsa.RSAPrivateKey:
        """
        Deserializes private key from file
        :param file_name: Path to the file with private key
        :return: RSA private key
        """
        return FilesHandler.read_private_key(file_name)

    def encrypt_symmetric_key(self, path_public: str, symmetric_key: bytes, save_path: str) -> bytes:
        """
        Encrypts key of symmetric cipher algorithm with RSA algorithm
        :param path_public: Path to the RSA public key
        :param symmetric_key: Symmetric key as bytes object
        :param save_path: Path to save encrypted key
        :return: None
        """
        public_key = self.deserialization_public_key(path_public)
        c_text = public_key.encrypt(symmetric_key, padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(), label=None
            )
        )
        FilesHandler.write_bytes(save_path, c_text)
        return c_text

    def decrypt_symmetric_key(self, path_private: str, path_encrypted: str) -> bytes:
        """
        Decrypts symmetric algo key encrypted with RSA algorithm
        :param path_private: Path to the RSA private key
        :param path_encrypted: Path to the encrypted key
        :return: None
        """
        private_key = self.deserialization_private_key(path_private)
        encrypted_sym_key = FilesHandler.get_bytes(path_encrypted)
        dc_text = private_key.decrypt(encrypted_sym_key,
                                      padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                   algorithm=hashes.SHA256(), label=None))

        return dc_text

