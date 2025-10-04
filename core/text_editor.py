from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtGui import QFont, QContextMenuEvent
from PyQt5.QtCore import QPoint
from core.syntax_highlighter import SyntaxHighlighter


class TextEditor(QPlainTextEdit):
    """
    Custom text editor widget with enhanced functionality.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLineWrapMode(QPlainTextEdit.WidgetWidth)
        self.setFont(QFont("Segoe UI", 11))
        self.syntax_highlighter = None
        self.current_language = None

    def set_editor_font(self, font):
        """Set the font for the text editor."""
        self.setFont(font)

    def get_content(self):
        """Get the current text content."""
        return self.toPlainText()

    def set_content(self, content):
        """Set the text content."""
        self.setPlainText(content)

    def clear_content(self):
        """Clear all text content."""
        self.clear()

    def get_cursor_position(self):
        """Get the current cursor position (line, column)."""
        cursor = self.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber() + 1
        return line, col

    def set_cursor_position(self, line, column):
        """Set the cursor position."""
        cursor = self.textCursor()
        cursor.setPosition(0)  # Start from beginning
        for _ in range(line - 1):
            cursor.movePosition(cursor.Down)
        for _ in range(column - 1):
            cursor.movePosition(cursor.Right)
        self.setTextCursor(cursor)

    def goto_line(self, line_number):
        """Go to a specific line number."""
        cursor = self.textCursor()
        cursor.setPosition(0)  # Start from beginning
        for _ in range(line_number - 1):
            cursor.movePosition(cursor.Down)
        self.setTextCursor(cursor)

    def get_line_count(self):
        """Get the total number of lines."""
        return self.document().blockCount()

    def insert_text_at_cursor(self, text):
        """Insert text at the current cursor position."""
        cursor = self.textCursor()
        cursor.insertText(text)

    def get_selected_text(self):
        """Get the currently selected text."""
        return self.textCursor().selectedText()

    def has_selection(self):
        """Check if there is selected text."""
        return self.textCursor().hasSelection()

    def select_all_text(self):
        """Select all text in the editor."""
        self.selectAll()

    def delete_selected_text(self):
        """Delete the currently selected text."""
        cursor = self.textCursor()
        if cursor.hasSelection():
            cursor.removeSelectedText()
        else:
            cursor.deleteChar()

    def find_text(self, text, start_position=0, flags=None):
        """Find text in the document."""
        if flags is None:
            flags = []
        cursor = self.textCursor()
        cursor.setPosition(start_position)
        found_cursor = self.document().find(text, cursor, flags)
        return found_cursor

    def replace_selected_text(self, replacement_text):
        """Replace the currently selected text."""
        cursor = self.textCursor()
        cursor.insertText(replacement_text)

    def get_document(self):
        """Get the underlying document."""
        return self.document()

    def print_document(self, printer):
        """Print the document."""
        self.print_(printer)

    def enable_syntax_highlighting(self, language="python"):
        """Enable syntax highlighting for the specified language."""
        if self.syntax_highlighter:
            self.syntax_highlighter.set_language(language)
        else:
            self.syntax_highlighter = SyntaxHighlighter(self.document(), language)
        self.current_language = language

    def disable_syntax_highlighting(self):
        """Disable syntax highlighting."""
        if self.syntax_highlighter:
            self.syntax_highlighter.setDocument(None)
            self.syntax_highlighter = None
            self.current_language = None

    def is_syntax_highlighting_enabled(self):
        """Check if syntax highlighting is enabled."""
        return self.syntax_highlighter is not None

    def get_current_language(self):
        """Get the current syntax highlighting language."""
        return self.current_language

    def contextMenuEvent(self, event):
        """Handle context menu events to ensure proper theming."""
        # Create the standard context menu
        menu = self.createStandardContextMenu()
        
        # Apply the application's stylesheet to ensure proper theming
        if self.parent() and hasattr(self.parent(), 'styleSheet'):
            app_stylesheet = self.parent().styleSheet()
            if app_stylesheet:
                menu.setStyleSheet(app_stylesheet)
        
        # Show the menu at the cursor position
        menu.exec_(event.globalPos())
        event.accept()