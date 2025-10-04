from PyQt5.QtGui import QKeySequence

from core.base_action import BaseAction
from ui.icons import ModernIcon


class RedoAction(BaseAction):
    """
    Action for redoing the last undone operation.
    """

    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            text="&Redo",
            shortcut=QKeySequence("Ctrl+Y"),
            icon=ModernIcon.create_icon("redo"),
            tooltip="Redo last action (Ctrl+Y)",
            status_tip="Redo last action"
        )

    def execute(self):
        """Execute the redo action."""
        text_editor = self.get_text_editor()
        text_editor.redo()