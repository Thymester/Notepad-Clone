from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton
from PyQt5.QtCore import Qt, QTimer

from core.base_action import BaseAction


class DarkModeAction(BaseAction):
    """
    Action for toggling dark mode theme.
    """

    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            text="&Dark Mode",
            tooltip="Toggle dark mode theme",
            status_tip="Toggle dark mode theme"
        )
        self.is_dark_mode = False
        self.load_dark_mode_setting()

    def execute(self):
        """Execute the dark mode toggle action."""
        self.is_dark_mode = not self.is_dark_mode
        self.save_dark_mode_setting()
        self.update_theme()

    def load_dark_mode_setting(self):
        """Load dark mode setting from persistent storage."""
        try:
            from PyQt5.QtCore import QSettings
            settings = QSettings("ModernNotepad", "Theme")
            self.is_dark_mode = settings.value("dark_mode", False, type=bool)
            if self.is_dark_mode:
                # Defer theme application to ensure UI is fully initialized
                QTimer.singleShot(0, self.update_theme)
        except Exception:
            # If loading fails, default to light mode
            self.is_dark_mode = False

    def save_dark_mode_setting(self):
        """Save dark mode setting to persistent storage."""
        try:
            from PyQt5.QtCore import QSettings
            settings = QSettings("ModernNotepad", "Theme")
            settings.setValue("dark_mode", self.is_dark_mode)
            settings.sync()  # Ensure immediate write
        except Exception:
            # If saving fails, continue without error
            pass

    def execute(self):
        """Execute the dark mode toggle action."""
        self.is_dark_mode = not self.is_dark_mode
        self.save_dark_mode_setting()
        self.update_theme()

    def update_theme(self):
        """Update the application theme."""
        window = self.get_parent_window()
        if self.is_dark_mode:
            window.setStyleSheet(self.get_dark_theme_stylesheet())
            self.setText("&Light Mode")
            self.setToolTip("Switch to light mode theme")
            self.setStatusTip("Switch to light mode theme")
        else:
            window.setStyleSheet(self.get_light_theme_stylesheet())
            self.setText("&Dark Mode")
            self.setToolTip("Toggle dark mode theme")
            self.setStatusTip("Toggle dark mode theme")

    def get_dark_theme_stylesheet(self):
        """Get the dark theme stylesheet."""
        return """
            QMainWindow {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QPlainTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                padding: 8px;
                font-family: 'Segoe UI', Consolas, 'Courier New', monospace;
                line-height: 1.4;
                selection-background-color: #264f78;
            }
            QMenuBar {
                background-color: #2b2b2b;
                border-bottom: 1px solid #3c3c3c;
                padding: 4px;
                color: #ffffff;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 6px 12px;
                border-radius: 4px;
                color: #ffffff;
            }
            QMenuBar::item:selected {
                background-color: #3c3c3c;
            }
            QMenu {
                background-color: #2b2b2b;
                border: 1px solid #3c3c3c;
                color: #ffffff;
                padding: 4px 0px;
            }
            QMenu::item {
                background-color: transparent;
                padding: 6px 24px;
                color: #ffffff;
                border: none;
            }
            QMenu::item:selected {
                background-color: #3c3c3c;
                color: #ffffff;
            }
            QMenu::item:disabled {
                color: #888888;
                background-color: transparent;
            }
            QMenu::separator {
                background-color: #3c3c3c;
                height: 1px;
                margin: 4px 0px;
            }
            QToolBar {
                background-color: #2b2b2b;
                border: none;
                border-bottom: 1px solid #3c3c3c;
                spacing: 4px;
                padding: 8px;
            }
            QToolBar::separator {
                background-color: #3c3c3c;
                width: 1px;
                margin: 4px;
            }
            QStatusBar {
                background-color: #2b2b2b;
                border-top: 1px solid #3c3c3c;
                padding: 4px;
                color: #ffffff;
            }
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0b5ed7;
            }
            QPushButton:pressed {
                background-color: #0a58ca;
            }
            QDialog {
                background-color: #2b2b2b;
                border: 1px solid #3c3c3c;
                border-radius: 8px;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
            QComboBox {
                background-color: #1e1e1e;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                padding: 4px;
                color: #ffffff;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid #ffffff;
                margin-right: 8px;
            }
            QTabWidget::pane {
                border: 1px solid #3c3c3c;
                background-color: #1e1e1e;
            }
            QTabBar::tab {
                background-color: #2b2b2b;
                border: 1px solid #3c3c3c;
                padding: 8px 16px;
                margin-right: 2px;
                color: #ffffff;
            }
            QTabBar::tab:selected {
                background-color: #1e1e1e;
                border-bottom: none;
            }
            QTabBar::tab:hover {
                background-color: #3c3c3c;
            }
            QToolButton {
                background-color: transparent;
                border: none;
                padding: 4px;
                border-radius: 4px;
                color: #ffffff;
            }
            QToolButton:hover {
                background-color: #3c3c3c;
            }
            QToolButton:pressed {
                background-color: #1e1e1e;
            }
        """

    def get_light_theme_stylesheet(self):
        """Get the light theme stylesheet."""
        return """
            QMainWindow {
                background-color: #f8f9fa;
                color: #212529;
            }
            QPlainTextEdit {
                background-color: #ffffff;
                border: 1px solid #e9ecef;
                border-radius: 4px;
                padding: 8px;
                font-family: 'Segoe UI', Consolas, 'Courier New', monospace;
                line-height: 1.4;
            }
            QMenuBar {
                background-color: #ffffff;
                border-bottom: 1px solid #e9ecef;
                padding: 4px;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QMenuBar::item:selected {
                background-color: #e9ecef;
            }
            QMenu {
                background-color: #ffffff;
                border: 1px solid #e9ecef;
                padding: 4px 0px;
            }
            QMenu::item {
                background-color: transparent;
                padding: 6px 24px;
                border: none;
            }
            QMenu::item:selected {
                background-color: #e9ecef;
            }
            QMenu::item:disabled {
                color: #6c757d;
                background-color: transparent;
            }
            QMenu::separator {
                background-color: #e9ecef;
                height: 1px;
                margin: 4px 0px;
            }
            QToolBar {
                background-color: #ffffff;
                border: none;
                border-bottom: 1px solid #e9ecef;
                spacing: 4px;
                padding: 8px;
            }
            QToolBar::separator {
                background-color: #e9ecef;
                width: 1px;
                margin: 4px;
            }
            QStatusBar {
                background-color: #f8f9fa;
                border-top: 1px solid #e9ecef;
                padding: 4px;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
            QDialog {
                background-color: #ffffff;
                border: 1px solid #e9ecef;
                border-radius: 8px;
            }
            QComboBox {
                background-color: #ffffff;
                border: 1px solid #e9ecef;
                border-radius: 4px;
                padding: 4px;
            }
            QTabWidget::pane {
                border: 1px solid #e9ecef;
                background-color: #ffffff;
            }
            QTabBar::tab {
                background-color: #ffffff;
                border: 1px solid #e9ecef;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #f8f9fa;
                border-bottom: none;
            }
            QTabBar::tab:hover {
                background-color: #e9ecef;
            }
            QToolButton {
                background-color: transparent;
                border: none;
                padding: 4px;
                border-radius: 4px;
                color: #212529;
            }
            QToolButton:hover {
                background-color: #e9ecef;
            }
            QToolButton:pressed {
                background-color: #dee2e6;
            }
        """