from PyQt5.QtGui import QKeySequence

from core.base_action import BaseAction
from ui.icons import ModernIcon


class NewFileAction(BaseAction):
    """
    Action for creating a new file.
    """

    def __init__(self, parent=None, is_new_window=False):
        text = "&New" if not is_new_window else "New &Window"
        shortcut = QKeySequence.New if not is_new_window else QKeySequence("Ctrl+Shift+N")
        tooltip = "Create a new file (Ctrl+N)" if not is_new_window else "Open a new window (Ctrl+Shift+N)"

        super().__init__(
            parent=parent,
            text=text,
            shortcut=shortcut,
            icon=ModernIcon.create_icon("new"),
            tooltip=tooltip,
            status_tip="Create a new file" if not is_new_window else "Open a new window"
        )
        self.is_new_window = is_new_window

    def execute(self):
        """Execute the new file action."""
        if self.is_new_window:
            # Create a new window
            from core.notepad_window import NotepadWindow
            new_window = NotepadWindow()
            new_window.show()
        else:
            # Create new document tab in current window
            window = self.get_parent_window()
            window.new_document()

    def _check_save_changes(self):
        """Check if there are unsaved changes and prompt user."""
        window = self.get_parent_window()
        if window.is_document_modified():
            from PyQt5.QtWidgets import QMessageBox
            reply = QMessageBox.question(
                window, "Modern Notepad",
                "Do you want to save changes to this file?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Save
            )

            if reply == QMessageBox.Save:
                return self._save_current_file()
            elif reply == QMessageBox.Cancel:
                return False

        return True

    def _save_current_file(self):
        """Save the current file."""
        from features.file_operations.save_file import SaveFileAction
        save_action = SaveFileAction(self.get_parent_window())
        return save_action.execute()