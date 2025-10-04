from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from core.base_action import BaseAction
from ui.icons import ModernIcon
from ui.password_dialog import PasswordPromptDialog
from utils.security.encryption import EncryptionService, InvalidPasswordError


class OpenFileAction(BaseAction):
    """
    Action for opening an existing file.
    """

    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            text="&Open...",
            shortcut=QKeySequence.Open,
            icon=ModernIcon.create_icon("open"),
            tooltip="Open an existing file (Ctrl+O)",
            status_tip="Open an existing file"
        )
        self.encryption_service = EncryptionService()

    def execute(self):
        """Execute the open file action."""
        window = self.get_parent_window()
        text_editor = self.get_text_editor()

        # Check if current document needs saving
        if not self._check_save_changes():
            return

        file_path, _ = QFileDialog.getOpenFileName(
            window, 'Open File', '',
            'All files (*.*);;Text files (*.txt);;Encrypted files (*.enc)'
        )

        if file_path:
            self._open_file(file_path)

    def _open_file(self, file_path):
        """Open the file at the specified path."""
        window = self.get_parent_window()
        text_editor = self.get_text_editor()

        try:
            # Check if file is encrypted
            if self.encryption_service.is_encrypted_file(file_path):
                content = self._open_encrypted_file(file_path)
                if content is None:
                    return  # User cancelled or wrong password
            else:
                # Open as plain text
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

            text_editor.set_content(content)
            window.set_current_file_path(file_path)
            window.set_modified(False)

            # Add to recent files
            if hasattr(window, 'menu_bar') and hasattr(window.menu_bar, 'recent_files_action'):
                window.menu_bar.recent_files_action.add_recent_file(file_path)

            # Update status bar
            file_type = "encrypted" if self.encryption_service.is_encrypted_file(file_path) else "plain text"
            window.status_bar.show_message(f"Opened {file_type} file: {file_path}", 2000)

        except Exception as e:
            QMessageBox.critical(window, "Error", f"Could not open file: {str(e)}")

    def _open_encrypted_file(self, file_path):
        """Open and decrypt an encrypted file."""
        window = self.get_parent_window()

        # Prompt for password
        password_dialog = PasswordPromptDialog(window, "Enter Password to Decrypt")
        if password_dialog.exec_() != PasswordPromptDialog.Accepted:
            return None

        password = password_dialog.get_password()
        if not password:
            QMessageBox.warning(window, "Error", "Password cannot be empty.")
            return None

        try:
            # Read encrypted data
            with open(file_path, 'rb') as file:
                encrypted_data = file.read()

            # Decrypt
            content = self.encryption_service.decrypt_data(encrypted_data, password)
            return content

        except InvalidPasswordError:
            QMessageBox.critical(window, "Error", "Incorrect password. Cannot decrypt file.")
            return None
        except Exception as e:
            QMessageBox.critical(window, "Error", f"Failed to decrypt file: {str(e)}")
            return None

    def _check_save_changes(self):
        """Check if there are unsaved changes and prompt user."""
        window = self.get_parent_window()
        if window.is_document_modified():
            reply = QMessageBox.question(
                window, "Modern Notepad",
                "Do you want to save changes to this file?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Save
            )

            if reply == QMessageBox.Save:
                from features.file_operations.save_file import SaveFileAction
                save_action = SaveFileAction(window)
                return save_action.execute()
            elif reply == QMessageBox.Cancel:
                return False

        return True