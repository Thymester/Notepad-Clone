import pytest
from unittest.mock import Mock, patch, MagicMock

from features.file_operations.new_file import NewFileAction
from features.file_operations.open_file import OpenFileAction
from features.file_operations.save_file import SaveFileAction
from features.file_operations.save_as_file import SaveAsFileAction
from features.file_operations.print_file import PrintFileAction
from features.file_operations.exit_app import ExitAppAction


class TestNewFileAction:
    """Test cases for NewFileAction."""

    def test_new_file_action_initialization(self):
        """Test NewFileAction initializes correctly."""
        mock_parent = Mock()
        action = NewFileAction(mock_parent)

        assert action.text() == "&New\tCtrl+N"
        assert not action.is_new_window

    def test_new_window_action_initialization(self):
        """Test NewFileAction initializes as new window."""
        mock_parent = Mock()
        action = NewFileAction(mock_parent, is_new_window=True)

        assert action.text() == "New &Window\tCtrl+Shift+N"
        assert action.is_new_window

    @patch('features.file_operations.new_file.NotepadWindow')
    def test_execute_new_window(self, mock_notepad_window, qtbot):
        """Test executing new window action."""
        mock_parent = Mock()
        action = NewFileAction(mock_parent, is_new_window=True)

        action.execute()

        mock_notepad_window.assert_called_once()
        mock_notepad_window.return_value.show.assert_called_once()

    def test_execute_new_file_with_save_check(self, qtbot):
        """Test executing new file with save check."""
        mock_parent = Mock()
        mock_text_editor = Mock()
        mock_parent.get_text_editor.return_value = mock_text_editor
        mock_parent.is_document_modified.return_value = True

        action = NewFileAction(mock_parent)

        with patch.object(action, '_check_save_changes', return_value=True):
            action.execute()

            mock_text_editor.clear_content.assert_called_once()
            mock_parent.set_current_file_path.assert_called_once_with("")
            mock_parent.set_modified.assert_called_once_with(False)

    def test_check_save_changes_not_modified(self):
        """Test _check_save_changes when document is not modified."""
        mock_parent = Mock()
        mock_parent.is_document_modified.return_value = False

        action = NewFileAction(mock_parent)

        result = action._check_save_changes()

        assert result is True

    @patch('PyQt5.QtWidgets.QMessageBox.question')
    def test_check_save_changes_user_cancels(self, mock_question):
        """Test _check_save_changes when user cancels."""
        mock_question.return_value = Mock()  # Mock QMessageBox.Cancel
        mock_question.return_value.name = "Cancel"  # Simulate Cancel

        mock_parent = Mock()
        mock_parent.is_document_modified.return_value = True

        action = NewFileAction(mock_parent)

        # Mock the QMessageBox constants
        with patch('PyQt5.QtWidgets.QMessageBox.Cancel', Mock()):
            with patch('PyQt5.QtWidgets.QMessageBox.question', return_value=Mock()):
                result = action._check_save_changes()
                assert result is False


class TestOpenFileAction:
    """Test cases for OpenFileAction."""

    def test_open_file_action_initialization(self):
        """Test OpenFileAction initializes correctly."""
        mock_parent = Mock()
        action = OpenFileAction(mock_parent)

        assert action.text() == "&Open...\tCtrl+O"

    @patch('PyQt5.QtWidgets.QFileDialog.getOpenFileName')
    def test_execute_open_file_success(self, mock_get_open_file, qtbot):
        """Test successfully opening a file."""
        mock_get_open_file.return_value = ("test.txt", "Text files (*.txt)")

        mock_parent = Mock()
        mock_text_editor = Mock()
        mock_parent.get_text_editor.return_value = mock_text_editor

        action = OpenFileAction(mock_parent)

        with patch('builtins.open', Mock()) as mock_open:
            mock_file = Mock()
            mock_file.read.return_value = "file content"
            mock_open.return_value.__enter__.return_value = mock_file

            with patch.object(action, '_check_save_changes', return_value=True):
                action.execute()

                mock_text_editor.set_content.assert_called_once_with("file content")
                mock_parent.set_current_file_path.assert_called_once_with("test.txt")
                mock_parent.set_modified.assert_called_once_with(False)

    @patch('PyQt5.QtWidgets.QFileDialog.getOpenFileName')
    def test_execute_open_file_cancelled(self, mock_get_open_file):
        """Test when user cancels file open dialog."""
        mock_get_open_file.return_value = ("", "")

        mock_parent = Mock()
        action = OpenFileAction(mock_parent)

        action.execute()

        # Should not call any file operations
        mock_parent.get_text_editor.assert_not_called()


