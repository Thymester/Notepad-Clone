from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QInputDialog

from core.base_action import BaseAction


class GotoAction(BaseAction):
    """
    Action for going to a specific line number.
    """

    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            text="&Go To...",
            shortcut=QKeySequence("Ctrl+G"),
            tooltip="Go to a specific line (Ctrl+G)",
            status_tip="Go to a specific line"
        )

    def execute(self):
        """Execute the goto action."""
        window = self.get_parent_window()
        text_editor = self.get_text_editor()

        current_line, _ = text_editor.get_cursor_position()
        total_lines = text_editor.get_line_count()

        line_number, ok = QInputDialog.getInt(
            window, "Go To Line",
            f"Line number (1-{total_lines}):",
            current_line, 1, total_lines
        )

        if ok:
            text_editor.goto_line(line_number)