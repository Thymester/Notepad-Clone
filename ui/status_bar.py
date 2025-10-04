from PyQt5.QtWidgets import QStatusBar, QLabel


class StatusBar:
    """
    Custom status bar for the notepad application.
    """

    def __init__(self, parent=None):
        self.parent_window = parent
        self.status_bar = QStatusBar(parent)

        # Create labels
        self.line_col_label = QLabel("Line 1, Column 1")
        self.word_count_label = QLabel("Words: 0")
        self.char_count_label = QLabel("Chars: 0")
        self.line_count_label = QLabel("Lines: 1")
        self.zoom_label = QLabel("100%")

        # Add permanent widgets
        self.status_bar.addPermanentWidget(self.line_col_label)
        self.status_bar.addPermanentWidget(self.word_count_label)
        self.status_bar.addPermanentWidget(self.char_count_label)
        self.status_bar.addPermanentWidget(self.line_count_label)
        self.status_bar.addPermanentWidget(self.zoom_label)

    def update_cursor_position(self):
        """Update the cursor position display."""
        if hasattr(self.parent_window, 'text_editor'):
            line, col = self.parent_window.text_editor.get_cursor_position()
            self.line_col_label.setText(f"Line {line}, Column {col}")

    def update_word_count(self):
        """Update the word count display."""
        if hasattr(self.parent_window, 'text_editor'):
            text = self.parent_window.text_editor.get_content()
            words = len(text.split()) if text.strip() else 0
            self.word_count_label.setText(f"Words: {words}")

    def update_char_count(self):
        """Update the character count display."""
        if hasattr(self.parent_window, 'text_editor'):
            text = self.parent_window.text_editor.get_content()
            chars = len(text)
            self.char_count_label.setText(f"Chars: {chars}")

    def update_line_count(self):
        """Update the line count display."""
        if hasattr(self.parent_window, 'text_editor'):
            lines = self.parent_window.text_editor.get_line_count()
            self.line_count_label.setText(f"Lines: {lines}")

    def update_zoom_label(self, zoom_level):
        """Update the zoom level display."""
        self.zoom_label.setText(f"{zoom_level}%")

    def show_message(self, message, timeout=0):
        """Show a message in the status bar."""
        self.status_bar.showMessage(message, timeout)