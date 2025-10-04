from PyQt5.QtGui import QKeySequence
import datetime
from core.base_action import BaseAction

class TimeDateAction(BaseAction):
    """
    Action for inserting current time and date.
    """

    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            text="Time and Date",
            tooltip="Insert current time and date",
            status_tip="Insert current time and date"
        )
        # Note: F5 shortcut removed to avoid display issues in menus

    def execute(self):
        """Execute the time/date action."""
        text_editor = self.get_text_editor()

        current_time = datetime.datetime.now()
        time_str = current_time.strftime("%I:%M %p %m/%d/%Y")

        text_editor.insert_text_at_cursor(time_str)