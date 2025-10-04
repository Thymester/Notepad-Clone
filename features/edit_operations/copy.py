from PyQt5.QtGui import QKeySequence

from core.base_action import BaseAction
from ui.icons import ModernIcon


class CopyAction(BaseAction):
    """
    Action for copying selected text to clipboard.
    """

    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            text="&Copy",
            shortcut=QKeySequence.Copy,
            icon=ModernIcon.create_icon("copy"),
            tooltip="Copy selected text (Ctrl+C)",
            status_tip="Copy selected text"
        )

    def execute(self):
        """Execute the copy action."""
        text_editor = self.get_text_editor()
        text_editor.copy()