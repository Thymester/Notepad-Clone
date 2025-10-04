from PyQt5.QtGui import QKeySequence

from core.base_action import BaseAction
from ui.icons import ModernIcon


class FindAction(BaseAction):
    """
    Action for showing the find dialog.
    """

    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            text="&Find...",
            shortcut=QKeySequence.Find,
            icon=ModernIcon.create_icon("find"),
            tooltip="Find text (Ctrl+F)",
            status_tip="Find text"
        )

    def execute(self):
        """Execute the find action."""
        window = self.get_parent_window()
        if hasattr(window, 'find_replace_dialog'):
            window.find_replace_dialog.show()
            window.find_replace_dialog.raise_()
            window.find_replace_dialog.activateWindow()
        else:
            # Create and show find dialog
            from ui.find_replace_dialog import FindReplaceDialog
            window.find_replace_dialog = FindReplaceDialog(window)
            window.find_replace_dialog.show()