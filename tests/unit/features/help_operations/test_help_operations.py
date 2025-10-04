import pytest
from unittest.mock import Mock, patch

from features.help_operations.about import AboutAction


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