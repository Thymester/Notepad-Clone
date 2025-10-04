import pytest
from unittest.mock import Mock, patch

from features.edit_operations.undo import UndoAction
from features.edit_operations.redo import RedoAction
from features.edit_operations.cut import CutAction
from features.edit_operations.copy import CopyAction
from features.edit_operations.paste import PasteAction
from features.edit_operations.delete import DeleteAction
from features.edit_operations.find import FindAction
from features.edit_operations.replace import ReplaceAction
from features.edit_operations.goto import GotoAction
from features.edit_operations.select_all import SelectAllAction
from features.edit_operations.time_date import TimeDateAction


class TestUndoAction:
    """Test cases for UndoAction."""

    def test_undo_action_initialization(self):
        """Test UndoAction initializes correctly."""
        mock_parent = Mock()
        action = UndoAction(mock_parent)

        assert action.text() == "&Undo\tCtrl+Z"

    def test_execute_undo(self):
        """Test executing undo action."""
        mock_parent = Mock()
        mock_text_editor = Mock()
        mock_parent.get_text_editor.return_value = mock_text_editor

        action = UndoAction(mock_parent)
        action.execute()

        mock_text_editor.undo.assert_called_once()


class TestRedoAction:
    """Test cases for RedoAction."""

    def test_redo_action_initialization(self):
        """Test RedoAction initializes correctly."""
        mock_parent = Mock()
        action = RedoAction(mock_parent)

        assert action.text() == "&Redo\tCtrl+Y"

    def test_execute_redo(self):
        """Test executing redo action."""
        mock_parent = Mock()
        mock_text_editor = Mock()
        mock_parent.get_text_editor.return_value = mock_text_editor

        action = RedoAction(mock_parent)
        action.execute()

        mock_text_editor.redo.assert_called_once()


class TestCutAction:
    """Test cases for CutAction."""

    def test_cut_action_initialization(self):
        """Test CutAction initializes correctly."""
        mock_parent = Mock()
        action = CutAction(mock_parent)

        assert action.text() == "Cu&t\tCtrl+X"

    def test_execute_cut(self):
        """Test executing cut action."""
        mock_parent = Mock()
        mock_text_editor = Mock()
        mock_parent.get_text_editor.return_value = mock_text_editor

        action = CutAction(mock_parent)
        action.execute()

        mock_text_editor.cut.assert_called_once()


class TestCopyAction:
    """Test cases for CopyAction."""

    def test_copy_action_initialization(self):
        """Test CopyAction initializes correctly."""
        mock_parent = Mock()
        action = CopyAction(mock_parent)

        assert action.text() == "&Copy\tCtrl+C"

    def test_execute_copy(self):
        """Test executing copy action."""
        mock_parent = Mock()
        mock_text_editor = Mock()
        mock_parent.get_text_editor.return_value = mock_text_editor

        action = CopyAction(mock_parent)
        action.execute()

        mock_text_editor.copy.assert_called_once()


class TestPasteAction:
    """Test cases for PasteAction."""

    def test_paste_action_initialization(self):
        """Test PasteAction initializes correctly."""
        mock_parent = Mock()
        action = PasteAction(mock_parent)

        assert action.text() == "&Paste\tCtrl+V"

    def test_execute_paste(self):
        """Test executing paste action."""
        mock_parent = Mock()
        mock_text_editor = Mock()
        mock_parent.get_text_editor.return_value = mock_text_editor

        action = PasteAction(mock_parent)
        action.execute()

        mock_text_editor.paste.assert_called_once()


class TestDeleteAction:
    """Test cases for DeleteAction."""

    def test_delete_action_initialization(self):
        """Test DeleteAction initializes correctly."""
        mock_parent = Mock()
        action = DeleteAction(mock_parent)

        assert action.text() == "&Delete\tDel"

    def test_execute_delete(self):
        """Test executing delete action."""
        mock_parent = Mock()
        mock_text_editor = Mock()
        mock_parent.get_text_editor.return_value = mock_text_editor

        action = DeleteAction(mock_parent)
        action.execute()

        mock_text_editor.delete_selected_text.assert_called_once()


class TestFindAction:
    """Test cases for FindAction."""

    def test_find_action_initialization(self):
        """Test FindAction initializes correctly."""
        mock_parent = Mock()
        action = FindAction(mock_parent)

        assert action.text() == "&Find...\tCtrl+F"

    def test_execute_find_with_existing_dialog(self):
        """Test executing find with existing dialog."""
        mock_parent = Mock()
        mock_dialog = Mock()
        mock_parent.find_replace_dialog = mock_dialog

        action = FindAction(mock_parent)
        action.execute()

        mock_dialog.show.assert_called_once()
        mock_dialog.raise_.assert_called_once()
        mock_dialog.activateWindow.assert_called_once()

    @patch('ui.find_replace_dialog.FindReplaceDialog')
    def test_execute_find_create_new_dialog(self, mock_dialog_class):
        """Test executing find by creating new dialog."""
        mock_parent = Mock()
        mock_parent.find_replace_dialog = None
        mock_dialog_instance = Mock()
        mock_dialog_class.return_value = mock_dialog_instance

        action = FindAction(mock_parent)
        action.execute()

        mock_dialog_class.assert_called_once_with(mock_parent)
        mock_dialog_instance.show.assert_called_once()
        assert mock_parent.find_replace_dialog == mock_dialog_instance


