import sys
from PyQt5.QtWidgets import QApplication
from core.notepad_window import NotepadWindow
from ui.icons import ModernIcon

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

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
