import pytest
from unittest.mock import Mock, patch, mock_open
import os
import sys
from typing import Dict, Any

from utils.registry_manager import RegistryManager


class TestRegistryManager:
    """Test cases for RegistryManager."""

    def setup_method(self):
        """Set up test fixtures."""
        self.registry_manager = RegistryManager()
        self.test_exe_path = r"C:\Users\test\Desktop\Modern Notepad.exe"

    @patch('ctypes.windll.shell32.IsUserAnAdmin')
    def test_is_admin_true(self, mock_is_admin):
        """Test is_admin returns True when running as administrator."""
        mock_is_admin.return_value = 1
        assert self.registry_manager.is_admin() is True

    @patch('ctypes.windll.shell32.IsUserAnAdmin')
    def test_is_admin_false(self, mock_is_admin):
        """Test is_admin returns False when not running as administrator."""
        mock_is_admin.return_value = 0
        assert self.registry_manager.is_admin() is False

    @patch('utils.registry_manager.winreg.CreateKey')
    @patch('utils.registry_manager.winreg.SetValue')
    def test_set_file_association_success(self, mock_set_value, mock_create_key):
        """Test successful file association setup."""
        # Mock admin check
        with patch.object(self.registry_manager, 'is_admin', return_value=True):
            # Mock registry operations
            mock_key = Mock()
            mock_create_key.return_value.__enter__.return_value = mock_key

            result = self.registry_manager.set_file_association(
                ".txt", "TestProgID", "Test Document", self.test_exe_path
            )

            assert result is True
            # Verify registry calls were made
            assert mock_create_key.call_count == 4  # extension, progid, icon, command
            assert mock_set_value.call_count == 4   # extension value, progid desc, icon, command

    @patch('utils.registry_manager.winreg.CreateKey')
    @patch('utils.registry_manager.winreg.SetValue')
    def test_set_file_association_no_admin(self, mock_set_value, mock_create_key):
        """Test file association setup fails without admin privileges."""
        with patch.object(self.registry_manager, 'is_admin', return_value=False):
            with pytest.raises(PermissionError, match="Administrator privileges required"):
                self.registry_manager.set_file_association(
                    ".txt", "TestProgID", "Test Document", self.test_exe_path
                )

    @patch('utils.registry_manager.winreg.CreateKey')
    @patch('utils.registry_manager.winreg.SetValue')
    def test_set_file_association_registry_error(self, mock_set_value, mock_create_key):
        """Test file association setup handles registry errors."""
        with patch.object(self.registry_manager, 'is_admin', return_value=True):
            mock_create_key.side_effect = Exception("Registry error")

            result = self.registry_manager.set_file_association(
                ".txt", "TestProgID", "Test Document", self.test_exe_path
            )

            assert result is False

    @patch('utils.registry_manager.winreg.CreateKey')
    @patch('utils.registry_manager.winreg.SetValue')
    def test_register_application_success(self, mock_set_value, mock_create_key):
        """Test successful application registration."""
        with patch.object(self.registry_manager, 'is_admin', return_value=True):
            mock_key = Mock()
            mock_create_key.return_value.__enter__.return_value = mock_key

            result = self.registry_manager.register_application(
                "TestApp.exe", self.test_exe_path
            )

            assert result is True
            # Verify registry calls
            assert mock_create_key.call_count == 3  # app, icon, command
            assert mock_set_value.call_count == 3   # app name, icon, command

    @patch('utils.registry_manager.winreg.CreateKey')
    @patch('utils.registry_manager.winreg.SetValue')
    def test_register_application_no_admin(self, mock_set_value, mock_create_key):
        """Test application registration fails without admin privileges."""
        with patch.object(self.registry_manager, 'is_admin', return_value=False):
            with pytest.raises(PermissionError, match="Administrator privileges required"):
                self.registry_manager.register_application(
                    "TestApp.exe", self.test_exe_path
                )

    @patch('utils.registry_manager.winreg.OpenKey')
    @patch('utils.registry_manager.winreg.QueryValueEx')
    def test_get_file_association_success(self, mock_query_value, mock_open_key):
        """Test successful file association retrieval."""
        mock_key = Mock()
        mock_open_key.return_value.__enter__.return_value = mock_key
        mock_query_value.return_value = ("TestProgID", 1)

        result = self.registry_manager.get_file_association(".txt")

        assert result == "TestProgID"
        mock_open_key.assert_called_once()
        args, kwargs = mock_open_key.call_args
        assert args[1] == ".txt"  # Second argument should be the extension

    @patch('utils.registry_manager.winreg.OpenKey')
    def test_get_file_association_not_found(self, mock_open_key):
        """Test file association retrieval when extension not found."""
        mock_open_key.side_effect = FileNotFoundError()

        result = self.registry_manager.get_file_association(".txt")

        assert result is None

    @patch('utils.registry_manager.winreg.OpenKey')
    def test_get_file_association_error(self, mock_open_key):
        """Test file association retrieval handles errors."""
        mock_open_key.side_effect = Exception("Registry error")

        result = self.registry_manager.get_file_association(".txt")

        assert result is None

    @patch.object(RegistryManager, 'register_application')
    @patch.object(RegistryManager, 'set_file_association')
    def test_setup_notepad_associations_success(self, mock_set_assoc, mock_register_app):
        """Test successful setup of Notepad associations."""
        with patch.object(self.registry_manager, 'is_admin', return_value=True):
            mock_register_app.return_value = True
            mock_set_assoc.return_value = True

            results = self.registry_manager.setup_notepad_associations(self.test_exe_path)

            expected_results = {
                'app_registration': True,
                'txt_association': True,
                'enc_association': True
            }
            assert results == expected_results

            # Verify calls
            mock_register_app.assert_called_once_with("Modern Notepad.exe", self.test_exe_path)
            assert mock_set_assoc.call_count == 2  # .txt and .enc

    @patch.object(RegistryManager, 'register_application')
    @patch.object(RegistryManager, 'set_file_association')
    def test_setup_notepad_associations_partial_failure(self, mock_set_assoc, mock_register_app):
        """Test setup of Notepad associations with partial failures."""
        with patch.object(self.registry_manager, 'is_admin', return_value=True):
            mock_register_app.return_value = True
            mock_set_assoc.side_effect = [True, False]  # txt succeeds, enc fails

            results = self.registry_manager.setup_notepad_associations(self.test_exe_path)

            expected_results = {
                'app_registration': True,
                'txt_association': True,
                'enc_association': False
            }
            assert results == expected_results