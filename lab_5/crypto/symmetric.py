import logging
import os

from cryptography.hazmat.decrepit.ciphers import algorithms
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, modes

from fileshandler import FilesHandler


logger = logging.getLogger(__name__)

class Symmetric:
    """
    Class that handles CAST5 cipher algorithm.
    """
    def __init__(self):
        self.key = None
        logger.debug("Инициализация")

    def generate_key(self, key_len: int) -> None:
        """
        Generates random key with given length (key_len in bits, self.key in bytes).
        :param key_len: Length of key in bits
        :return: None
        """
        logger.info(f"Попытка генерации ключа длиной {key_len} бит")
        if not(40 <= key_len <= 128):
            logger.error(f"Недопустимая длина ключа ({key_len} бит)")
            raise ValueError("Wrong key length!")

        self.key = os.urandom(key_len // 8)
        logger.info(f"Ключ длиной {key_len} бит успешно сгенерирован")

    def serialization_symmetric_key(self, save_path: str) -> None:
        """
        Writes key to the file.
        :param save_path: Path to save the key
        :return: None
        """
        logger.info(f"Сохранение ключа в файл {save_path}")
        FilesHandler.write_bytes(save_path, self.key)
        logger.info("Ключ успешно сохранён")

    def deserialization_symmetric_key(self, file_name: str) -> bytes:
        """
        Reads key from the file.
        :param file_name: Path to the file with key
        :return: None
        """
        logger.info(f"Загрузка ключа из файла {file_name}")
        self.key = FilesHandler.get_bytes(file_name)
        logger.info(f"Ключ загружен ({len(self.key)} байт)")
        return self.key

    def encrypt_text(self, file_name: str, save_path: str) -> None:
        """
        Encrypts text using CAST5 algorithm and saves encrypted
        text to the file.
        :param file_name: Path to file with plain text
        :param save_path: Path to save encrypted text
        :return: None
        """
        logger.info(f"Начало шифрования файла {file_name}")

        text = FilesHandler.get_bytes(file_name)
        logger.debug(f"Прочитано {len(text)} байт для шифрования")

        padder = padding.PKCS7(64).padder()
        padded_text = padder.update(text) + padder.finalize()
        logger.debug(f"Применён padding, размер данных: {len(padded_text)} байт")

        iv = os.urandom(8)
        cipher = Cipher(algorithms.CAST5(self.key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        c_text = encryptor.update(padded_text) + encryptor.finalize()
        c_text = iv + c_text

        logger.debug(f"Сформирован зашифрованный текст длиной {len(c_text)} байт")

        FilesHandler.write_bytes(save_path, c_text)
        logger.info(f"Шифрование завершено, сохранено {len(c_text)} байт в {save_path}")


    def decrypt_text(self, encrypted_path: str, save_path: str) -> str:
        """
        Decrypts text, that encrypted using CAST5 algorithm, and
        saves it to the file
        :param encrypted_path: Path to the file with encrypted text
        :param save_path: Path so save file with decrypted text
        :return: Decrypted text
        """
        logger.info(f"Начало дешифрования файла {encrypted_path}")

        encrypted_text = FilesHandler.get_bytes(encrypted_path)

        logger.debug(f"Прочитано {len(encrypted_text)} байт для дешифрования")

        iv = encrypted_text[:8]
        cipher = Cipher(algorithms.CAST5(self.key), modes.CBC(iv))
        encrypted_text = encrypted_text[8:]
        decryptor = cipher.decryptor()
        decrypted_text = decryptor.update(encrypted_text) + decryptor.finalize()
        unpadder = padding.PKCS7(64).unpadder()
        unpadder_dc_text = unpadder.update(decrypted_text) + unpadder.finalize()

        logger.debug(f"Дешифровано {len(unpadder_dc_text)} байт данных")

        result = unpadder_dc_text.decode('UTF-8')

        FilesHandler.write_txt(save_path, result)

        logger.info(f"Дешифрование завершено, сохранено {len(result)} символов в {save_path}")
        return result

