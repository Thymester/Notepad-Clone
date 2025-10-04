from PyQt5.QtGui import QKeySequence

from core.base_action import BaseAction


class ReplaceAction(BaseAction):
    """
    Action for showing the replace dialog.
    """

    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            text="&Replace...",
            shortcut=QKeySequence.Replace,
            tooltip="Replace text (Ctrl+H)",
            status_tip="Replace text"
        )

    def execute(self):
        """Execute the replace action."""
        window = self.get_parent_window()
        if hasattr(window, 'find_replace_dialog'):
            window.find_replace_dialog.show()
            window.find_replace_dialog.raise_()
            window.find_replace_dialog.activateWindow()
        else:
            # Create and show find/replace dialog
            from ui.find_replace_dialog import FindReplaceDialog
            window.find_replace_dialog = FindReplaceDialog(window)
            window.find_replace_dialog.show()