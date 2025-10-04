from PyQt5.QtWidgets import QToolBar
from PyQt5.QtCore import Qt, QSize

from features.file_operations.new_file import NewFileAction
from features.file_operations.open_file import OpenFileAction
from features.file_operations.save_file import SaveFileAction
from features.file_operations.print_file import PrintFileAction
from features.edit_operations.cut import CutAction
from features.edit_operations.copy import CopyAction
from features.edit_operations.paste import PasteAction
from features.edit_operations.undo import UndoAction
from features.edit_operations.redo import RedoAction
from features.edit_operations.find import FindAction


class ToolBar(QToolBar):
    """
    Custom toolbar for the notepad application.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setWindowTitle("Main")
        self.setMovable(False)
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.setIconSize(QSize(24, 24))

        self.create_actions()

    def create_actions(self):
        """Create and add toolbar actions."""
        # File actions
        new_action = NewFileAction(self.parent_window)
        self.addAction(new_action)

        open_action = OpenFileAction(self.parent_window)
        self.addAction(open_action)

        save_action = SaveFileAction(self.parent_window)
        self.addAction(save_action)

        self.addSeparator()

        # Edit actions
        cut_action = CutAction(self.parent_window)
        self.addAction(cut_action)

        copy_action = CopyAction(self.parent_window)
        self.addAction(copy_action)

        paste_action = PasteAction(self.parent_window)
        self.addAction(paste_action)

        self.addSeparator()

        # Undo/Redo
        undo_action = UndoAction(self.parent_window)
        self.addAction(undo_action)

        redo_action = RedoAction(self.parent_window)
        self.addAction(redo_action)

        self.addSeparator()

        # Find and print
        find_action = FindAction(self.parent_window)
        self.addAction(find_action)

        print_action = PrintFileAction(self.parent_window)
        self.addAction(print_action)