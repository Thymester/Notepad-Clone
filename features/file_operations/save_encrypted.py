from PyQt5.QtWidgets import QFileDialog, QMessageBox

from core.base_action import BaseAction
from ui.password_dialog import PasswordDialog
from utils.security.encryption import EncryptionService


class SaveEncryptedAction(BaseAction):
    """
    Action for saving the current file with encryption.
    """

    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            text="Save &Encrypted...",
            tooltip="Save the current file with encryption",
            status_tip="Save the current file with encryption"
        )
        self.encryption_service = EncryptionService()

    def execute(self):
        """Execute the save encrypted action."""
        window = self.get_parent_window()
        text_editor = self.get_text_editor()

        # Show password dialog
        password_dialog = PasswordDialog(window, mode="encrypt")
        if password_dialog.exec_() != PasswordDialog.Accepted:
            return False

        password = password_dialog.get_password()
        algorithm = password_dialog.get_algorithm()

        # Show save dialog
        file_path, _ = QFileDialog.getSaveFileName(
            window, 'Save Encrypted File', '',
            'Encrypted files (*.enc);;All files (*.*)'
        )

        if file_path:
            # Ensure correct extension
            if not file_path.endswith('.enc'):
                file_path += '.enc'

            return self._save_encrypted_to_path(file_path, password, algorithm)
        return False

    def _save_encrypted_to_path(self, file_path, password, algorithm):
        """Save encrypted content to the specified file path."""
        window = self.get_parent_window()
        text_editor = self.get_text_editor()

        try:
            content = text_editor.get_content()

            # Encrypt the content
            encrypted_data = self.encryption_service.encrypt_data(content, password, algorithm)

            # Save encrypted data
            with open(file_path, 'wb') as file:
                file.write(encrypted_data)

            window.set_current_file_path(file_path)
            window.set_modified(False)

            # Update status bar
            window.status_bar.show_message(f"Saved encrypted file: {file_path}", 2000)
            return True

        except Exception as e:
            QMessageBox.critical(window, "Error", f"Could not save encrypted file: {str(e)}")
            return False