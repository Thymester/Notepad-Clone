from PyQt5.QtWidgets import QMessageBox

from core.base_action import BaseAction


class AboutAction(BaseAction):
    """
    Action for showing the about dialog.
    """

    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            text="&About Modern Notepad",
            tooltip="Show information about the application",
            status_tip="Show information about the application"
        )

    def execute(self):
        """Execute the about action."""
        window = self.get_parent_window()

        QMessageBox.about(
            window, "About Modern Notepad",
            "Modern Notepad\n\n"
            "A modern, feature-rich text editor built with PyQt5.\n"
            "Includes all standard Notepad features with modern improvements.\n\n"
            "© 2025 Modern Notepad"
        )