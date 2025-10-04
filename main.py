import sys
from PyQt5.QtWidgets import QApplication
from core.notepad_window import NotepadWindow
from ui.icons import ModernIcon
from features.file_operations.open_file import OpenFileAction


def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    app.setApplicationName("Modern Notepad")
    app.setOrganizationName("ModernNotepad")

    # Set modern application style
    app.setStyle('Fusion')

    # Create app icon
    app_icon = ModernIcon.create_icon("new", 32)
    app.setWindowIcon(app_icon)

    window = NotepadWindow()
    window.show()

    # Handle command line arguments (files to open)
    if len(sys.argv) > 1:
        open_action = OpenFileAction(window)
        for file_path in sys.argv[1:]:
            # Create a new tab for each file
            if window.tab_widget.count() > 1 or window.is_document_modified():
                window.new_document()
            open_action._open_file(file_path)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
