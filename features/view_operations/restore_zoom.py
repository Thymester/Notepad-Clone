from PyQt5.QtGui import QKeySequence

from core.base_action import BaseAction


class RestoreZoomAction(BaseAction):
    """
    Action for restoring default zoom level.
    """

    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            text="&Restore Default Zoom",
            shortcut=QKeySequence("Ctrl+0"),
            tooltip="Restore default zoom (Ctrl+0)",
            status_tip="Restore default zoom"
        )

    def execute(self):
        """Execute the restore zoom action."""
        window = self.get_parent_window()
        window.zoom_level = 100
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