class TestSaveFileAction:
    """Test cases for SaveFileAction."""

    def test_save_file_action_initialization(self):
        """Test SaveFileAction initializes correctly."""
        mock_parent = Mock()
        action = SaveFileAction(mock_parent)

        assert action.text() == "&Save\tCtrl+S"

    def test_execute_with_existing_file_path(self):
        """Test saving when file path already exists."""
        mock_parent = Mock()
        mock_parent.get_current_file_path.return_value = "existing.txt"

        action = SaveFileAction(mock_parent)

        with patch.object(action, '_save_to_path', return_value=True) as mock_save:
            result = action.execute()

            mock_save.assert_called_once_with("existing.txt")
            assert result is True

    def test_execute_without_existing_file_path(self):
        """Test saving when no file path exists."""
        mock_parent = Mock()
        mock_parent.get_current_file_path.return_value = ""

        action = SaveFileAction(mock_parent)

        with patch.object(action, '_save_as', return_value=True) as mock_save_as:
            result = action.execute()

            mock_save_as.assert_called_once()
            assert result is True

    @patch('PyQt5.QtWidgets.QFileDialog.getSaveFileName')
    def test_save_as_success(self, mock_get_save_file):
        """Test successful save as operation."""
        mock_get_save_file.return_value = ("newfile.txt", "Text files (*.txt)")

        mock_parent = Mock()
        mock_text_editor = Mock()
        mock_text_editor.get_content.return_value = "test content"
        mock_parent.get_text_editor.return_value = mock_text_editor

        action = SaveFileAction(mock_parent)

        with patch('builtins.open', Mock()) as mock_open:
            mock_file = Mock()
            mock_open.return_value.__enter__.return_value = mock_file

            result = action._save_as()

            assert result is True
            mock_parent.set_current_file_path.assert_called_once_with("newfile.txt")
            mock_parent.set_modified.assert_called_once_with(False)

    @patch('PyQt5.QtWidgets.QFileDialog.getSaveFileName')
    def test_save_as_cancelled(self, mock_get_save_file):
        """Test when user cancels save as dialog."""
        mock_get_save_file.return_value = ("", "")

        mock_parent = Mock()
        action = SaveFileAction(mock_parent)

        result = action._save_as()

        assert result is False


class TestPrintFileAction:
    """Test cases for PrintFileAction."""

    def test_print_file_action_initialization(self):
        """Test PrintFileAction initializes correctly."""
        mock_parent = Mock()
        action = PrintFileAction(mock_parent)

        assert action.text() == "&Print...\tCtrl+P"

    @patch('PyQt5.QtPrintSupport.QPrintDialog')
    @patch('PyQt5.QtPrintSupport.QPrinter')
    def test_execute_print_success(self, mock_printer, mock_print_dialog, qtbot):
        """Test successful printing."""
        mock_dialog_instance = Mock()
        mock_dialog_instance.exec_.return_value = mock_print_dialog.Accepted
        mock_print_dialog.return_value = mock_dialog_instance

        mock_printer_instance = Mock()
        mock_printer.return_value = mock_printer_instance

        mock_parent = Mock()
        mock_text_editor = Mock()
        mock_parent.get_text_editor.return_value = mock_text_editor

        action = PrintFileAction(mock_parent)
        action.execute()

        mock_text_editor.print_document.assert_called_once_with(mock_printer_instance)


class TestExitAppAction:
    """Test cases for ExitAppAction."""

    def test_exit_app_action_initialization(self):
        """Test ExitAppAction initializes correctly."""
        mock_parent = Mock()
        action = ExitAppAction(mock_parent)

        assert action.text() == "E&xit"

    def test_execute_exit_app(self):
        """Test executing exit application."""
        mock_parent = Mock()
        action = ExitAppAction(mock_parent)

        action.execute()

        mock_parent.close.assert_called_once()