class TestReplaceAction:
    """Test cases for ReplaceAction."""

    def test_replace_action_initialization(self):
        """Test ReplaceAction initializes correctly."""
        mock_parent = Mock()
        action = ReplaceAction(mock_parent)

        assert action.text() == "&Replace...\tCtrl+H"

    def test_execute_replace_with_existing_dialog(self):
        """Test executing replace with existing dialog."""
        mock_parent = Mock()
        mock_dialog = Mock()
        mock_parent.find_replace_dialog = mock_dialog

        action = ReplaceAction(mock_parent)
        action.execute()

        mock_dialog.show.assert_called_once()
        mock_dialog.raise_.assert_called_once()
        mock_dialog.activateWindow.assert_called_once()

    @patch('ui.find_replace_dialog.FindReplaceDialog')
    def test_execute_replace_create_new_dialog(self, mock_dialog_class):
        """Test executing replace by creating new dialog."""
        mock_parent = Mock()
        mock_parent.find_replace_dialog = None
        mock_dialog_instance = Mock()
        mock_dialog_class.return_value = mock_dialog_instance

        action = ReplaceAction(mock_parent)
        action.execute()

        mock_dialog_class.assert_called_once_with(mock_parent)
        mock_dialog_instance.show.assert_called_once()
        assert mock_parent.find_replace_dialog == mock_dialog_instance


class TestGotoAction:
    """Test cases for GotoAction."""

    def test_goto_action_initialization(self):
        """Test GotoAction initializes correctly."""
        mock_parent = Mock()
        action = GotoAction(mock_parent)

        assert action.text() == "&Go To...\tCtrl+G"

    @patch('PyQt5.QtWidgets.QInputDialog.getInt')
    def test_execute_goto_success(self, mock_get_int):
        """Test successful goto operation."""
        mock_get_int.return_value = (5, True)  # Line 5, OK pressed

        mock_parent = Mock()
        mock_text_editor = Mock()
        mock_parent.get_text_editor.return_value = mock_text_editor

        action = GotoAction(mock_parent)
        action.execute()

        mock_text_editor.goto_line.assert_called_once_with(5)

    @patch('PyQt5.QtWidgets.QInputDialog.getInt')
    def test_execute_goto_cancelled(self, mock_get_int):
        """Test cancelled goto operation."""
        mock_get_int.return_value = (0, False)  # Cancelled

        mock_parent = Mock()
        mock_text_editor = Mock()
        mock_parent.get_text_editor.return_value = mock_text_editor

        action = GotoAction(mock_parent)
        action.execute()

        mock_text_editor.goto_line.assert_not_called()


class TestSelectAllAction:
    """Test cases for SelectAllAction."""

    def test_select_all_action_initialization(self):
        """Test SelectAllAction initializes correctly."""
        mock_parent = Mock()
        action = SelectAllAction(mock_parent)

        assert action.text() == "Select &All\tCtrl+A"

    def test_execute_select_all(self):
        """Test executing select all action."""
        mock_parent = Mock()
        mock_text_editor = Mock()
        mock_parent.get_text_editor.return_value = mock_text_editor

        action = SelectAllAction(mock_parent)
        action.execute()

        mock_text_editor.select_all_text.assert_called_once()


class TestTimeDateAction:
    """Test cases for TimeDateAction."""

    def test_time_date_action_initialization(self):
        """Test TimeDateAction initializes correctly."""
        mock_parent = Mock()
        action = TimeDateAction(mock_parent)

        assert action.text() == "Time/&Date\tF5"

    @patch('datetime.datetime')
    def test_execute_time_date(self, mock_datetime):
        """Test executing time/date action."""
        # Mock datetime.now() to return a specific datetime
        mock_now = Mock()
        mock_now.strftime.return_value = "12:30 PM 10/04/2025"
        mock_datetime.now.return_value = mock_now

        mock_parent = Mock()
        mock_text_editor = Mock()
        mock_parent.get_text_editor.return_value = mock_text_editor

        action = TimeDateAction(mock_parent)
        action.execute()

        mock_text_editor.insert_text_at_cursor.assert_called_once_with("12:30 PM 10/04/2025")