import pytest
from unittest.mock import Mock, patch

from features.format_operations.word_wrap import WordWrapAction
from features.format_operations.font import FontAction


class TestWordWrapAction:
    """Test cases for WordWrapAction."""

    def test_word_wrap_action_initialization(self):
        """Test WordWrapAction initializes correctly."""
        mock_parent = Mock()
        action = WordWrapAction(mock_parent)

        assert action.text() == "&Word Wrap"
        assert action.isCheckable()
        assert action.isChecked()

    def test_execute_word_wrap_checked(self):
        """Test executing word wrap when checked."""
        mock_parent = Mock()
        mock_text_editor = Mock()
        mock_parent.get_text_editor.return_value = mock_text_editor

        action = WordWrapAction(mock_parent)
        action.setChecked(True)
        action.execute()

        # Should set line wrap mode to WidgetWidth
        mock_text_editor.setLineWrapMode.assert_called_once()
        call_args = mock_text_editor.setLineWrapMode.call_args[0][0]
        assert call_args.name == "WidgetWidth"

    def test_execute_word_wrap_unchecked(self):
        """Test executing word wrap when unchecked."""
        mock_parent = Mock()
        mock_text_editor = Mock()
        mock_parent.get_text_editor.return_value = mock_text_editor

        action = WordWrapAction(mock_parent)
        action.setChecked(False)
        action.execute()

        # Should set line wrap mode to NoWrap
        mock_text_editor.setLineWrapMode.assert_called_once()
        call_args = mock_text_editor.setLineWrapMode.call_args[0][0]
        assert call_args.name == "NoWrap"


class TestFontAction:
    """Test cases for FontAction."""

    def test_font_action_initialization(self):
        """Test FontAction initializes correctly."""
        mock_parent = Mock()
        action = FontAction(mock_parent)

        assert action.text() == "&Font..."

    @patch('PyQt5.QtWidgets.QFontDialog.getFont')
    def test_execute_font_success(self, mock_get_font):
        """Test successful font change."""
        mock_font = Mock()
        mock_get_font.return_value = (mock_font, True)  # Font selected

        mock_parent = Mock()
        mock_text_editor = Mock()
        mock_parent.get_text_editor.return_value = mock_text_editor

        action = FontAction(mock_parent)
        action.execute()

        mock_text_editor.set_editor_font.assert_called_once_with(mock_font)

    @patch('PyQt5.QtWidgets.QFontDialog.getFont')
    def test_execute_font_cancelled(self, mock_get_font):
        """Test cancelled font change."""
        mock_get_font.return_value = (None, False)  # Cancelled

        mock_parent = Mock()
        mock_text_editor = Mock()
        mock_parent.get_text_editor.return_value = mock_text_editor

        action = FontAction(mock_parent)
        action.execute()

        mock_text_editor.set_editor_font.assert_not_called()