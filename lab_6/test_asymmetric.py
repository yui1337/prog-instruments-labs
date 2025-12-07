import pytest
from asymmetric import Asymmetric
from unittest.mock import Mock, patch
from cryptography.hazmat.primitives.asymmetric import rsa


class TestAsymmetric:
    def test_generate_asymmetric_keys(self):
        asym = Asymmetric()
        public_key, private_key = asym.generate_asymmetric_keys()
        assert public_key is not None
        assert private_key is not None
        assert isinstance(public_key, rsa.RSAPublicKey)
        assert isinstance(private_key, rsa.RSAPrivateKey)

    @patch('asymmetric.FilesHandler.write_public_key')
    def test_serialization_public_key(self, mock_write):
        asym = Asymmetric()
        asym.generate_asymmetric_keys()
        asym.serialization_public_key('public_key.pem')
        mock_write.assert_called_once_with('public_key.pem', asym.public_key)

    @patch('asymmetric.FilesHandler.write_private_key')
    def test_serialization_private_key(self, mock_write):
        asym = Asymmetric()
        asym.generate_asymmetric_keys()
        asym.serialization_private_key('private_key.pem')
        mock_write.assert_called_once_with('private_key.pem', asym.private_key)

    @patch('asymmetric.FilesHandler.read_public_key')
    def test_deserialization_public_key(self, mock_read):
        mock_key = Mock(spec=rsa.RSAPublicKey)
        mock_read.return_value = mock_key
        result = Asymmetric.deserialization_public_key('public_key.pem')
        assert result == mock_key

    @patch('asymmetric.FilesHandler.read_private_key')
    def test_deserialization_private_key(self, mock_read):
        mock_key = Mock(spec=rsa.RSAPrivateKey)
        mock_read.return_value = mock_key
        result = Asymmetric.deserialization_private_key('private_key.pem')
        assert result == mock_key

    @patch('asymmetric.FilesHandler.write_bytes')
    @patch('asymmetric.FilesHandler.read_public_key')
    def test_encrypt_symmetric_key(self, mock_read_public, mock_write_bytes):
        asym = Asymmetric()
        asym.generate_asymmetric_keys()
        mock_read_public.return_value = asym.public_key
        symmetric_key = b'1234567890123456'
        result = asym.encrypt_symmetric_key('public_key.pem', symmetric_key, 'encrypted_key.bin')
        assert result is not None
        assert isinstance(result, bytes)
        mock_write_bytes.assert_called_once()

    @patch('asymmetric.FilesHandler.get_bytes')
    @patch('asymmetric.FilesHandler.read_private_key')
    def test_decrypt_symmetric_key(self, mock_read_private, mock_get_bytes):
        asym = Asymmetric()
        asym.generate_asymmetric_keys()
        symmetric_key = b'1234567890123456'
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import padding
        encrypted_key = asym.public_key.encrypt(
            symmetric_key,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(), label=None))
        mock_read_private.return_value = asym.private_key
        mock_get_bytes.return_value = encrypted_key
        result = asym.decrypt_symmetric_key('private_key.pem', 'encrypted_key.bin')
        assert result == symmetric_key

    def test_encrypt_decrypt_roundtrip(self):
        asym = Asymmetric()
        asym.generate_asymmetric_keys()
        original_data = b'secret_symmetric_key'
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import padding
        encrypted = asym.public_key.encrypt(
            original_data,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(), label=None))
        decrypted = asym.private_key.decrypt(
            encrypted,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(), label=None))
        assert decrypted == original_data
