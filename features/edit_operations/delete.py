from PyQt5.QtGui import QKeySequence

from core.base_action import BaseAction


class DeleteAction(BaseAction):
    """
    Action for deleting selected text or character at cursor.
    """

    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            text="&Delete",
            shortcut=QKeySequence.Delete,
            tooltip="Delete selected text or character (Del)",
            status_tip="Delete selected text or character"
        )

    def execute(self):
        """Execute the delete action."""
        text_editor = self.get_text_editor()
        text_editor.delete_selected_text()