from PyQt5.QtWidgets import QMenu
from PyQt5.QtCore import pyqtSignal
from core.base_action import BaseAction

class RecentFilesAction(BaseAction):
    """
    Action for managing recent files menu.
    """

    # Signal emitted when a recent file is selected
    file_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            text="&Recent Files",
            tooltip="Open recently used files",
            status_tip="Open recently used files"
        )
        self.recent_files = []
        self.max_recent_files = 10
        self.load_recent_files()

    def execute(self):
        """Execute the recent files action - creates submenu."""
        # This action creates a submenu, so execute doesn't do anything
        # The submenu is created in the menu bar
        pass

    def add_recent_file(self, file_path):
        """Add a file to the recent files list."""
        if file_path in self.recent_files:
            self.recent_files.remove(file_path)
        
        self.recent_files.insert(0, file_path)
        
        # Keep only the most recent files
        if len(self.recent_files) > self.max_recent_files:
            self.recent_files = self.recent_files[:self.max_recent_files]
        
        self.save_recent_files()

    def get_recent_files_menu(self):
        """Get a QMenu populated with recent files."""
        menu = QMenu("Recent Files", self.get_parent_window())
        
        if not self.recent_files:
            action = menu.addAction("No recent files")
            action.setEnabled(False)
        else:
            for i, file_path in enumerate(self.recent_files):
                # Truncate long paths for display
                display_name = self._truncate_path(file_path)
                action = menu.addAction(f"&{i+1} {display_name}")
                action.setData(file_path)
                action.triggered.connect(lambda checked, path=file_path: self._on_file_selected(path))
        
        return menu

    def _on_file_selected(self, file_path):
        """Handle selection of a recent file."""
        self.file_selected.emit(file_path)

    def _truncate_path(self, file_path, max_length=50):
        """Truncate a file path for display in menu."""
        if len(file_path) <= max_length:
            return file_path
        
        # Try to keep the filename and some of the directory
        import os
        dirname = os.path.dirname(file_path)
        basename = os.path.basename(file_path)
        
        if len(basename) >= max_length - 3:
            return basename[:max_length-3] + "..."
        
        remaining = max_length - len(basename) - 3
        if len(dirname) > remaining:
            dirname = "..." + dirname[-(remaining):]
        
        return os.path.join(dirname, basename)

    def load_recent_files(self):
        """Load recent files from persistent storage."""
        try:
            from PyQt5.QtCore import QSettings
            settings = QSettings("ModernNotepad", "RecentFiles")
            files = settings.value("files", [], type=list)
            self.recent_files = [f for f in files if f]  # Filter out empty strings
        except Exception:
            self.recent_files = []

    def save_recent_files(self):
        """Save recent files to persistent storage."""
        try:
            from PyQt5.QtCore import QSettings
            settings = QSettings("ModernNotepad", "RecentFiles")
            settings.setValue("files", self.recent_files)
            settings.sync()
        except Exception:
            pass

    def clear_recent_files(self):
        """Clear all recent files."""
        self.recent_files = []
        self.save_recent_files()