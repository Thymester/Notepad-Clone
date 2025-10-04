import pytest
from unittest.mock import Mock, patch

from core.text_editor import TextEditor


class TestTextEditor:
    """Test cases for the TextEditor class."""

    def test_text_editor_initialization(self, qtbot):
        """Test that TextEditor initializes correctly."""
        editor = TextEditor()
        qtbot.addWidget(editor)

        assert editor.lineWrapMode().name == "WidgetWidth"
        assert editor.toPlainText() == ""

    def test_set_editor_font(self, qtbot):
        """Test setting the editor font."""
        editor = TextEditor()
        qtbot.addWidget(editor)

        mock_font = Mock()
        editor.set_editor_font(mock_font)

        # Verify font was set
        assert editor.font() == mock_font

    def test_get_content(self, qtbot):
        """Test getting content from the editor."""
        editor = TextEditor()
        qtbot.addWidget(editor)

        test_text = "Hello, World!"
        editor.setPlainText(test_text)

        assert editor.get_content() == test_text

    def test_set_content(self, qtbot):
        """Test setting content in the editor."""
        editor = TextEditor()
        qtbot.addWidget(editor)

        test_text = "Test content"
        editor.set_content(test_text)

        assert editor.toPlainText() == test_text

    def test_clear_content(self, qtbot):
        """Test clearing content from the editor."""
        editor = TextEditor()
        qtbot.addWidget(editor)

        editor.setPlainText("Some content")
        editor.clear_content()

        assert editor.toPlainText() == ""

    def test_get_cursor_position(self, qtbot):
        """Test getting cursor position."""
        editor = TextEditor()
        qtbot.addWidget(editor)

        editor.setPlainText("Line 1\nLine 2\nLine 3")
        cursor = editor.textCursor()
        cursor.setPosition(7)  # Position at "L" in "Line 2"
        editor.setTextCursor(cursor)

        line, col = editor.get_cursor_position()

        assert line == 2  # Second line (1-indexed)
        assert col == 1  # First character (1-indexed)

    def test_set_cursor_position(self, qtbot):
        """Test setting cursor position."""
        editor = TextEditor()
        qtbot.addWidget(editor)

        editor.setPlainText("Line 1\nLine 2\nLine 3")
        editor.set_cursor_position(2, 3)  # Line 2, column 3

        cursor = editor.textCursor()
        assert cursor.blockNumber() + 1 == 2
        assert cursor.columnNumber() + 1 == 3

    def test_get_line_count(self, qtbot):
        """Test getting line count."""
        editor = TextEditor()
        qtbot.addWidget(editor)

        # Single line
        assert editor.get_line_count() == 1

        # Multiple lines
        editor.setPlainText("Line 1\nLine 2\nLine 3")
        assert editor.get_line_count() == 3

    def test_insert_text_at_cursor(self, qtbot):
        """Test inserting text at cursor position."""
        editor = TextEditor()
        qtbot.addWidget(editor)

        editor.setPlainText("Hello World")
        cursor = editor.textCursor()
        cursor.setPosition(6)  # After "Hello "
        editor.setTextCursor(cursor)

        editor.insert_text_at_cursor("Beautiful ")

        assert editor.toPlainText() == "Hello Beautiful World"

    def test_select_all_text(self, qtbot):
        """Test selecting all text."""
        editor = TextEditor()
        qtbot.addWidget(editor)

        editor.setPlainText("Test text")
        editor.select_all_text()

        cursor = editor.textCursor()
        assert cursor.hasSelection()
        assert cursor.selectedText() == "Test text"

    def test_has_selection(self, qtbot):
        """Test checking if text is selected."""
        editor = TextEditor()
        qtbot.addWidget(editor)

        editor.setPlainText("Test text")

        # No selection
        assert not editor.has_selection()

        # With selection
        editor.selectAll()
        assert editor.has_selection()

    def test_get_selected_text(self, qtbot):
        """Test getting selected text."""
        editor = TextEditor()
        qtbot.addWidget(editor)

        editor.setPlainText("Hello World")
        cursor = editor.textCursor()
        cursor.setPosition(0)
        cursor.setPosition(5, cursor.KeepAnchor)  # Select "Hello"
        editor.setTextCursor(cursor)

        assert editor.get_selected_text() == "Hello"

    def test_delete_selected_text(self, qtbot):
        """Test deleting selected text."""
        editor = TextEditor()
        qtbot.addWidget(editor)

        editor.setPlainText("Hello World")
        cursor = editor.textCursor()
        cursor.setPosition(6)
        cursor.setPosition(11, cursor.KeepAnchor)  # Select "World"
        editor.setTextCursor(cursor)

        editor.delete_selected_text()

        assert editor.toPlainText() == "Hello "

    def test_goto_line(self, qtbot):
        """Test going to a specific line."""
        editor = TextEditor()
        qtbot.addWidget(editor)

        editor.setPlainText("Line 1\nLine 2\nLine 3")
        editor.goto_line(2)  # Go to line 2

        cursor = editor.textCursor()
        assert cursor.blockNumber() + 1 == 2

    @patch('core.text_editor.QTextDocument')
    def test_find_text(self, mock_qtextdocument, qtbot):
        """Test finding text in the document."""
        editor = TextEditor()
        qtbot.addWidget(editor)

        editor.setPlainText("Hello World")

        # Mock the document and find method
        mock_document = Mock()
        mock_cursor = Mock()
        mock_cursor.isNull.return_value = False
        mock_document.find.return_value = mock_cursor

        with patch.object(editor, 'document', return_value=mock_document):
            result = editor.find_text("World")

            assert result == mock_cursor
            mock_document.find.assert_called_once()

    @patch('core.text_editor.QTextDocument')
    def test_replace_selected_text(self, mock_qtextdocument, qtbot):
        """Test replacing selected text."""
        editor = TextEditor()
        qtbot.addWidget(editor)

        editor.setPlainText("Hello World")
        cursor = editor.textCursor()
        cursor.setPosition(6)
        cursor.setPosition(11, cursor.KeepAnchor)  # Select "World"
        editor.setTextCursor(cursor)

        editor.replace_selected_text("Universe")

        assert editor.toPlainText() == "Hello Universe"

    def test_get_document(self, qtbot):
        """Test getting the document."""
        editor = TextEditor()
        qtbot.addWidget(editor)

        document = editor.get_document()
        assert document is not None
        assert document == editor.document()

    @patch('core.text_editor.QPlainTextEdit.print_')
    def test_print_document(self, mock_print, qtbot):
        """Test printing the document."""
        editor = TextEditor()
        qtbot.addWidget(editor)

        mock_printer = Mock()
        editor.print_document(mock_printer)

        mock_print.assert_called_once_with(mock_printer)

    def test_context_menu_event_creates_standard_menu(self):
        """Test contextMenuEvent creates and shows standard context menu."""
        # Create a mock editor that has the contextMenuEvent method
        editor = Mock(spec=TextEditor)
        editor.createStandardContextMenu = Mock()
        editor.parent = Mock()
        editor.contextMenuEvent = TextEditor.contextMenuEvent.__get__(editor, TextEditor)

        mock_menu = Mock()
        editor.createStandardContextMenu.return_value = mock_menu
        editor.parent.return_value = Mock()

        # Create mock event
        mock_event = Mock()
        mock_event.globalPos.return_value = Mock()

        # Call contextMenuEvent
        editor.contextMenuEvent(mock_event)

        # Verify standard context menu was created
        editor.createStandardContextMenu.assert_called_once()

        # Verify menu was shown at correct position
        mock_menu.exec_.assert_called_once_with(mock_event.globalPos.return_value)

        # Verify event was accepted
        mock_event.accept.assert_called_once()

    def test_context_menu_event_applies_parent_stylesheet(self):
        """Test contextMenuEvent applies parent's stylesheet to the menu."""
        # Create a mock editor that has the contextMenuEvent method
        editor = Mock(spec=TextEditor)
        editor.createStandardContextMenu = Mock()
        editor.parent = Mock()
        editor.contextMenuEvent = TextEditor.contextMenuEvent.__get__(editor, TextEditor)

        mock_menu = Mock()
        editor.createStandardContextMenu.return_value = mock_menu

        mock_parent_instance = Mock()
        mock_parent_instance.styleSheet.return_value = "test_stylesheet"
        editor.parent.return_value = mock_parent_instance

        # Create mock event
        mock_event = Mock()
        mock_event.globalPos.return_value = Mock()

        # Call contextMenuEvent
        editor.contextMenuEvent(mock_event)

        # Verify stylesheet was applied to menu
        mock_menu.setStyleSheet.assert_called_once_with("test_stylesheet")

    def test_context_menu_event_handles_no_parent_stylesheet(self):
        """Test contextMenuEvent handles case when parent has no stylesheet."""
        # Create a mock editor that has the contextMenuEvent method
        editor = Mock(spec=TextEditor)
        editor.createStandardContextMenu = Mock()
        editor.parent = Mock()
        editor.contextMenuEvent = TextEditor.contextMenuEvent.__get__(editor, TextEditor)

        mock_menu = Mock()
        editor.createStandardContextMenu.return_value = mock_menu

        mock_parent_instance = Mock()
        mock_parent_instance.styleSheet.return_value = ""
        editor.parent.return_value = mock_parent_instance

        # Create mock event
        mock_event = Mock()
        mock_event.globalPos.return_value = Mock()

        # Call contextMenuEvent
        editor.contextMenuEvent(mock_event)

        # Verify setStyleSheet was not called with empty stylesheet
        mock_menu.setStyleSheet.assert_not_called()

    def test_context_menu_event_handles_no_parent(self):
        """Test contextMenuEvent handles case when there is no parent."""
        # Create a mock editor that has the contextMenuEvent method
        editor = Mock(spec=TextEditor)
        editor.createStandardContextMenu = Mock()
        editor.parent = Mock()
        editor.contextMenuEvent = TextEditor.contextMenuEvent.__get__(editor, TextEditor)

        mock_menu = Mock()
        editor.createStandardContextMenu.return_value = mock_menu
        editor.parent.return_value = None

        # Create mock event
        mock_event = Mock()
        mock_event.globalPos.return_value = Mock()

        # Call contextMenuEvent
        editor.contextMenuEvent(mock_event)

        # Verify setStyleSheet was not called
        mock_menu.setStyleSheet.assert_not_called()