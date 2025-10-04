from PyQt5.QtWidgets import QFontDialog

from core.base_action import BaseAction


class FontAction(BaseAction):
    """
    Action for changing the font.
    """

    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            text="&Font...",
            tooltip="Change the font",
            status_tip="Change the font"
        )

    def execute(self):
        """Execute the font action."""
        window = self.get_parent_window()
        text_editor = self.get_text_editor()

        current_font = text_editor.font()
        font, ok = QFontDialog.getFont(current_font, window)

        if ok:
            text_editor.set_editor_font(font)