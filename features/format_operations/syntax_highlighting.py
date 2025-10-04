from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QCheckBox
from PyQt5.QtCore import Qt

from core.base_action import BaseAction


class SyntaxHighlightingAction(BaseAction):
    """
    Action for toggling syntax highlighting.
    """

    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            text="Syntax &Highlighting...",
            tooltip="Enable syntax highlighting for code",
            status_tip="Enable syntax highlighting for code"
        )
        self.languages = ["None", "Python", "JavaScript", "C++"]
        self.load_syntax_highlighting_setting()

    def execute(self):
        """Execute the syntax highlighting action."""
        dialog = SyntaxHighlightingDialog(self.get_parent_window())
        if dialog.exec_() == QDialog.Accepted:
            language = dialog.get_selected_language()
            self.save_syntax_highlighting_setting(language)
            text_editor = self.get_text_editor()

            if language == "None":
                text_editor.disable_syntax_highlighting()
            else:
                text_editor.enable_syntax_highlighting(language.lower())

    def load_syntax_highlighting_setting(self):
        """Load syntax highlighting setting from persistent storage."""
        try:
            from PyQt5.QtCore import QSettings
            settings = QSettings("ModernNotepad", "SyntaxHighlighting")
            language = settings.value("language", "None", type=str)
            if language != "None":
                text_editor = self.get_text_editor()
                if text_editor:
                    text_editor.enable_syntax_highlighting(language.lower())
        except Exception:
            # If loading fails, default to no highlighting
            pass

    def save_syntax_highlighting_setting(self, language):
        """Save syntax highlighting setting to persistent storage."""
        try:
            from PyQt5.QtCore import QSettings
            settings = QSettings("ModernNotepad", "SyntaxHighlighting")
            settings.setValue("language", language)
            settings.sync()  # Ensure immediate write
        except Exception:
            # If saving fails, continue without error
            pass


class SyntaxHighlightingDialog(QDialog):
    """
    Dialog for selecting syntax highlighting options.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Syntax Highlighting")
        self.setModal(True)
        self.resize(300, 150)

        self.setup_ui()

        # Apply dark theme styling to match the app
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
                border: 1px solid #3c3c3c;
                border-radius: 8px;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0b5ed7;
            }
            QPushButton:pressed {
                background-color: #0a58ca;
            }
        """)

    def setup_ui(self):
        """Setup the dialog UI."""
        layout = QVBoxLayout()

        # Language selection
        language_layout = QHBoxLayout()
        language_layout.addWidget(QLabel("Language:"))
        self.language_combo = QComboBox()
        self.language_combo.addItems(["None", "Python", "JavaScript", "C++"])
        # Apply dark theme styling to match the app
        self.language_combo.setStyleSheet("""
            QComboBox {
                background-color: #1e1e1e;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                padding: 4px;
                color: #ffffff;
                min-width: 120px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid #ffffff;
                margin-right: 8px;
            }
            QComboBox QAbstractItemView {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #3c3c3c;
                selection-background-color: #3c3c3c;
                selection-color: #ffffff;
            }
        """)
        language_layout.addWidget(self.language_combo)
        layout.addLayout(language_layout)

        # Current status
        self.status_label = QLabel("Syntax highlighting is currently disabled")
        layout.addWidget(self.status_label)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        button_layout.addWidget(self.ok_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Update status based on current state
        self.update_status()

    def update_status(self):
        """Update the status label based on current syntax highlighting state."""
        parent_window = self.parent()
        if parent_window and hasattr(parent_window, 'text_editor'):
            text_editor = parent_window.text_editor
            if text_editor.is_syntax_highlighting_enabled():
                language = text_editor.get_current_language()
                self.status_label.setText(f"Syntax highlighting is enabled for {language.title()}")
                # Set current language in combo
                if language == "python":
                    self.language_combo.setCurrentText("Python")
                elif language == "javascript":
                    self.language_combo.setCurrentText("JavaScript")
                elif language == "cpp":
                    self.language_combo.setCurrentText("C++")
            else:
                self.status_label.setText("Syntax highlighting is currently disabled")
                self.language_combo.setCurrentText("None")

    def get_selected_language(self):
        """Get the selected language from the combo box."""
        return self.language_combo.currentText()