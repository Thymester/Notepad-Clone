"""
Registry management utilities for Windows file associations.
"""
import os
import sys
import winreg
import ctypes
from typing import Optional, Dict, Any


class RegistryManager:
    """
    Manages Windows registry operations for file associations.
    """

    def __init__(self):
        self._is_admin = None

    def is_admin(self) -> bool:
        """
        Check if the current process has administrator privileges.

        Returns:
            bool: True if running as administrator, False otherwise
        """
        if self._is_admin is not None:
            return self._is_admin

        try:
            result = ctypes.windll.shell32.IsUserAnAdmin() != 0
        except AttributeError:
            # Fallback for older Windows versions
            try:
                result = os.getuid() == 0
            except AttributeError:
                # Windows without getuid
                result = False

        self._is_admin = result
        return result

    def set_file_association(self, extension: str, prog_id: str, description: str,
                           exe_path: str, icon_path: Optional[str] = None) -> bool:
        """
        Set up file association for a given extension.

        Args:
            extension: File extension (e.g., '.txt')
            prog_id: Program ID for the association
            description: Description of the file type
            exe_path: Path to the executable
            icon_path: Path to the icon (defaults to exe_path,0)

        Returns:
            bool: True if successful, False otherwise
        """
        if not self.is_admin():
            raise PermissionError("Administrator privileges required for registry operations")

        if icon_path is None:
            icon_path = f'"{exe_path}",0'

        try:
            # Set the extension to point to our ProgID
            with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, extension) as key:
                winreg.SetValue(key, None, winreg.REG_SZ, prog_id)

            # Create the ProgID key
            with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, prog_id) as key:
                winreg.SetValue(key, None, winreg.REG_SZ, description)

            # Set the default icon
            with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, f"{prog_id}\\DefaultIcon") as key:
                winreg.SetValue(key, None, winreg.REG_SZ, icon_path)

            # Set the open command
            with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, f"{prog_id}\\shell\\open\\command") as key:
                winreg.SetValue(key, None, winreg.REG_SZ, f'"{exe_path}" "%1"')

            return True

        except Exception as e:
            print(f"Error setting file association for {extension}: {e}")
            return False

    def register_application(self, app_name: str, exe_path: str,
                           icon_path: Optional[str] = None) -> bool:
        """
        Register an application in the Applications registry key.

        Args:
            app_name: Name of the application
            exe_path: Path to the executable
            icon_path: Path to the icon (defaults to exe_path,0)

        Returns:
            bool: True if successful, False otherwise
        """
        if not self.is_admin():
            raise PermissionError("Administrator privileges required for registry operations")

        if icon_path is None:
            icon_path = f'"{exe_path}",0'

        try:
            # Register the application
            app_key = f"Applications\\{app_name}"
            with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, app_key) as key:
                winreg.SetValue(key, None, winreg.REG_SZ, app_name)

            # Set the default icon
            with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, f"{app_key}\\DefaultIcon") as key:
                winreg.SetValue(key, None, winreg.REG_SZ, icon_path)

            # Set the open command
            with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, f"{app_key}\\shell\\open\\command") as key:
                winreg.SetValue(key, None, winreg.REG_SZ, f'"{exe_path}" "%1"')

            return True

        except Exception as e:
            print(f"Error registering application {app_name}: {e}")
            return False

    def get_file_association(self, extension: str) -> Optional[str]:
        """
        Get the current file association for an extension.

        Args:
            extension: File extension (e.g., '.txt')

        Returns:
            Optional[str]: ProgID if found, None otherwise
        """
        try:
            with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, extension) as key:
                value, _ = winreg.QueryValueEx(key, None)
                return value
        except FileNotFoundError:
            return None
        except Exception as e:
            print(f"Error reading file association for {extension}: {e}")
            return None

    def setup_notepad_associations(self, exe_path: str) -> Dict[str, bool]:
        """
        Set up file associations for Notepad Clone (.txt and .enc files).

        Args:
            exe_path: Path to the Notepad Clone executable

        Returns:
            Dict[str, bool]: Results for each association setup
        """
        results = {}

        # Register the application
        results['app_registration'] = self.register_application(
            "Modern Notepad.exe", exe_path
        )

        # Set up .txt files
        results['txt_association'] = self.set_file_association(
            ".txt", "ModernNotepad.txt", "Text Document", exe_path
        )

        # Set up .enc files
        results['enc_association'] = self.set_file_association(
            ".enc", "ModernNotepad.enc", "Encrypted Document", exe_path
        )

        return results