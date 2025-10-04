import os
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QStatusBar, QLabel, QTabWidget, QTextEdit
from PyQt5.QtCore import QSettings

from core.text_editor import TextEditor
from ui.menu_bar import MenuBar
from ui.tool_bar import ToolBar
from ui.status_bar import StatusBar
from utils.settings_manager import SettingsManager


class DocumentTab(QWidget):
    """
    A tab containing a text editor and document state.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_path = ""
        self.is_modified = False
        self.text_editor = TextEditor()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.text_editor)


class NotepadWindow(QMainWindow):
    """
    Main notepad application window.
    """

    def __init__(self):
        super().__init__()
        self.zoom_level = 100

        # Initialize components
        self.settings_manager = SettingsManager()
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)

        self.menu_bar = MenuBar(self)
        self.tool_bar = ToolBar(self)
        self.status_bar = StatusBar(self)

        # Create initial tab
        self.new_document()

        self.init_ui()
        self.connect_signals()
        self.load_settings()

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Modern Notepad")
        self.setGeometry(200, 200, 900, 700)

        # Set modern dark theme colors
        self.setStyleSheet("""
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
        """)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.tab_widget)

        # Set menu bar and tool bar
        self.setMenuBar(self.menu_bar)
        self.addToolBar(self.tool_bar)
        self.setStatusBar(self.status_bar.status_bar)

    def connect_signals(self):
        """Connect signals between components."""
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        
        # Connect text editor signals
        self.connect_text_editor_signals()

    def connect_text_editor_signals(self):
        """Connect signals for the current text editor."""
        if self.text_editor:
            # Disconnect any existing connections first
            try:
                self.text_editor.textChanged.disconnect()
            except:
                pass
            try:
                self.text_editor.cursorPositionChanged.disconnect()
            except:
                pass
            
            # Connect new signals
            self.text_editor.textChanged.connect(self.on_text_changed)
            self.text_editor.textChanged.connect(self.update_counters)
            self.text_editor.cursorPositionChanged.connect(self.status_bar.update_cursor_position)
            
            # Update counters immediately
            self.update_counters()

    @property
    def text_editor(self):
        """Get the current text editor."""
        current_widget = self.tab_widget.currentWidget()
        if current_widget and hasattr(current_widget, 'text_editor'):
            return current_widget.text_editor
        return None

    def update_counters(self):
        """Update all counter displays in the status bar."""
        self.status_bar.update_word_count()
        self.status_bar.update_char_count()
        self.status_bar.update_line_count()

    def new_document(self):
        """Create a new document tab."""
        tab_widget = DocumentTab()

        tab_index = self.tab_widget.addTab(tab_widget, "Untitled")
        self.tab_widget.setCurrentIndex(tab_index)
        self.update_tab_title(tab_index)
        self.connect_text_editor_signals()

    def close_tab(self, index):
        """Close a tab at the given index."""
        if self.tab_widget.count() > 1:
            tab_widget = self.tab_widget.widget(index)
            if tab_widget and tab_widget.is_modified:
                # TODO: Ask for save confirmation
                pass
            self.tab_widget.removeTab(index)
        else:
            # Don't close the last tab, just clear it
            tab_widget = self.tab_widget.widget(index)
            if tab_widget:
                tab_widget.text_editor.clear_content()
                tab_widget.is_modified = False
                tab_widget.file_path = ""
                self.update_tab_title(index)

    def on_tab_changed(self, index):
        """Handle tab change."""
        if index >= 0:
            self.update_title()
            # Reconnect text editor signals for the new tab
            self.connect_text_editor_signals()

    def on_text_changed(self):
        """Handle text changes in the current editor."""
        current_tab = self.get_current_tab()
        if current_tab and not current_tab.is_modified:
            current_tab.is_modified = True
            self.update_current_tab_title()

    def get_current_tab(self):
        """Get the current document tab."""
        current_widget = self.tab_widget.currentWidget()
        if isinstance(current_widget, DocumentTab):
            return current_widget
        return None

    def update_current_tab_title(self):
        """Update the title of the current tab."""
        current_index = self.tab_widget.currentIndex()
        if current_index >= 0:
            self.update_tab_title(current_index)

    def update_tab_title(self, index):
        """Update the title of a specific tab."""
        tab_widget = self.tab_widget.widget(index)
        if tab_widget:
            title = "Untitled"
            if tab_widget.file_path:
                title = os.path.basename(tab_widget.file_path)
            if tab_widget.is_modified:
                title = f"*{title}"
            self.tab_widget.setTabText(index, title)

    def update_title(self):
        """Update the window title based on current tab."""
        current_tab = self.get_current_tab()
        if current_tab:
            title = "Modern Notepad"
            if current_tab.file_path:
                filename = os.path.basename(current_tab.file_path)
                title = f"{filename} - {title}"
            else:
                title = f"Untitled - {title}"

            if current_tab.is_modified:
                title = f"*{title}"

            self.setWindowTitle(title)

    def set_current_file_path(self, file_path):
        """Set the current file path for the current tab."""
        current_tab = self.get_current_tab()
        if current_tab:
            current_tab.file_path = file_path
            current_tab.is_modified = False
            self.update_current_tab_title()
            self.update_title()

    def set_modified(self, modified):
        """Set the modification status for the current tab."""
        current_tab = self.get_current_tab()
        if current_tab:
            current_tab.is_modified = modified
            self.update_current_tab_title()
            self.update_title()
        self.update_title()

    def get_text_editor(self):
        """Get the text editor instance."""
        return self.text_editor

    def get_current_file_path(self):
        """Get the current file path."""
        current_tab = self.get_current_tab()
        return current_tab.file_path if current_tab else ""

    def is_document_modified(self):
        """Check if the current document has been modified."""
        current_tab = self.get_current_tab()
        return current_tab.is_modified if current_tab else False

    def open_recent_file(self, file_path):
        """Open a file from the recent files list."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Create new tab or use current empty tab
            if self.text_editor and self.text_editor.get_content().strip():
                self.new_document()
            
            self.text_editor.set_content(content)
            self.set_current_file_path(file_path)
            self.status_bar.show_message(f"Opened {file_path}", 3000)
            
        except Exception as e:
            self.status_bar.show_message(f"Error opening file: {str(e)}", 5000)

    def load_settings(self):
        """Load application settings."""
        self.settings_manager.load_window_settings(self)
        self.settings_manager.load_editor_settings(self.text_editor)

    def save_settings(self):
        """Save application settings."""
        self.settings_manager.save_window_settings(self)
        self.settings_manager.save_editor_settings(self.text_editor)

    def closeEvent(self, event):
        """Handle application close event."""
        self.save_settings()
        event.accept()