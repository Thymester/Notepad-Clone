from PyQt5.QtWidgets import QMenuBar, QMenu

from features.file_operations.new_file import NewFileAction
from features.file_operations.open_file import OpenFileAction
from features.file_operations.save_file import SaveFileAction
from features.file_operations.save_as_file import SaveAsFileAction
from features.file_operations.print_file import PrintFileAction
from features.file_operations.exit_app import ExitAppAction
from features.file_operations.recent_files import RecentFilesAction
from features.file_operations.save_encrypted import SaveEncryptedAction

from features.edit_operations.undo import UndoAction
from features.edit_operations.redo import RedoAction
from features.edit_operations.cut import CutAction
from features.edit_operations.copy import CopyAction
from features.edit_operations.paste import PasteAction
from features.edit_operations.delete import DeleteAction
from features.edit_operations.find import FindAction
from features.edit_operations.replace import ReplaceAction
from features.edit_operations.goto import GotoAction
from features.edit_operations.select_all import SelectAllAction
from features.edit_operations.time_date import TimeDateAction

from features.format_operations.word_wrap import WordWrapAction
from features.format_operations.font import FontAction
from features.format_operations.syntax_highlighting import SyntaxHighlightingAction

from features.view_operations.zoom_in import ZoomInAction
from features.view_operations.zoom_out import ZoomOutAction
from features.view_operations.restore_zoom import RestoreZoomAction
from features.view_operations.toggle_status_bar import ToggleStatusBarAction
from features.view_operations.dark_mode import DarkModeAction

from features.help_operations.about import AboutAction


class MenuBar(QMenuBar):
    """
    Custom menu bar for the notepad application.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.create_menus()

    def create_menus(self):
        """Create all menus and their actions."""
        self.create_file_menu()
        self.create_edit_menu()
        self.create_format_menu()
        self.create_view_menu()
        self.create_help_menu()

    def create_file_menu(self):
        """Create the File menu."""
        file_menu = self.addMenu("&File")

        # File operations
        new_action = NewFileAction(self.parent_window)
        file_menu.addAction(new_action)

        new_window_action = NewFileAction(self.parent_window, is_new_window=True)
        new_window_action.setText("New &Window\tCtrl+Shift+N")
        file_menu.addAction(new_window_action)

        open_action = OpenFileAction(self.parent_window)
        file_menu.addAction(open_action)

        save_action = SaveFileAction(self.parent_window)
        file_menu.addAction(save_action)

        save_as_action = SaveAsFileAction(self.parent_window)
        file_menu.addAction(save_as_action)

        save_encrypted_action = SaveEncryptedAction(self.parent_window)
        file_menu.addAction(save_encrypted_action)

        file_menu.addSeparator()

        # Recent files submenu
        self.recent_files_action = RecentFilesAction(self.parent_window)
        recent_menu = self.recent_files_action.get_recent_files_menu()
        file_menu.addMenu(recent_menu)
        self.recent_files_action.file_selected.connect(self.parent_window.open_recent_file)

        file_menu.addSeparator()

        # Print operations
        print_action = PrintFileAction(self.parent_window)
        file_menu.addAction(print_action)

        file_menu.addSeparator()

        exit_action = ExitAppAction(self.parent_window)
        file_menu.addAction(exit_action)

    def create_edit_menu(self):
        """Create the Edit menu."""
        edit_menu = self.addMenu("&Edit")

        # Undo/Redo
        undo_action = UndoAction(self.parent_window)
        edit_menu.addAction(undo_action)

        redo_action = RedoAction(self.parent_window)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        # Clipboard operations
        cut_action = CutAction(self.parent_window)
        edit_menu.addAction(cut_action)

        copy_action = CopyAction(self.parent_window)
        edit_menu.addAction(copy_action)

        paste_action = PasteAction(self.parent_window)
        edit_menu.addAction(paste_action)

        delete_action = DeleteAction(self.parent_window)
        edit_menu.addAction(delete_action)

        edit_menu.addSeparator()

        # Find/Replace
        find_action = FindAction(self.parent_window)
        edit_menu.addAction(find_action)

        replace_action = ReplaceAction(self.parent_window)
        edit_menu.addAction(replace_action)

        goto_action = GotoAction(self.parent_window)
        edit_menu.addAction(goto_action)

        edit_menu.addSeparator()

        # Selection operations
        select_all_action = SelectAllAction(self.parent_window)
        edit_menu.addAction(select_all_action)

        time_date_action = TimeDateAction(self.parent_window)
        edit_menu.addAction(time_date_action)

    def create_format_menu(self):
        """Create the Format menu."""
        format_menu = self.addMenu("F&ormat")

        word_wrap_action = WordWrapAction(self.parent_window)
        format_menu.addAction(word_wrap_action)

        font_action = FontAction(self.parent_window)
        format_menu.addAction(font_action)

        format_menu.addSeparator()

        syntax_highlighting_action = SyntaxHighlightingAction(self.parent_window)
        format_menu.addAction(syntax_highlighting_action)

    def create_view_menu(self):
        """Create the View menu."""
        view_menu = self.addMenu("&View")

        zoom_menu = view_menu.addMenu("&Zoom")

        zoom_in_action = ZoomInAction(self.parent_window)
        zoom_menu.addAction(zoom_in_action)

        zoom_out_action = ZoomOutAction(self.parent_window)
        zoom_menu.addAction(zoom_out_action)

        restore_zoom_action = RestoreZoomAction(self.parent_window)
        zoom_menu.addAction(restore_zoom_action)

        toggle_status_bar_action = ToggleStatusBarAction(self.parent_window)
        view_menu.addAction(toggle_status_bar_action)

        view_menu.addSeparator()

        dark_mode_action = DarkModeAction(self.parent_window)
        view_menu.addAction(dark_mode_action)

    def create_help_menu(self):
        """Create the Help menu."""
        help_menu = self.addMenu("&Help")

        about_action = AboutAction(self.parent_window)
        help_menu.addAction(about_action)