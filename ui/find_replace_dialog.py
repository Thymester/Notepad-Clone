from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QCheckBox, QMessageBox


class FindReplaceDialog(QDialog):
    """
    A dialog for finding and replacing text in the notepad application.
    """

    def __init__(self, parent=None):
        """
        Initialize the find and replace dialog.

        Args:
            parent: The parent widget (typically the main notepad window)
        """
        super().__init__(parent)
        self.parent_editor = parent
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface components."""
        self.setWindowTitle("Find and Replace")
        self.setFixedSize(400, 200)
        layout = QVBoxLayout()

        # Find section
        find_layout = QHBoxLayout()
        find_layout.addWidget(QLabel("Find:"))
        self.find_input = QLineEdit()
        find_layout.addWidget(self.find_input)
        layout.addLayout(find_layout)

        # Replace section
        replace_layout = QHBoxLayout()
        replace_layout.addWidget(QLabel("Replace:"))
        self.replace_input = QLineEdit()
        replace_layout.addWidget(self.replace_input)
        layout.addLayout(replace_layout)

        # Options
        self.match_case = QCheckBox("Match case")
        self.wrap_around = QCheckBox("Wrap around")
        self.wrap_around.setChecked(True)
        layout.addWidget(self.match_case)
        layout.addWidget(self.wrap_around)

        # Buttons
        button_layout = QHBoxLayout()
        self.find_next_btn = QPushButton("Find Next")
        self.replace_btn = QPushButton("Replace")
        self.replace_all_btn = QPushButton("Replace All")
        self.cancel_btn = QPushButton("Cancel")

        button_layout.addWidget(self.find_next_btn)
        button_layout.addWidget(self.replace_btn)
        button_layout.addWidget(self.replace_all_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Connect signals
        self.find_next_btn.clicked.connect(self.find_next)
        self.replace_btn.clicked.connect(self.replace_current)
        self.replace_all_btn.clicked.connect(self.replace_all)
        self.cancel_btn.clicked.connect(self.close)

    def find_next(self):
        """Find the next occurrence of the search text."""
        if self.parent_editor:
            self.parent_editor.find_text_advanced(
                self.find_input.text(),
                self.match_case.isChecked(),
                self.wrap_around.isChecked()
            )

    def replace_current(self):
        """Replace the currently selected text."""
        if self.parent_editor:
            self.parent_editor.replace_current_selection(
                self.find_input.text(),
                self.replace_input.text(),
                self.match_case.isChecked()
            )

    def replace_all(self):
        """Replace all occurrences of the search text."""
        if self.parent_editor:
            count = self.parent_editor.replace_all_text(
                self.find_input.text(),
                self.replace_input.text(),
                self.match_case.isChecked()
            )
            QMessageBox.information(self, "Replace All", f"Replaced {count} occurrences.")