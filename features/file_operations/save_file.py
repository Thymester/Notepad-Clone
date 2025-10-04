from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from core.base_action import BaseAction
from ui.icons import ModernIcon


class SaveFileAction(BaseAction):
    """
    Action for saving the current file.
    """

    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            text="&Save",
            shortcut=QKeySequence.Save,
            icon=ModernIcon.create_icon("save"),
            tooltip="Save the current file (Ctrl+S)",
            status_tip="Save the current file"
        )

    def execute(self):
        """Execute the save file action."""
        window = self.get_parent_window()
        text_editor = self.get_text_editor()

        if window.get_current_file_path():
            # Save to existing file
            return self._save_to_path(window.get_current_file_path())
        else:
            # Save as new file
            return self._save_as()

    def _save_as(self):
        """Show save as dialog and save file."""
        window = self.get_parent_window()
        text_editor = self.get_text_editor()

        file_path, _ = QFileDialog.getSaveFileName(
            window, 'Save File', '',
            'Text files (*.txt);;All files (*.*)'
        )

        if file_path:
            # Ensure correct extension
            if not file_path.endswith('.txt'):
                file_path += '.txt'

            return self._save_to_path(file_path)
        return False

    def _save_to_path(self, file_path):
        """Save content to the specified file path."""
        window = self.get_parent_window()
        text_editor = self.get_text_editor()

        try:
            content = text_editor.get_content()

            # Save as plain text
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)

            window.set_current_file_path(file_path)
            window.set_modified(False)

            # Update status bar
            window.status_bar.show_message(f"Saved file: {file_path}", 2000)
            return True

        except Exception as e:
            QMessageBox.critical(window, "Error", f"Could not save file: {str(e)}")
            return False