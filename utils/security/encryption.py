"""
Secure encryption service for encrypted notepads.
Provides AES encryption with PBKDF2 key derivation and secure file formats.
"""

import os
import hashlib
import secrets
from typing import Optional, Tuple, Dict, Any
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.ciphers import algorithms as crypto_algorithms
from cryptography.exceptions import InvalidKey


class EncryptionError(Exception):
    """Base exception for encryption operations."""
    pass


class InvalidPasswordError(EncryptionError):
    """Raised when password is incorrect."""
    pass


class EncryptionService:
    """
    Secure encryption service using AES-256 with PBKDF2 key derivation.
    Supports multiple encryption algorithms and secure file formats.
    """

    # File format constants
    MAGIC_HEADER = b"ENCRYPTED_NOTEPAD_V1"
    SALT_SIZE = 32
    IV_SIZE = 24  # Maximum IV size (for XChaCha20), pad others with zeros
    ALGORITHM_SIZE = 12  # Algorithm field size (enough for "XChaCha20" + padding)
    CHACHA_NONCE_SIZE = 12  # ChaCha20 uses 12-byte nonce
    XCHACHA_NONCE_SIZE = 24  # XChaCha20 uses 24-byte nonce
    AES_IV_SIZE = 16  # AES uses 16-byte IV
    KEY_SIZE = 32  # 256 bits
    ITERATIONS = 100000

    # Supported algorithms
    ALGORITHMS = {
        'AES-256': 'aes256',
        'AES-192': 'aes192',
        'AES-128': 'aes128',
        'ChaCha20': 'chacha20',
        'XChaCha20': 'xchacha20'
    }

    def __init__(self):
        self.backend = default_backend()

    def derive_key(self, password: str, salt: bytes, key_size: int = KEY_SIZE) -> bytes:
        """
        Derive encryption key from password using PBKDF2.

        Args:
            password: User password
            salt: Random salt bytes
            key_size: Desired key size in bytes

        Returns:
            Derived key bytes
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=key_size,
            salt=salt,
            iterations=self.ITERATIONS,
            backend=self.backend
        )
        return kdf.derive(password.encode('utf-8'))

    def encrypt_data(self, data: str, password: str, algorithm: str = 'AES-256') -> bytes:
        """
        Encrypt text data with the specified algorithm.

        Args:
            data: Text to encrypt
            password: Encryption password
            algorithm: Encryption algorithm ('AES-256', 'AES-192', 'AES-128')

        Returns:
            Encrypted data as bytes with header information
        """
        # Generate salt and IV/nonce
        salt = secrets.token_bytes(self.SALT_SIZE)
        if algorithm == 'XChaCha20':
            iv = secrets.token_bytes(self.XCHACHA_NONCE_SIZE)  # 24-byte nonce for XChaCha20
        elif self._is_aead_algorithm(algorithm):
            iv = secrets.token_bytes(self.CHACHA_NONCE_SIZE)  # 12-byte nonce for ChaCha20
        else:
            iv = secrets.token_bytes(self.AES_IV_SIZE)  # 16-byte IV for AES

        # Pad IV to 24 bytes for consistent file format
        iv_padded = iv.ljust(self.IV_SIZE, b'\x00')

        # Derive key
        key_size = self._get_key_size(algorithm)
        key = self.derive_key(password, salt, key_size)

        # Prepare data for encryption
        data_bytes = data.encode('utf-8')

        if algorithm == 'XChaCha20':
            # XChaCha20-Poly1305 (AEAD) - use 24-byte nonce
            subkey, chacha_nonce = self._xchacha20_setup(key, iv)
            chacha = ChaCha20Poly1305(subkey)
            encrypted_data = chacha.encrypt(chacha_nonce, data_bytes, None)  # None for associated data
        elif self._is_aead_algorithm(algorithm):
            # ChaCha20-Poly1305 (AEAD) - use first 12 bytes of IV as nonce
            chacha = ChaCha20Poly1305(key)
            encrypted_data = chacha.encrypt(iv[:self.CHACHA_NONCE_SIZE], data_bytes, None)  # None for associated data
        else:
            # AES with padding
            # Add PKCS7 padding
            padder = padding.PKCS7(algorithms.AES.block_size).padder()
            padded_data = padder.update(data_bytes) + padder.finalize()

            # Encrypt
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
            encryptor = cipher.encryptor()
            encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        # Create file format: MAGIC + SALT + IV + ALGORITHM + ENCRYPTED_DATA
        algorithm_bytes = algorithm.encode('utf-8').ljust(self.ALGORITHM_SIZE, b'\x00')
        file_data = (
            self.MAGIC_HEADER +
            salt +
            iv_padded +
            algorithm_bytes +
            encrypted_data
        )

        return file_data

    def decrypt_data(self, encrypted_data: bytes, password: str) -> str:
        """
        Decrypt encrypted data.

        Args:
            encrypted_data: Encrypted data with header
            password: Decryption password

        Returns:
            Decrypted text

        Raises:
            InvalidPasswordError: If password is incorrect
            EncryptionError: For other decryption errors
        """
        try:
            header_size = len(self.MAGIC_HEADER)
            salt = encrypted_data[header_size:header_size + self.SALT_SIZE]
            iv_padded = encrypted_data[header_size + self.SALT_SIZE:header_size + self.SALT_SIZE + self.IV_SIZE]
            algorithm_bytes = encrypted_data[header_size + self.SALT_SIZE + self.IV_SIZE:header_size + self.SALT_SIZE + self.IV_SIZE + self.ALGORITHM_SIZE]
            encrypted_content = encrypted_data[header_size + self.SALT_SIZE + self.IV_SIZE + self.ALGORITHM_SIZE:]

            # Extract algorithm
            algorithm = algorithm_bytes.decode('utf-8').rstrip('\x00')

            # Unpad IV based on algorithm
            if algorithm == 'XChaCha20':
                iv = iv_padded[:self.XCHACHA_NONCE_SIZE]
            elif self._is_aead_algorithm(algorithm):
                iv = iv_padded[:self.CHACHA_NONCE_SIZE]
            else:
                iv = iv_padded[:16]  # AES uses 16 bytes

            # Derive key
            key_size = self._get_key_size(algorithm)
            key = self.derive_key(password, salt, key_size)

            if algorithm == 'XChaCha20':
                # XChaCha20-Poly1305 (AEAD) - use 24-byte nonce
                subkey, chacha_nonce = self._xchacha20_setup(key, iv)
                chacha = ChaCha20Poly1305(subkey)
                data_bytes = chacha.decrypt(chacha_nonce, encrypted_content, None)  # None for associated data
            elif self._is_aead_algorithm(algorithm):
                # ChaCha20-Poly1305 (AEAD) - use first 12 bytes of IV as nonce
                chacha = ChaCha20Poly1305(key)
                data_bytes = chacha.decrypt(iv[:self.CHACHA_NONCE_SIZE], encrypted_content, None)  # None for associated data
            else:
                # AES decryption
                # Decrypt
                cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
                decryptor = cipher.decryptor()
                padded_data = decryptor.update(encrypted_content) + decryptor.finalize()

                # Remove padding
                unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
                data_bytes = unpadder.update(padded_data) + unpadder.finalize()

            return data_bytes.decode('utf-8')

        except InvalidKey:
            raise InvalidPasswordError("Incorrect password")
        except UnicodeDecodeError:
            # Wrong password often results in undecodable bytes
            raise InvalidPasswordError("Incorrect password or corrupted data")
        except Exception as e:
            # For AES, wrong passwords often result in padding errors
            # Check if this might be a wrong password by looking for padding errors
            if "padding" in str(e).lower() or "mac" in str(e).lower():
                raise InvalidPasswordError("Incorrect password or corrupted data")
            raise EncryptionError(f"Decryption failed: {str(e)}")

    def _get_key_size(self, algorithm: str) -> int:
        """Get key size for the specified algorithm."""
        sizes = {
            'AES-256': 32,
            'AES-192': 24,
            'AES-128': 16,
            'ChaCha20': 32,
            'XChaCha20': 32
        }
        return sizes.get(algorithm, 32)

    def _is_aead_algorithm(self, algorithm: str) -> bool:
        """Check if algorithm uses AEAD (Authenticated Encryption with Associated Data)."""
        return algorithm in ['ChaCha20', 'XChaCha20']

    def _xchacha20_setup(self, key: bytes, nonce: bytes) -> tuple[bytes, bytes]:
        """
        XChaCha20 setup: Generate subkey and 12-byte nonce from 24-byte nonce.

        Args:
            key: 32-byte key
            nonce: 24-byte nonce

        Returns:
            Tuple of (subkey, chacha_nonce)
        """
        # Simplified XChaCha20 construction for compatibility
        # Use PBKDF2-like construction to derive subkey from key and nonce
        import hashlib

        # Create subkey by hashing key + nonce
        subkey_input = key + nonce
        subkey = hashlib.sha256(subkey_input).digest()

        # Create 12-byte ChaCha20 nonce from nonce
        chacha_nonce = nonce[:12]  # Use first 12 bytes of the 24-byte nonce

        return subkey, chacha_nonce

    def is_encrypted_file(self, file_path: str) -> bool:
        """
        Check if a file is an encrypted notepad file.

        Args:
            file_path: Path to the file

        Returns:
            True if file is encrypted, False otherwise
        """
        try:
            with open(file_path, 'rb') as f:
                header = f.read(len(self.MAGIC_HEADER))
                return header == self.MAGIC_HEADER
        except:
            return False

    def generate_secure_password(self, length: int = 20) -> str:
        """
        Generate a highly secure random password with balanced character distribution.

        Args:
            length: Password length (minimum 16, default 20)

        Returns:
            Cryptographically secure random password
        """
        if length < 16:
            length = 16

        # Define character sets for better security
        uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        lowercase = "abcdefghijklmnopqrstuvwxyz"
        digits = "0123456789"
        symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"

        # Ensure at least one character from each set
        password_chars = [
            secrets.choice(uppercase),
            secrets.choice(lowercase),
            secrets.choice(digits),
            secrets.choice(symbols)
        ]

        # Fill the rest randomly from all characters
        all_chars = uppercase + lowercase + digits + symbols
        for _ in range(length - 4):
            password_chars.append(secrets.choice(all_chars))

        # Shuffle to avoid predictable patterns
        secrets.SystemRandom().shuffle(password_chars)

        return ''.join(password_chars)

    def validate_password_strength(self, password: str) -> Dict[str, Any]:
        """
        Validate password strength and provide feedback.

        Args:
            password: Password to validate

        Returns:
            Dictionary with strength assessment
        """
        score = 0
        feedback = []

        if len(password) >= 8:
            score += 1
        else:
            feedback.append("Password should be at least 8 characters long")

        if any(c.isupper() for c in password):
            score += 1
        else:
            feedback.append("Include uppercase letters")

        if any(c.islower() for c in password):
            score += 1
        else:
            feedback.append("Include lowercase letters")

        if any(c.isdigit() for c in password):
            score += 1
        else:
            feedback.append("Include numbers")

        if any(c in "!@#$%^&*" for c in password):
            score += 1
        else:
            feedback.append("Include special characters")

        strength_levels = ["Very Weak", "Weak", "Fair", "Good", "Strong"]
        strength = strength_levels[min(score, 4)]

        return {
            'score': score,
            'strength': strength,
            'feedback': feedback,
            'is_acceptable': score >= 3
        }