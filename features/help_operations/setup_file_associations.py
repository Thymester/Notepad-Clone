import os
import sys
import subprocess
from typing import Optional
from PyQt5.QtWidgets import QMessageBox

from core.base_action import BaseAction
from ui.icons import ModernIcon
from utils.registry_manager import RegistryManager


class SetupFileAssociationsAction(BaseAction):
    """
    Action for setting up file associations for .txt and .enc files.
    """

    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            text="Setup File Associations",
            tooltip="Set up file associations for .txt and .enc files",
            status_tip="Configure Windows to open .txt and .enc files with this application"
        )

    def execute(self):
        """Execute the setup file associations action."""
        window = self.get_parent_window()
        registry_manager = RegistryManager()

        # Check if running as administrator
        if not registry_manager.is_admin():
            reply = QMessageBox.question(
                window,
                "Administrator Privileges Required",
                "Setting up file associations requires administrator privileges.\n\n"
                "The application will attempt to restart itself with elevated privileges.\n\n"
                "Do you want to continue?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if reply != QMessageBox.Yes:
                return

            # Restart with administrator privileges
            try:
                exe_path = self._get_executable_path()
                if exe_path:
                    subprocess.run(['powershell', 'Start-Process', exe_path, '-Verb', 'RunAs'],
                                 check=True)
                else:
                    self._show_error(window, "Could not determine executable path.")
            except subprocess.CalledProcessError:
                self._show_error(window, "Failed to restart with administrator privileges.")
            except Exception as e:
                self._show_error(window, f"Error restarting as administrator: {str(e)}")
            return

        # Show information dialog
        reply = QMessageBox.question(
            window,
            "Setup File Associations",
            "This will set up file associations so that .txt and .enc files open with Notepad Clone.\n\n"
            "Do you want to continue?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        try:
            # Get the executable path
            exe_path = self._get_executable_path()
            if not exe_path:
                self._show_error(window, "Could not determine executable path.")
                return

            # Set up file associations
            results = registry_manager.setup_notepad_associations(exe_path)

            # Check results and show appropriate message
            if all(results.values()):
                QMessageBox.information(
                    window,
                    "Success",
                    "File associations have been set up successfully!\n\n"
                    ".txt and .enc files will now open with Notepad Clone.\n\n"
                    "You may need to restart Windows Explorer or log out/in for changes to take effect."
                )
            else:
                failed_items = [k for k, v in results.items() if not v]
                self._show_error(window, f"Some associations failed to set up: {', '.join(failed_items)}")

        except PermissionError:
            self._show_error(window, "Administrator privileges are required to set up file associations.")
        except Exception as e:
            self._show_error(window, f"Error setting up file associations: {str(e)}")

    def _get_executable_path(self) -> Optional[str]:
        """Get the path to the executable file."""
        # First check if we're running as a packaged executable
        if getattr(sys, 'frozen', False):
            # Running as PyInstaller bundle
            return sys.executable

        # Check for executable on Desktop (both regular and OneDrive)
        possible_desktop_paths = [
            os.path.join(os.path.expanduser("~"), "Desktop", "Modern Notepad.exe"),
            os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop", "Modern Notepad.exe"),
        ]

        for desktop_exe in possible_desktop_paths:
            if os.path.exists(desktop_exe):
                return desktop_exe

        # Check for executable in dist folder (development)
        script_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        dist_exe = os.path.join(script_dir, "dist", "main.exe")
        if os.path.exists(dist_exe):
            return dist_exe

        # As last resort, try to find any .exe file in the dist folder
        dist_dir = os.path.join(script_dir, "dist")
        if os.path.exists(dist_dir):
            for file in os.listdir(dist_dir):
                if file.endswith('.exe'):
                    return os.path.join(dist_dir, file)

        return None

    def _show_error(self, window, message):
        """Show error message dialog."""
        QMessageBox.critical(
            window,
            "Setup Failed",
            f"{message}\n\n"
            "Please refer to FILE_ASSOCIATIONS_README.md for manual setup instructions."
        )