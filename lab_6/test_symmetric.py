import pytest
import os
from symmetric import Symmetric
from unittest.mock import Mock, patch, mock_open


class TestSymmetric:
    def test_generate_key_valid_length(self):
        sym = Symmetric()
        sym.generate_key(128)
        assert sym.key is not None
        assert len(sym.key) == 16

    @pytest.mark.parametrize("key_len,expected_bytes", [
        (40, 5),
        (64, 8),
        (128, 16),
    ])
    def test_generate_key_parametrized(self, key_len, expected_bytes):
        sym = Symmetric()
        sym.generate_key(key_len)
        assert len(sym.key) == expected_bytes

    @pytest.mark.parametrize("invalid_key_len", [32, 256, 0, -1])
    def test_generate_key_invalid_length(self, invalid_key_len):
        sym = Symmetric()
        with pytest.raises(ValueError, match="Wrong key length!"):
            sym.generate_key(invalid_key_len)

    @patch('symmetric.FilesHandler.write_bytes')
    def test_serialization_symmetric_key(self, mock_write):
        sym = Symmetric()
        sym.key = b'test_key_12345678'
        sym.serialization_symmetric_key('test_key.bin')
        mock_write.assert_called_once_with('test_key.bin', sym.key)

    @patch('symmetric.FilesHandler.get_bytes')
    def test_deserialization_symmetric_key(self, mock_get_bytes):
        sym = Symmetric()
        expected_key = b'test_key_12345678'
        mock_get_bytes.return_value = expected_key
        result = sym.deserialization_symmetric_key('test_key.bin')
        assert sym.key == expected_key
        assert result == expected_key

    @patch('symmetric.FilesHandler.write_bytes')
    @patch('symmetric.FilesHandler.get_bytes')
    @patch('symmetric.os.urandom')
    def test_encrypt_text(self, mock_urandom, mock_get_bytes, mock_write_bytes):
        sym = Symmetric()
        sym.key = b'12345678'
        mock_urandom.return_value = b'12345678'
        mock_get_bytes.return_value = b'Hello World!'
        sym.encrypt_text('plain.txt', 'encrypted.bin')
        mock_get_bytes.assert_called_once_with('plain.txt')
        mock_write_bytes.assert_called_once()
        encrypted_data = mock_write_bytes.call_args[0][1]
        assert encrypted_data[:8] == b'12345678'

    @patch('symmetric.FilesHandler.write_txt')
    @patch('symmetric.FilesHandler.get_bytes')
    def test_decrypt_text(self, mock_get_bytes, mock_write_txt):
        sym = Symmetric()
        sym.key = b'12345678'
        from cryptography.hazmat.primitives import padding
        from cryptography.hazmat.primitives.ciphers import Cipher, modes
        from cryptography.hazmat.decrepit.ciphers import algorithms
        iv = b'12345678'
        plain_text = b'Hello World!'
        padder = padding.PKCS7(64).padder()
        padded_text = padder.update(plain_text) + padder.finalize()
        cipher = Cipher(algorithms.CAST5(sym.key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        encrypted = encryptor.update(padded_text) + encryptor.finalize()
        mock_get_bytes.return_value = iv + encrypted
        result = sym.decrypt_text('encrypted.bin', 'decrypted.txt')
        assert result == 'Hello World!'
