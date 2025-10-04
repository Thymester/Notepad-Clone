import pytest
from unittest.mock import Mock, patch

from core.notepad_window import NotepadWindow, DocumentTab


class TestDocumentTab:
    """Test cases for DocumentTab."""

    def test_document_tab_initialization(self):
        """Test DocumentTab initializes correctly."""
        with patch('PyQt5.QtWidgets.QWidget.__init__'), \
             patch('PyQt5.QtWidgets.QVBoxLayout'), \
             patch('core.text_editor.TextEditor') as mock_text_editor:
            mock_editor_instance = Mock()
            mock_text_editor.return_value = mock_editor_instance

            tab = DocumentTab()

            assert tab.file_path == ""
            assert tab.is_modified == False
            assert tab.text_editor == mock_editor_instance


class TestNotepadWindowTabs:
    """Test cases for tab functionality in NotepadWindow."""

    def test_notepad_window_initialization_with_tabs(self):
        """Test NotepadWindow initializes with tab widget."""
        with patch('PyQt5.QtWidgets.QMainWindow.__init__'), \
             patch('PyQt5.QtWidgets.QTabWidget') as mock_tab_widget, \
             patch('core.notepad_window.MenuBar'), \
             patch('core.notepad_window.ToolBar'), \
             patch('core.notepad_window.StatusBar'), \
             patch.object(NotepadWindow, 'new_document'), \
             patch.object(NotepadWindow, 'init_ui'), \
             patch.object(NotepadWindow, 'connect_signals'), \
             patch.object(NotepadWindow, 'load_settings'):

            mock_tab_instance = Mock()
            mock_tab_widget.return_value = mock_tab_instance

            window = NotepadWindow()

            assert hasattr(window, 'tab_widget')
            mock_tab_instance.setTabsClosable.assert_called_once_with(True)

    def test_new_document_creates_tab(self):
        """Test new_document creates a new tab."""
        with patch('PyQt5.QtWidgets.QMainWindow.__init__'), \
             patch('PyQt5.QtWidgets.QTabWidget'), \
             patch('core.notepad_window.MenuBar'), \
             patch('core.notepad_window.ToolBar'), \
             patch('core.notepad_window.StatusBar'), \
             patch('core.notepad_window.DocumentTab') as mock_doc_tab, \
             patch.object(NotepadWindow, 'init_ui'), \
             patch.object(NotepadWindow, 'connect_signals'), \
             patch.object(NotepadWindow, 'load_settings'), \
             patch.object(NotepadWindow, 'update_tab_title'):

            mock_tab_widget = Mock()
            mock_doc_tab_instance = Mock()
            mock_doc_tab.return_value = mock_doc_tab_instance

            window = NotepadWindow()
            window.tab_widget = mock_tab_widget

            window.new_document()

            mock_doc_tab.assert_called_once()
            mock_tab_widget.addTab.assert_called_once_with(mock_doc_tab_instance, "Untitled")

    def test_close_tab_with_multiple_tabs(self):
        """Test closing a tab when multiple tabs exist."""
        with patch('PyQt5.QtWidgets.QMainWindow.__init__'), \
             patch('PyQt5.QtWidgets.QTabWidget'), \
             patch('core.notepad_window.MenuBar'), \
             patch('core.notepad_window.ToolBar'), \
             patch('core.notepad_window.StatusBar'), \
             patch.object(NotepadWindow, 'init_ui'), \
             patch.object(NotepadWindow, 'connect_signals'), \
             patch.object(NotepadWindow, 'load_settings'):

            mock_tab_widget = Mock()
            mock_tab_widget.count.return_value = 3  # Multiple tabs

            window = NotepadWindow()
            window.tab_widget = mock_tab_widget

            window.close_tab(1)

            mock_tab_widget.removeTab.assert_called_once_with(1)

    def test_close_last_tab_clears_content(self):
        """Test closing the last tab clears content instead of removing."""
        with patch('PyQt5.QtWidgets.QMainWindow.__init__'), \
             patch('PyQt5.QtWidgets.QTabWidget'), \
             patch('core.notepad_window.MenuBar'), \
             patch('core.notepad_window.ToolBar'), \
             patch('core.notepad_window.StatusBar'), \
             patch.object(NotepadWindow, 'init_ui'), \
             patch.object(NotepadWindow, 'connect_signals'), \
             patch.object(NotepadWindow, 'load_settings'), \
             patch.object(NotepadWindow, 'update_tab_title'):

            mock_tab_widget = Mock()
            mock_tab_widget.count.return_value = 1  # Only one tab
            mock_tab = Mock()
            mock_tab_widget.widget.return_value = mock_tab

            window = NotepadWindow()
            window.tab_widget = mock_tab_widget

            window.close_tab(0)

            # Should clear content instead of removing tab
            mock_tab.text_editor.clear_content.assert_called_once()
            assert mock_tab.is_modified == False
            assert mock_tab.file_path == ""
            mock_tab_widget.removeTab.assert_not_called()

    def test_get_current_tab(self):
        """Test getting the current document tab."""
        with patch('PyQt5.QtWidgets.QMainWindow.__init__'), \
             patch('PyQt5.QtWidgets.QTabWidget'), \
             patch('core.notepad_window.MenuBar'), \
             patch('core.notepad_window.ToolBar'), \
             patch('core.notepad_window.StatusBar'), \
             patch.object(NotepadWindow, 'init_ui'), \
             patch.object(NotepadWindow, 'connect_signals'), \
             patch.object(NotepadWindow, 'load_settings'):

            mock_tab_widget = Mock()
            mock_tab = Mock()
            mock_tab_widget.currentWidget.return_value = mock_tab

            window = NotepadWindow()
            window.tab_widget = mock_tab_widget

            result = window.get_current_tab()

            assert result == mock_tab

    def test_text_editor_property(self):
        """Test the text_editor property returns current tab's editor."""
        with patch('PyQt5.QtWidgets.QMainWindow.__init__'), \
             patch('PyQt5.QtWidgets.QTabWidget'), \
             patch('core.notepad_window.MenuBar'), \
             patch('core.notepad_window.ToolBar'), \
             patch('core.notepad_window.StatusBar'), \
             patch.object(NotepadWindow, 'init_ui'), \
             patch.object(NotepadWindow, 'connect_signals'), \
             patch.object(NotepadWindow, 'load_settings'):

            mock_tab_widget = Mock()
            mock_tab = Mock()
            mock_editor = Mock()
            mock_tab.text_editor = mock_editor
            mock_tab_widget.currentWidget.return_value = mock_tab

            window = NotepadWindow()
            window.tab_widget = mock_tab_widget

            result = window.text_editor

            assert result == mock_editor

    def test_set_current_file_path(self):
        """Test setting current file path for current tab."""
        with patch('PyQt5.QtWidgets.QMainWindow.__init__'), \
             patch('PyQt5.QtWidgets.QTabWidget'), \
             patch('core.notepad_window.MenuBar'), \
             patch('core.notepad_window.ToolBar'), \
             patch('core.notepad_window.StatusBar'), \
             patch.object(NotepadWindow, 'init_ui'), \
             patch.object(NotepadWindow, 'connect_signals'), \
             patch.object(NotepadWindow, 'load_settings'), \
             patch.object(NotepadWindow, 'update_current_tab_title'), \
             patch.object(NotepadWindow, 'update_title'):

            mock_tab_widget = Mock()
            mock_tab = Mock()
            mock_tab_widget.currentWidget.return_value = mock_tab

            window = NotepadWindow()
            window.tab_widget = mock_tab_widget

            window.set_current_file_path("/path/to/file.txt")

            assert mock_tab.file_path == "/path/to/file.txt"
            assert mock_tab.is_modified == False

    def test_set_modified(self):
        """Test setting modification status for current tab."""
        with patch('PyQt5.QtWidgets.QMainWindow.__init__'), \
             patch('PyQt5.QtWidgets.QTabWidget'), \
             patch('core.notepad_window.MenuBar'), \
             patch('core.notepad_window.ToolBar'), \
             patch('core.notepad_window.StatusBar'), \
             patch.object(NotepadWindow, 'init_ui'), \
             patch.object(NotepadWindow, 'connect_signals'), \
             patch.object(NotepadWindow, 'load_settings'), \
             patch.object(NotepadWindow, 'update_current_tab_title'), \
             patch.object(NotepadWindow, 'update_title'):

            mock_tab_widget = Mock()
            mock_tab = Mock()
            mock_tab_widget.currentWidget.return_value = mock_tab

            window = NotepadWindow()
            window.tab_widget = mock_tab_widget

            window.set_modified(True)

            assert mock_tab.is_modified == True

    def test_is_document_modified(self):
        """Test checking if current document is modified."""
        with patch('PyQt5.QtWidgets.QMainWindow.__init__'), \
             patch('PyQt5.QtWidgets.QTabWidget'), \
             patch('core.notepad_window.MenuBar'), \
             patch('core.notepad_window.ToolBar'), \
             patch('core.notepad_window.ToolBar'), \
             patch('core.notepad_window.StatusBar'), \
             patch.object(NotepadWindow, 'init_ui'), \
             patch.object(NotepadWindow, 'connect_signals'), \
             patch.object(NotepadWindow, 'load_settings'):

            mock_tab_widget = Mock()
            mock_tab = Mock()
            mock_tab.is_modified = True
            mock_tab_widget.currentWidget.return_value = mock_tab

            window = NotepadWindow()
            window.tab_widget = mock_tab_widget

            result = window.is_document_modified()

            assert result == True

    def test_get_current_file_path(self):
        """Test getting current file path from current tab."""
        with patch('PyQt5.QtWidgets.QMainWindow.__init__'), \
             patch('PyQt5.QtWidgets.QTabWidget'), \
             patch('core.notepad_window.MenuBar'), \
             patch('core.notepad_window.ToolBar'), \
             patch('core.notepad_window.StatusBar'), \
             patch.object(NotepadWindow, 'init_ui'), \
             patch.object(NotepadWindow, 'connect_signals'), \
             patch.object(NotepadWindow, 'load_settings'):

            mock_tab_widget = Mock()
            mock_tab = Mock()
            mock_tab.file_path = "/test/path/file.txt"
            mock_tab_widget.currentWidget.return_value = mock_tab

            window = NotepadWindow()
            window.tab_widget = mock_tab_widget

            result = window.get_current_file_path()

            assert result == "/test/path/file.txt"