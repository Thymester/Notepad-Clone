"""
Password dialog for encrypted notepads.
Provides UI for password entry, encryption settings, and password strength validation.
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QComboBox, QCheckBox, QProgressBar,
                             QMessageBox, QFormLayout, QGroupBox, QTextEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QIcon

from utils.security.encryption import EncryptionService


class PasswordDialog(QDialog):
    """
    Dialog for password entry and encryption settings.
    """

    def __init__(self, parent=None, mode="encrypt", current_password=None):
        """
        Initialize password dialog.

        Args:
            parent: Parent widget
            mode: "encrypt", "decrypt", or "change"
            current_password: Current password for change mode
        """
        super().__init__(parent)
        self.mode = mode
        self.current_password = current_password
        self.encryption_service = EncryptionService()

        self.setWindowTitle(self._get_title())
        self.setModal(True)
        self.resize(450, 350)

        self.setup_ui()
        self.connect_signals()

    def _get_title(self):
        """Get dialog title based on mode."""
        titles = {
            "encrypt": "Encrypt Document",
            "decrypt": "Decrypt Document",
            "change": "Change Password"
        }
        return titles.get(self.mode, "Password Required")

    def setup_ui(self):
        """Setup the dialog UI."""
        layout = QVBoxLayout()

        # Header
        header_label = QLabel(self._get_header_text())
        header_label.setWordWrap(True)
        header_font = header_label.font()
        header_font.setBold(True)
        header_label.setFont(header_font)
        layout.addWidget(header_label)

        # Password input section
        self.setup_password_section(layout)

        # Encryption settings (only for encrypt mode)
        if self.mode == "encrypt":
            self.setup_encryption_settings(layout)

        # Buttons
        self.setup_buttons(layout)

        self.setLayout(layout)

    def _get_header_text(self):
        """Get header text based on mode."""
        if self.mode == "encrypt":
            return "Enter a password to encrypt this document. Choose a strong password and remember it - there is no way to recover encrypted documents without the password."
        elif self.mode == "decrypt":
            return "Enter the password to decrypt this document."
        elif self.mode == "change":
            return "Enter the current password and a new password for this document."
        else:
            return "Password required to access this document."

    def setup_password_section(self, layout):
        """Setup password input fields."""
        password_group = QGroupBox("Password")
        password_layout = QFormLayout()

        if self.mode == "change":
            # Current password field
            self.current_password_edit = QLineEdit()
            self.current_password_edit.setEchoMode(QLineEdit.Password)
            password_layout.addRow("Current Password:", self.current_password_edit)

        # Password field
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        password_label = "New Password:" if self.mode == "change" else "Password:"
        password_layout.addRow(password_label, self.password_edit)

        # Confirm password field
        self.confirm_password_edit = QLineEdit()
        self.confirm_password_edit.setEchoMode(QLineEdit.Password)
        confirm_label = "Confirm New Password:" if self.mode == "change" else "Confirm Password:"
        password_layout.addRow(confirm_label, self.confirm_password_edit)

        # Show password checkbox
        self.show_password_check = QCheckBox("Show passwords")
        self.show_password_check.stateChanged.connect(self.toggle_password_visibility)
        password_layout.addRow("", self.show_password_check)

        # Password strength indicator (for encrypt/change modes)
        if self.mode in ["encrypt", "change"]:
            strength_layout = QHBoxLayout()
            strength_layout.addWidget(QLabel("Password Strength:"))
            self.strength_bar = QProgressBar()
            self.strength_bar.setRange(0, 5)
            self.strength_bar.setValue(0)
            strength_layout.addWidget(self.strength_bar)
            password_layout.addRow("", strength_layout)

            self.strength_label = QLabel("Very Weak")
            password_layout.addRow("", self.strength_label)

        password_group.setLayout(password_layout)
        layout.addWidget(password_group)

    def setup_encryption_settings(self, layout):
        """Setup encryption algorithm selection."""
        settings_group = QGroupBox("🔐 ENCRYPTION SETTINGS")
        settings_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                color: #FF6B35;
                border: 3px solid #FF6B35;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        settings_layout = QFormLayout()

        # Algorithm selection with HIGH visibility
        algorithm_label = QLabel("CHOOSE ENCRYPTION ALGORITHM:")
        algorithm_label.setStyleSheet("font-weight: bold; font-size: 12px; color: #FF6B35;")
        self.algorithm_combo = QComboBox()
        self.algorithm_combo.addItems(["AES-256 (RECOMMENDED - MAXIMUM SECURITY)", "AES-192 (STRONG SECURITY)", "AES-128 (GOOD SECURITY)", "ChaCha20 (MODERN & FAST)", "XChaCha20 (ENHANCED MODERN - BEST)"])
        self.algorithm_combo.setCurrentText("AES-256 (RECOMMENDED - MAXIMUM SECURITY)")
        self.algorithm_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 4px solid #FF6B35;
                border-radius: 6px;
                background-color: #2D3436;
                color: #FFFFFF;
                font-weight: bold;
                font-size: 11px;
                min-width: 300px;
                min-height: 25px;
            }
            QComboBox:hover {
                border-color: #FF8C42;
                background-color: #34495E;
            }
            QComboBox::drop-down {
                border: none;
                background-color: #FF6B35;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 6px solid white;
                margin-top: 2px;
            }
            QComboBox QAbstractItemView {
                background-color: #2D3436;
                color: #FFFFFF;
                border: 2px solid #FF6B35;
                selection-background-color: #FF6B35;
                selection-color: #FFFFFF;
                font-weight: bold;
            }
        """)
        settings_layout.addRow(algorithm_label, self.algorithm_combo)

        # Algorithm description
        self.algorithm_desc = QLabel("AES-256: MILITARY-GRADE ENCRYPTION - MOST SECURE OPTION RECOMMENDED FOR SENSITIVE DATA")
        self.algorithm_desc.setWordWrap(True)
        self.algorithm_desc.setStyleSheet("""
            QLabel {
                color: #FF6B35;
                font-size: 11px;
                font-weight: bold;
                margin-top: 5px;
                padding: 5px;
                background-color: #2D3436;
                border: 2px solid #FF6B35;
                border-radius: 4px;
            }
        """)
        settings_layout.addRow("", self.algorithm_desc)

        # Connect algorithm change to update description
        self.algorithm_combo.currentTextChanged.connect(self.update_algorithm_description)

        # Generate password button - make it HUGE and visible
        generate_btn = QPushButton("🔑 GENERATE SECURE PASSWORD")
        generate_btn.setStyleSheet("""
            QPushButton {
                padding: 12px 20px;
                background-color: #FF6B35;
                color: white;
                border: 3px solid #FF8C42;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12px;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #FF8C42;
                border-color: #FFA366;
            }
            QPushButton:pressed {
                background-color: #E55A2B;
                border-color: #FF6B35;
            }
        """)
        generate_btn.clicked.connect(self.generate_password)
        settings_layout.addRow("", generate_btn)

        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)

    def setup_buttons(self, layout):
        """Setup dialog buttons."""
        button_layout = QHBoxLayout()

        button_layout.addStretch()

        # Cancel button
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        # OK button
        self.ok_btn = QPushButton(self._get_ok_button_text())
        self.ok_btn.clicked.connect(self.validate_and_accept)
        self.ok_btn.setDefault(True)
        button_layout.addWidget(self.ok_btn)

        layout.addLayout(button_layout)

    def _get_ok_button_text(self):
        """Get OK button text based on mode."""
        texts = {
            "encrypt": "Encrypt",
            "decrypt": "Decrypt",
            "change": "Change Password"
        }
        return texts.get(self.mode, "OK")

    def connect_signals(self):
        """Connect widget signals."""
        if hasattr(self, 'password_edit'):
            self.password_edit.textChanged.connect(self.update_password_strength)

    def toggle_password_visibility(self, state):
        """Toggle password field visibility."""
        mode = QLineEdit.Normal if state else QLineEdit.Password

        if hasattr(self, 'current_password_edit'):
            self.current_password_edit.setEchoMode(mode)
        self.password_edit.setEchoMode(mode)
        self.confirm_password_edit.setEchoMode(mode)

    def update_password_strength(self):
        """Update password strength indicator."""
        if not hasattr(self, 'strength_bar'):
            return

        password = self.password_edit.text()
        if not password:
            self.strength_bar.setValue(0)
            self.strength_label.setText("Very Weak")
            return

        strength_info = self.encryption_service.validate_password_strength(password)
        self.strength_bar.setValue(strength_info['score'])
        self.strength_label.setText(strength_info['strength'])

        # Color coding
        if strength_info['score'] >= 4:
            color = "green"
        elif strength_info['score'] >= 3:
            color = "orange"
        else:
            color = "red"

        self.strength_bar.setStyleSheet(f"QProgressBar::chunk {{ background-color: {color}; }}")

    def generate_password(self):
        """Generate a secure random password."""
        password = self.encryption_service.generate_secure_password()
        self.password_edit.setText(password)
        self.confirm_password_edit.setText(password)

    def validate_and_accept(self):
        """Validate input and accept dialog."""
        try:
            self.validate_input()
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Validation Error", str(e))

    def validate_input(self):
        """Validate user input."""
        # Check passwords match
        password = self.password_edit.text()
        confirm_password = self.confirm_password_edit.text()

        if password != confirm_password:
            raise ValueError("Passwords do not match.")

        if not password:
            raise ValueError("Password cannot be empty.")

        # Check current password for change mode
        if self.mode == "change" and hasattr(self, 'current_password_edit'):
            current_pass = self.current_password_edit.text()
            if not current_pass:
                raise ValueError("Current password is required.")
            # Note: Actual validation happens in the calling code

        # Check password strength for encryption
        if self.mode == "encrypt":
            strength_info = self.encryption_service.validate_password_strength(password)
            if not strength_info['is_acceptable']:
                response = QMessageBox.question(
                    self, "Weak Password",
                    "The password is weak. Continue anyway?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if response == QMessageBox.No:
                    raise ValueError("Please choose a stronger password.")

    def get_password(self):
        """Get the entered password."""
        return self.password_edit.text()

    def get_current_password(self):
        """Get the current password (for change mode)."""
        if hasattr(self, 'current_password_edit'):
            return self.current_password_edit.text()
        return None

    def get_algorithm(self):
        """Get the selected encryption algorithm."""
        if hasattr(self, 'algorithm_combo'):
            algorithm_text = self.algorithm_combo.currentText()
            # Extract algorithm name from "Algorithm (Description)" format
            if " (" in algorithm_text:
                return algorithm_text.split(" (")[0]
            return algorithm_text
        return "AES-256"

    def update_algorithm_description(self, algorithm_text):
        """Update the algorithm description based on selection."""
        descriptions = {
            "AES-256 (RECOMMENDED - MAXIMUM SECURITY)": "AES-256: MILITARY-GRADE ENCRYPTION - MOST SECURE OPTION RECOMMENDED FOR SENSITIVE DATA",
            "AES-192 (STRONG SECURITY)": "AES-192: VERY STRONG ENCRYPTION - EXCELLENT SECURITY WITH GOOD PERFORMANCE",
            "AES-128 (GOOD SECURITY)": "AES-128: STRONG ENCRYPTION - GOOD SECURITY FOR MOST EVERYDAY USE",
            "ChaCha20 (MODERN & FAST)": "ChaCha20: MODERN FAST ENCRYPTION - EXCELLENT SECURITY WITH HIGH SPEED",
            "XChaCha20 (ENHANCED MODERN - BEST)": "XChaCha20: ENHANCED MODERN ENCRYPTION - BEST SPEED/SECURITY BALANCE WITH RANDOM NONCES"
        }
        self.algorithm_desc.setText(descriptions.get(algorithm_text, ""))


class PasswordPromptDialog(QDialog):
    """
    Simple dialog for password entry (decrypt mode).
    """

    def __init__(self, parent=None, title="Enter Password"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(300, 150)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Enter password to decrypt the document:"))

        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_edit)

        self.show_password_check = QCheckBox("Show password")
        self.show_password_check.stateChanged.connect(
            lambda: self.password_edit.setEchoMode(
                QLineEdit.Normal if self.show_password_check.isChecked() else QLineEdit.Password
            )
        )
        layout.addWidget(self.show_password_check)

        button_layout = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        ok_btn = QPushButton("Decrypt")
        ok_btn.clicked.connect(self.accept)
        ok_btn.setDefault(True)
        button_layout.addWidget(ok_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def get_password(self):
        """Get the entered password."""
        return self.password_edit.text()