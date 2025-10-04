from PyQt5.QtGui import QKeySequence
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter

from core.base_action import BaseAction
from ui.icons import ModernIcon


class PrintFileAction(BaseAction):
    """
    Action for printing the current document.
    """

    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            text="&Print...",
            shortcut=QKeySequence.Print,
            icon=ModernIcon.create_icon("print"),
            tooltip="Print the current document (Ctrl+P)",
            status_tip="Print the current document"
        )

    def execute(self):
        """Execute the print file action."""
        window = self.get_parent_window()
        text_editor = self.get_text_editor()

        printer = QPrinter()
        dialog = QPrintDialog(printer, window)

        if dialog.exec_() == QPrintDialog.Accepted:
            text_editor.print_document(printer)