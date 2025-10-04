from PyQt5.QtGui import QKeySequence

from core.base_action import BaseAction
from ui.icons import ModernIcon


class PasteAction(BaseAction):
    """
    Action for pasting text from clipboard.
    """

    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            text="&Paste",
            shortcut=QKeySequence.Paste,
            icon=ModernIcon.create_icon("paste"),
            tooltip="Paste text from clipboard (Ctrl+V)",
            status_tip="Paste text from clipboard"
        )

    def execute(self):
        """Execute the paste action."""
        text_editor = self.get_text_editor()
        text_editor.paste()