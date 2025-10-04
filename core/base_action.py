from PyQt5.QtWidgets import QAction


class BaseAction(QAction):
    """
    Base class for all notepad actions.
    """

    def __init__(self, parent=None, text="", shortcut=None, icon=None, tooltip="", status_tip=""):
        super().__init__(parent)

        self.setText(text)
        if shortcut:
            self.setShortcut(shortcut)
        if icon:
            self.setIcon(icon)
        if tooltip:
            self.setToolTip(tooltip)
        if status_tip:
            self.setStatusTip(status_tip)

        self.triggered.connect(self.execute)

    def execute(self):
        """Execute the action. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement execute method")

    def get_parent_window(self):
        """Get the parent notepad window."""
        return self.parent()

    def get_text_editor(self):
        """Get the text editor from the parent window."""
        return self.get_parent_window().get_text_editor()