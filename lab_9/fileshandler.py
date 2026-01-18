import json

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key


class FilesHandler:

    @staticmethod
    def get_bytes(file_name: str) -> bytes:
        """
        Reads data in bytes format from the file
        :param file_name: Path to the file
        :return: Bytes format object
        """
        try:
            with open(file_name, 'rb') as file:
                data = file.read()
            return data
        except FileNotFoundError:
            print(f"The file was not found.")
        except Exception as e:
            print(f"An error occurred while reading the file: {str(e)}.")

    @staticmethod
    def write_bytes(save_path: str, data: bytes) -> None:
        """
        Writes data to the file from bytes
        :param save_path: Path to save the file
        :param data: Data to save
        :return: None
        """
        try:
            with open(save_path, mode='wb') as file:
                file.write(data)
        except FileNotFoundError:
            print(f"The file was not found.")
        except Exception as e:
            print(f"An error occurred while writing the file: {str(e)}.")

    @staticmethod
    def get_txt(file_name: str) -> str:
        """
        Reads text from the file
        :param file_name: Path to the file
        :return: Text from the file
        """
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"The file was not found.")
        except Exception as e:
            print(f"An error occurred while reading the file: {str(e)}.")

    @staticmethod
    def write_txt(save_path: str, text: str) -> None:
        """
        Writes text to file
        :param save_path: Path to save the file
        :param text: Text to save
        :return: None
        """
        try:
            with open(save_path, 'w') as file:
                file.write(text)
        except FileNotFoundError:
            print(f"The file was not found.")
        except Exception as e:
            print(f"An error occurred while writing the file: {str(e)}.")

    @staticmethod
    def get_json(file_name: str) -> dict[str, str]:
        """
        Reads json from the file
        :param file_name: Path to the file
        :return: Dict of [str, str]
        """
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"The file was not found.")
        except Exception as e:
            print(f"An error occurred while reading json the file: {str(e)}.")

    @staticmethod
    def write_json(save_path: str, data: dict) -> None:
        """
        Saves data to json
        :param save_path: Path to save the json
        :param data: Data to save
        :return: None
        """
        try:
            with open(save_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=1)
        except FileNotFoundError:
            print(f"The file was not found.")
        except Exception as e:
            print(f"An error occurred while writing json the file: {str(e)}.")

    @staticmethod
    def write_public_key(save_path: str, public_key: rsa.RSAPublicKey) -> None:
        """
        Serializes public key to the file
        :param save_path: Path to save the public key
        :param public_key: RSA public key
        :return: None
        """
        try:
            with open(save_path, 'wb') as public_out:
                public_out.write(public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                         format=serialization.PublicFormat.SubjectPublicKeyInfo))
        except FileNotFoundError:
            print(f"The file was not found.")
        except Exception as e:
            print(f"An error occurred while writing the file: {str(e)}.")

    @staticmethod
    def write_private_key(save_path: str, private_key: rsa.RSAPrivateKey) -> None:
        """
        Serializes private key to the file
        :param save_path: Path to save the private key
        :param private_key: RSA private key
        :return: None
        """
        try:
            with open(save_path, 'wb') as private_out:
                private_out.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                            format=serialization.PrivateFormat.TraditionalOpenSSL,
                                                            encryption_algorithm=serialization.NoEncryption()))
        except FileNotFoundError:
            print(f"The file was not found.")
        except Exception as e:
            print(f"An error occurred while writing the file: {str(e)}.")

    @staticmethod
    def read_public_key(file_name: str) -> rsa.RSAPublicKey:
        """
        Deserializes public key from the file
        :param file_name: Path to the file
        :return: RSA public key object
        """
        try:
            with open(file_name, 'rb') as pem_in:
                public_bytes = pem_in.read()
                return load_pem_public_key(public_bytes)
        except FileNotFoundError:
            print(f"The file was not found.")
        except Exception as e:
            print(f"An error occurred while reading the file: {str(e)}.")

    @staticmethod
    def read_private_key(file_name: str) -> rsa.RSAPrivateKey:
        """
        Deserializes private key from the file
        :param file_name: Path to the file
        :return: RSA private key object
        """
        try:
            with open(file_name, 'rb') as pem_in:
                private_bytes = pem_in.read()
                return load_pem_private_key(
                    private_bytes, password=None)
        except FileNotFoundError:
            print(f"The file was not found.")
        except Exception as e:
            print(f"An error occurred while reading the file: {str(e)}.")

