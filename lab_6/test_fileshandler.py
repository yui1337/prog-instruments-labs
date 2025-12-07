import pytest
from fileshandler import FilesHandler
from unittest.mock import mock_open, patch
from cryptography.hazmat.primitives.asymmetric import rsa


class TestFilesHandler:
    @patch('builtins.open', new_callable=mock_open, read_data=b'test data')
    def test_get_bytes_success(self, mock_file):
        result = FilesHandler.get_bytes('test.bin')
        assert result == b'test data'

    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch('builtins.print')
    def test_get_bytes_file_not_found(self, mock_print, mock_file):
        result = FilesHandler.get_bytes('nonexistent.bin')
        assert result is None
        mock_print.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    def test_write_bytes_success(self, mock_file):
        FilesHandler.write_bytes('output.bin', b'test data')
        mock_file.assert_called_once_with('output.bin', mode='wb')

    @patch('builtins.open', new_callable=mock_open, read_data='Hello World!')
    def test_get_txt_success(self, mock_file):
        result = FilesHandler.get_txt('test.txt')
        assert result == 'Hello World!'

    @patch('builtins.open', new_callable=mock_open)
    def test_write_txt_success(self, mock_file):
        FilesHandler.write_txt('output.txt', 'Test text')
        mock_file.assert_called_once_with('output.txt', 'w')

    @patch('builtins.open', new_callable=mock_open, read_data='{"key": "value"}')
    def test_get_json_success(self, mock_file):
        result = FilesHandler.get_json('test.json')
        assert result == {"key": "value"}

    @patch('builtins.open', new_callable=mock_open)
    def test_write_json_success(self, mock_file):
        FilesHandler.write_json('output.json', {"name": "test"})
        mock_file.assert_called_once()

    @pytest.mark.parametrize("exception_type,expected_message", [
        (FileNotFoundError, "The file was not found."),
        (PermissionError, "An error occurred while reading the file"),
    ])
    @patch('builtins.print')
    def test_get_bytes_error_handling(self, mock_print, exception_type, expected_message):
        with patch('builtins.open', side_effect=exception_type("Test error")):
            result = FilesHandler.get_bytes('test.bin')
            assert result is None
            assert mock_print.called

    @patch('builtins.open', new_callable=mock_open)
    def test_write_public_key(self, mock_file):
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()
        FilesHandler.write_public_key('public.pem', public_key)
        mock_file.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    def test_write_private_key(self, mock_file):
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        FilesHandler.write_private_key('private.pem', private_key)
        mock_file.assert_called_once()
