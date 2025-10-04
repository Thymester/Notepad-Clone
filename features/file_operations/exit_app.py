from core.base_action import BaseAction


class ExitAppAction(BaseAction):
    """
    Action for exiting the application.
    """

    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            text="E&xit",
            tooltip="Exit the application",
            status_tip="Exit the application"
        )

    def execute(self):
        """Execute the exit application action."""
        window = self.get_parent_window()
        window.close()