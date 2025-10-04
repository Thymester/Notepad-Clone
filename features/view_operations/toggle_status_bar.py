from core.base_action import BaseAction


class ToggleStatusBarAction(BaseAction):
    """
    Action for toggling the status bar visibility.
    """

    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            text="&Status Bar",
            tooltip="Toggle status bar visibility",
            status_tip="Toggle status bar visibility"
        )
        self.setCheckable(True)
        self.setChecked(True)

    def execute(self):
        """Execute the toggle status bar action."""
        window = self.get_parent_window()
        if hasattr(window, 'status_bar'):
            if self.isChecked():
                window.status_bar.status_bar.show()
            else:
                window.status_bar.status_bar.hide()