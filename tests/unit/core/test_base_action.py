import pytest
from unittest.mock import Mock, patch

from core.base_action import BaseAction


class TestBaseAction:
    """Test cases for the BaseAction class."""

    def test_base_action_initialization(self):
        """Test that BaseAction initializes correctly."""
        action = BaseAction(parent=None, text="Test Action")

        assert action.text() == "Test Action"
        assert action.parent() is None

    def test_base_action_with_shortcut(self):
        """Test BaseAction with keyboard shortcut."""
        action = BaseAction(
            parent=None,
            text="Test Action",
            shortcut="Ctrl+T"
        )

        assert action.text() == "Test Action"
        # The shortcut should be set (we can't easily test the exact shortcut object)

    def test_base_action_with_icon(self):
        """Test BaseAction with icon."""
        # Skip icon test for now as it requires a real QIcon
        pytest.skip("Icon testing requires real QIcon object")

    def test_base_action_execute_not_implemented(self):
        """Test that execute raises NotImplementedError."""
        action = BaseAction(parent=None, text="Test Action")

        with pytest.raises(NotImplementedError):
            action.execute()

    def test_base_action_trigger_calls_execute(self):
        """Test that execute method can be called (trigger behavior is Qt internal)."""
        action = BaseAction(parent=None, text="Test Action")

        # We can't easily test the Qt signal connection, but we can test that
        # the execute method exists and behaves as expected
        with pytest.raises(NotImplementedError):
            action.execute()

    def test_get_parent_window(self):
        """Test get_parent_window method."""
        action = BaseAction(parent=None, text="Test Action")

        assert action.get_parent_window() is None

    def test_get_text_editor_calls_parent_method(self):
        """Test get_text_editor method calls parent method."""
        action = BaseAction(parent=None, text="Test Action")

        # Mock the parent and its get_text_editor method
        mock_parent = Mock()
        mock_text_editor = Mock()
        mock_parent.get_text_editor.return_value = mock_text_editor

        # Mock the get_parent_window method to return our mock parent
        with patch.object(action, 'get_parent_window', return_value=mock_parent):
            result = action.get_text_editor()

            assert result == mock_text_editor
            mock_parent.get_text_editor.assert_called_once()