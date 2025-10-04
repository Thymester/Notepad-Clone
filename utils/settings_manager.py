from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QFont


class SettingsManager:
    """
    Manages application settings persistence.
    """

    def __init__(self):
        self.settings = QSettings("ModernNotepad", "Settings")

    def load_window_settings(self, window):
        """Load window-specific settings."""
        geometry = self.settings.value("geometry")
        if geometry:
            window.restoreGeometry(geometry)

    def save_window_settings(self, window):
        """Save window-specific settings."""
        self.settings.setValue("geometry", window.saveGeometry())

    def load_editor_settings(self, text_editor):
        """Load text editor settings."""
        # Load font
        font_family = self.settings.value("font_family", "Segoe UI")
        font_size = self.settings.value("font_size", 11, type=int)
        font = QFont(font_family, font_size)
        text_editor.set_editor_font(font)

        # Load word wrap setting
        word_wrap = self.settings.value("word_wrap", True, type=bool)
        if word_wrap:
            text_editor.setLineWrapMode(text_editor.WidgetWidth)
        else:
            text_editor.setLineWrapMode(text_editor.NoWrap)

    def save_editor_settings(self, text_editor):
        """Save text editor settings."""
        font = text_editor.font()
        self.settings.setValue("font_family", font.family())
        self.settings.setValue("font_size", font.pointSize())
        self.settings.setValue("word_wrap", text_editor.lineWrapMode() == text_editor.WidgetWidth)

    def get_setting(self, key, default=None):
        """Get a setting value."""
        return self.settings.value(key, default)

    def set_setting(self, key, value):
        """Set a setting value."""
        self.settings.setValue(key, value)