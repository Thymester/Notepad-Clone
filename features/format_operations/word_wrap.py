from core.base_action import BaseAction


class WordWrapAction(BaseAction):
    """
    Action for toggling word wrap.
    """

    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            text="&Word Wrap",
            tooltip="Toggle word wrapping",
            status_tip="Toggle word wrapping"
        )
        self.setCheckable(True)
        self.setChecked(True)

    def execute(self):
        """Execute the word wrap action."""
        text_editor = self.get_text_editor()

        if self.isChecked():
            text_editor.setLineWrapMode(text_editor.WidgetWidth)
        else:
            text_editor.setLineWrapMode(text_editor.NoWrap)