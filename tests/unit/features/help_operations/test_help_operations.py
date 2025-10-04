import pytest
from unittest.mock import Mock, patch

from features.help_operations.about import AboutAction
from features.help_operations.setup_file_associations import SetupFileAssociationsAction


class TestAboutAction:
    """Test cases for AboutAction."""

    def test_about_action_initialization(self):
        """Test AboutAction initializes correctly."""
        mock_parent = Mock()
        action = AboutAction(mock_parent)

        assert action.text() == "&About Notepad"

    @patch('PyQt5.QtWidgets.QMessageBox.about')
    def test_execute_shows_about_dialog(self, mock_about):
        """Test that execute shows the about dialog."""
        mock_parent = Mock()
        mock_parent.windowTitle.return_value = "Notepad Clone"

        action = AboutAction(mock_parent)
        action.execute()

        mock_about.assert_called_once()
        args, kwargs = mock_about.call_args
        assert args[0] == mock_parent  # parent widget
        assert "Notepad Clone" in args[1]  # title
        assert "About Notepad" in args[1]
        assert "Notepad Clone" in args[2]  # message
        assert "Version" in args[2]


class TestSetupFileAssociationsAction:
    """Test cases for SetupFileAssociationsAction."""

    @patch('os.path.exists')
    def test_get_executable_path_packaged_app(self, mock_exists):
        """Test executable path detection for packaged app."""
        with patch('sys.frozen', True, create=True), \
             patch('sys.executable', 'C:\\packaged\\app.exe'):
            # Create action instance without Qt initialization
            action = SetupFileAssociationsAction.__new__(SetupFileAssociationsAction)

            result = action._get_executable_path()
            assert result == 'C:\\packaged\\app.exe'

    @patch('os.path.exists')
    def test_get_executable_path_desktop_exe(self, mock_exists):
        """Test executable path detection finds desktop exe."""
        mock_exists.return_value = True

        action = SetupFileAssociationsAction.__new__(SetupFileAssociationsAction)

        result = action._get_executable_path()
        assert result is not None
        assert 'Modern Notepad.exe' in result

    @patch('os.path.exists')
    def test_get_executable_path_dist_exe(self, mock_exists):
        """Test executable path detection finds dist exe."""
        # Mock exists to return False for desktop paths, True for dist
        def exists_side_effect(path):
            return 'dist' in path and path.endswith('.exe')

        mock_exists.side_effect = exists_side_effect

        action = SetupFileAssociationsAction.__new__(SetupFileAssociationsAction)

        result = action._get_executable_path()
        assert result is not None
        assert 'dist' in result
        assert result.endswith('.exe')

    @patch('os.path.exists')
    def test_get_executable_path_not_found(self, mock_exists):
        """Test executable path detection when nothing is found."""
        mock_exists.return_value = False

        action = SetupFileAssociationsAction.__new__(SetupFileAssociationsAction)

        result = action._get_executable_path()
        assert result is None