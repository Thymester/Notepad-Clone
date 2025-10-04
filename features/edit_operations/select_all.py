from PyQt5.QtGui import QKeySequence

from core.base_action import BaseAction


class SelectAllAction(BaseAction):
    """
    Action for selecting all text.
    """

    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            text="Select &All",
            shortcut=QKeySequence.SelectAll,
            tooltip="Select all text (Ctrl+A)",
            status_tip="Select all text"
        )

    def execute(self):
        """Execute the select all action."""
        text_editor = self.get_text_editor()
        text_editor.select_all_text()