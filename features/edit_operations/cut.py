from PyQt5.QtGui import QKeySequence

from core.base_action import BaseAction
from ui.icons import ModernIcon


class CutAction(BaseAction):
    """
    Action for cutting selected text to clipboard.
    """

    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            text="Cu&t",
            shortcut=QKeySequence.Cut,
            icon=ModernIcon.create_icon("cut"),
            tooltip="Cut selected text (Ctrl+X)",
            status_tip="Cut selected text"
        )

    def execute(self):
        """Execute the cut action."""
        text_editor = self.get_text_editor()
        text_editor.cut()