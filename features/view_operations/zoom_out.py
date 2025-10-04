from PyQt5.QtGui import QKeySequence

from core.base_action import BaseAction
from ui.icons import ModernIcon


class ZoomOutAction(BaseAction):
    """
    Action for zooming out the text.
    """

    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            text="Zoom &Out",
            shortcut=QKeySequence.ZoomOut,
            icon=ModernIcon.create_icon("zoom_out"),
            tooltip="Zoom out (Ctrl+-)",
            status_tip="Zoom out"
        )

    def execute(self):
        """Execute the zoom out action."""
        window = self.get_parent_window()
        if hasattr(window, 'zoom_level'):
            window.zoom_level = max(10, window.zoom_level - 10)
            self._apply_zoom()

    def _apply_zoom(self):
        """Apply the current zoom level."""
        window = self.get_parent_window()
        text_editor = self.get_text_editor()

        font = text_editor.font()
        base_size = 11
        new_size = int(base_size * window.zoom_level / 100)
        font.setPointSize(new_size)
        text_editor.set_editor_font(font)

        # Update status bar
        if hasattr(window, 'status_bar'):
            window.status_bar.update_zoom_label(window.zoom_level)