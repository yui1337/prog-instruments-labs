from crypto.asymmetric import Asymmetric
from crypto.symmetric import Symmetric

class Hybrid:
    """
    Class that works with both CAST5 and RSA algos. More like interface.
    """
    def __init__(self, key_length=128):
        self.symmetric = Symmetric()
        self.asymmetric = Asymmetric()
        self.key_len = key_length

    def generate_keys(self,
                      public_path: str,
                      private_path: str,
                      symmetric_path: str) -> None:
        """
        Generates keys for both asymmetric and symmetric algorithms,
        encrypts symmetric key with RSA and saves it to the
        given path.
        :param public_path: Path to save the RSA public key
        :param private_path: Path to save the RSA private key
        :param symmetric_path: Path to save the encrypted symmetric key
        :return: None
        """
        self.asymmetric.generate_asymmetric_keys()
        self.asymmetric.serialization_public_key(public_path)
        self.asymmetric.serialization_private_key(private_path)
        self.symmetric.generate_key(self.key_len)
        self.symmetric.key = self.asymmetric.encrypt_symmetric_key(public_path, self.symmetric.key, symmetric_path)
        self.symmetric.serialization_symmetric_key(symmetric_path)


    def encrypt_data(self,
                     file_name: str,
                     private_path: str,
                     encrypted_path: str,
                     save_path: str) -> None:
        """
        Encrypts data
        :param file_name: Path with plain data
        :param private_path: Path to the private key
        :param encrypted_path: Path to the encrypted symmetric algo key
        :param save_path: Path to save the encrypted data
        :return: None
        """
        self.symmetric.key = self.asymmetric.decrypt_symmetric_key(private_path, encrypted_path)
        self.symmetric.encrypt_text(file_name, save_path)

    def decrypt_data(self,
                     encrypted_file_path: str,
                     private_path: str,
                     encrypted_key_path: str,
                     save_path: str) -> None:
        """
        Decrypts data
        :param encrypted_file_path: Path to the encrypted data
        :param private_path: Path to the private key
        :param encrypted_key_path: Path to the encrypted symmetric algo key
        :param save_path: Path to save the encrypted data
        :return: None
        """
        self.symmetric.key = self.asymmetric.decrypt_symmetric_key(private_path, encrypted_key_path)
        self.symmetric.decrypt_text(encrypted_file_path, save_path)

