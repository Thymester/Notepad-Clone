from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from core.base_action import BaseAction
from ui.icons import ModernIcon


class SaveAsFileAction(BaseAction):
    """
    Action for saving the current file with a new name.
    """

    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            text="Save &As...",
            shortcut=QKeySequence.SaveAs,
            icon=ModernIcon.create_icon("save"),
            tooltip="Save the current file with a new name (Ctrl+Shift+S)",
            status_tip="Save the current file with a new name"
        )

    def execute(self):
        """Execute the save as file action."""
        window = self.get_parent_window()
        text_editor = self.get_text_editor()

        file_path, _ = QFileDialog.getSaveFileName(
            window, 'Save File As', '',
            'Text files (*.txt);;All files (*.*)'
        )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(text_editor.get_content())

                window.set_current_file_path(file_path)
                window.set_modified(False)

                # Update status bar
                window.status_bar.show_message(f"Saved: {file_path}", 2000)
                return True

            except Exception as e:
                QMessageBox.critical(window, "Error", f"Could not save file: {str(e)}")
                return False

        return False