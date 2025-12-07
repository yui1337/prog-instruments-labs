import pytest
from hybrid import Hybrid
from unittest.mock import Mock, patch


class TestHybrid:
    def test_init_default_key_length(self):
        hybrid = Hybrid()
        assert hybrid.key_len == 128
        assert hybrid.symmetric is not None
        assert hybrid.asymmetric is not None

    @pytest.mark.parametrize("key_length", [40, 64, 96, 128])
    def test_init_custom_key_length(self, key_length):
        hybrid = Hybrid(key_length=key_length)
        assert hybrid.key_len == key_length

    @patch('hybrid.Asymmetric.generate_asymmetric_keys')
    @patch('hybrid.Asymmetric.serialization_public_key')
    @patch('hybrid.Asymmetric.serialization_private_key')
    @patch('hybrid.Symmetric.generate_key')
    @patch('hybrid.Asymmetric.encrypt_symmetric_key')
    @patch('hybrid.Symmetric.serialization_symmetric_key')
    def test_generate_keys(self, mock_sym_ser, mock_asym_enc, mock_sym_gen,
                          mock_priv_ser, mock_pub_ser, mock_asym_gen):
        hybrid = Hybrid()
        mock_asym_enc.return_value = b'encrypted_key'
        hybrid.generate_keys('public.pem', 'private.pem', 'symmetric.bin')
        mock_asym_gen.assert_called_once()
        mock_pub_ser.assert_called_once_with('public.pem')
        mock_priv_ser.assert_called_once_with('private.pem')
        mock_sym_gen.assert_called_once_with(128)

    @patch('hybrid.Asymmetric.decrypt_symmetric_key')
    @patch('hybrid.Symmetric.encrypt_text')
    def test_encrypt_data(self, mock_encrypt, mock_decrypt_key):
        hybrid = Hybrid()
        mock_decrypt_key.return_value = b'decrypted_key_16'
        hybrid.encrypt_data('plain.txt', 'private.pem', 'encrypted_key.bin', 'encrypted.bin')
        mock_decrypt_key.assert_called_once()
        assert hybrid.symmetric.key == b'decrypted_key_16'

    @patch('hybrid.Asymmetric.decrypt_symmetric_key')
    @patch('hybrid.Symmetric.decrypt_text')
    def test_decrypt_data(self, mock_decrypt_text, mock_decrypt_key):
        hybrid = Hybrid()
        mock_decrypt_key.return_value = b'decrypted_key_16'
        hybrid.decrypt_data('encrypted.bin', 'private.pem', 'encrypted_key.bin', 'decrypted.txt')
        mock_decrypt_key.assert_called_once()
        assert hybrid.symmetric.key == b'decrypted_key_16'

    @patch('hybrid.Asymmetric')
    @patch('hybrid.Symmetric')
    def test_hybrid_workflow_integration(self, mock_sym_class, mock_asym_class):
        mock_sym = Mock()
        mock_asym = Mock()
        mock_sym_class.return_value = mock_sym
        mock_asym_class.return_value = mock_asym
        hybrid = Hybrid(key_length=64)
        hybrid.generate_keys('pub.pem', 'priv.pem', 'sym.bin')
        assert mock_asym.generate_asymmetric_keys.called
