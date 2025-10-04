import os
import sys
import subprocess
from PyQt5.QtWidgets import QMessageBox

from core.base_action import BaseAction
from ui.icons import ModernIcon


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

        # Show information dialog
        reply = QMessageBox.question(
            window,
            "Setup File Associations",
            "This will set up file associations so that .txt and .enc files open with Notepad Clone.\n\n"
            "This requires administrator privileges and will modify the Windows registry.\n\n"
            "Do you want to continue?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        try:
            # Determine which script to run
            script_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            batch_script = os.path.join(script_dir, "setup_file_associations.bat")
            ps_script = os.path.join(script_dir, "setup_file_associations.ps1")

            # Try batch script first (more reliable for admin elevation)
            if os.path.exists(batch_script):
                # Run batch script as administrator
                result = subprocess.run(
                    ['powershell', 'Start-Process', 'cmd.exe', '-ArgumentList', f'/c "{batch_script}"', '-Verb', 'RunAs'],
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:
                    QMessageBox.information(
                        window,
                        "Success",
                        "File associations have been set up successfully!\n\n"
                        ".txt and .enc files will now open with Notepad Clone.\n\n"
                        "You may need to restart Windows Explorer or log out/in for changes to take effect."
                    )
                else:
                    self._show_error(window, "Failed to run setup script. You may need to run the setup script manually as administrator.")

            elif os.path.exists(ps_script):
                # Fallback to PowerShell script
                result = subprocess.run(
                    ['powershell', '-ExecutionPolicy', 'Bypass', '-File', ps_script, '-Verb', 'RunAs'],
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:
                    QMessageBox.information(
                        window,
                        "Success",
                        "File associations have been set up successfully!\n\n"
                        ".txt and .enc files will now open with Notepad Clone.\n\n"
                        "You may need to restart Windows Explorer or log out/in for changes to take effect."
                    )
                else:
                    self._show_error(window, "Failed to run setup script. You may need to run the setup script manually as administrator.")
            else:
                self._show_error(window, "Setup scripts not found. Please run the setup scripts manually from the application directory.")

        except Exception as e:
            self._show_error(window, f"Error setting up file associations: {str(e)}")

    def _show_error(self, window, message):
        """Show error message dialog."""
        QMessageBox.critical(
            window,
            "Setup Failed",
            f"{message}\n\n"
            "Please refer to FILE_ASSOCIATIONS_README.md for manual setup instructions."
        )