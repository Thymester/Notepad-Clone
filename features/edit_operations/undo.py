from PyQt5.QtGui import QKeySequence

from core.base_action import BaseAction
from ui.icons import ModernIcon


class UndoAction(BaseAction):
    """
    Action for undoing the last operation.
    """

    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            text="&Undo",
            shortcut=QKeySequence.Undo,
            icon=ModernIcon.create_icon("undo"),
            tooltip="Undo last action (Ctrl+Z)",
            status_tip="Undo last action"
        )

    def execute(self):
        """Execute the undo action."""
        text_editor = self.get_text_editor()
        text_editor.undo()
