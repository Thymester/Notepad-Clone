"""
Unit tests for encryption service.
Tests AES and ChaCha20 encryption/decryption, password generation, and validation.
"""

import pytest
import os
from utils.security.encryption import EncryptionService, InvalidPasswordError, EncryptionError


class TestEncryptionService:
    """Test cases for EncryptionService."""

    def setup_method(self):
        """Set up test fixtures."""
        self.service = EncryptionService()
        self.test_password = "TestPassword123!"
        self.test_data = "This is test data for encryption.\nIt has multiple lines.\nAnd special chars: !@#$%^&*()"

    def test_encrypt_decrypt_aes256(self):
        """Test AES-256 encryption and decryption round trip."""
        # Encrypt
        encrypted = self.service.encrypt_data(self.test_data, self.test_password, "AES-256")

        # Decrypt
        decrypted = self.service.decrypt_data(encrypted, self.test_password)

        assert decrypted == self.test_data

    def test_encrypt_decrypt_aes192(self):
        """Test AES-192 encryption and decryption round trip."""
        encrypted = self.service.encrypt_data(self.test_data, self.test_password, "AES-192")
        decrypted = self.service.decrypt_data(encrypted, self.test_password)

        assert decrypted == self.test_data

    def test_encrypt_decrypt_aes128(self):
        """Test AES-128 encryption and decryption round trip."""
        encrypted = self.service.encrypt_data(self.test_data, self.test_password, "AES-128")
        decrypted = self.service.decrypt_data(encrypted, self.test_password)

        assert decrypted == self.test_data

    def test_encrypt_decrypt_chacha20(self):
        """Test ChaCha20 encryption and decryption round trip."""
        encrypted = self.service.encrypt_data(self.test_data, self.test_password, "ChaCha20")
        decrypted = self.service.decrypt_data(encrypted, self.test_password)

        assert decrypted == self.test_data

    def test_encrypt_decrypt_xchacha20(self):
        """Test XChaCha20 encryption and decryption round trip."""
        encrypted = self.service.encrypt_data(self.test_data, self.test_password, "XChaCha20")
        decrypted = self.service.decrypt_data(encrypted, self.test_password)

        assert decrypted == self.test_data

    def test_wrong_password_fails(self):
        """Test that wrong password raises InvalidPasswordError."""
        encrypted = self.service.encrypt_data(self.test_data, self.test_password, "AES-256")

        with pytest.raises(InvalidPasswordError):
            self.service.decrypt_data(encrypted, "WrongPassword123!")

    def test_invalid_file_format(self):
        """Test that invalid file format raises EncryptionError."""
        invalid_data = b"Not an encrypted file"

        with pytest.raises(EncryptionError):
            self.service.decrypt_data(invalid_data, self.test_password)

    def test_empty_data(self):
        """Test encryption/decryption of empty data."""
        empty_data = ""
        encrypted = self.service.encrypt_data(empty_data, self.test_password, "AES-256")
        decrypted = self.service.decrypt_data(encrypted, self.test_password)

        assert decrypted == empty_data

    def test_unicode_data(self):
        """Test encryption/decryption of Unicode data."""
        unicode_data = "Hello 世界 🌍 émojis 🎉 and spëcial chärs"
        encrypted = self.service.encrypt_data(unicode_data, self.test_password, "ChaCha20")
        decrypted = self.service.decrypt_data(encrypted, self.test_password)

        assert decrypted == unicode_data

    def test_different_algorithms_produce_different_output(self):
        """Test that different algorithms produce different encrypted output."""
        aes_encrypted = self.service.encrypt_data(self.test_data, self.test_password, "AES-256")
        chacha_encrypted = self.service.encrypt_data(self.test_data, self.test_password, "ChaCha20")

        # Should be different (different headers and encryption methods)
        assert aes_encrypted != chacha_encrypted

    def test_file_format_integrity(self):
        """Test that encrypted data has correct file format."""
        encrypted = self.service.encrypt_data(self.test_data, self.test_password, "AES-256")

        # Check magic header
        assert encrypted.startswith(self.service.MAGIC_HEADER)

        # Check total size (header + salt + iv + algorithm + encrypted data)
        expected_min_size = len(self.service.MAGIC_HEADER) + self.service.SALT_SIZE + self.service.IV_SIZE + 8
        assert len(encrypted) >= expected_min_size

    def test_generate_secure_password_length(self):
        """Test password generation length requirements."""
        # Test default length
        password = self.service.generate_secure_password()
        assert len(password) == 20

        # Test custom length >= 16
        password = self.service.generate_secure_password(16)
        assert len(password) == 16

        password = self.service.generate_secure_password(25)
        assert len(password) == 25

        # Test minimum enforcement
        password = self.service.generate_secure_password(10)  # Should be 16
        assert len(password) == 16

    def test_generate_secure_password_character_diversity(self):
        """Test that generated passwords contain all required character types."""
        password = self.service.generate_secure_password(20)

        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

        assert has_upper, "Password should contain uppercase letters"
        assert has_lower, "Password should contain lowercase letters"
        assert has_digit, "Password should contain digits"
        assert has_symbol, "Password should contain symbols"

    def test_generate_secure_password_uniqueness(self):
        """Test that generated passwords are unique."""
        passwords = [self.service.generate_secure_password() for _ in range(100)]
        unique_passwords = set(passwords)

        # Should have very high uniqueness (allowing for tiny chance of collision)
        assert len(unique_passwords) >= 95, "Generated passwords should be highly unique"

    def test_password_strength_validation(self):
        """Test password strength validation."""
        # Very weak password (no valid characters)
        weak_result = self.service.validate_password_strength("")
        assert weak_result['score'] == 0
        assert weak_result['strength'] == "Very Weak"
        assert not weak_result['is_acceptable']

        # Weak password (only digits)
        weak_result = self.service.validate_password_strength("123")
        assert weak_result['score'] == 1
        assert weak_result['strength'] == "Weak"
        assert not weak_result['is_acceptable']

        # Strong password
        strong_result = self.service.validate_password_strength("MySecurePass123!")
        assert strong_result['score'] >= 3
        assert strong_result['is_acceptable']

        # Very strong password
        very_strong = self.service.validate_password_strength("V3ryStr0ngP@ssw0rd!")
        assert very_strong['score'] == 5
        assert very_strong['strength'] == "Strong"
        assert very_strong['is_acceptable']

    def test_key_sizes(self):
        """Test that correct key sizes are returned for algorithms."""
        assert self.service._get_key_size("AES-256") == 32
        assert self.service._get_key_size("AES-192") == 24
        assert self.service._get_key_size("AES-128") == 16
        assert self.service._get_key_size("ChaCha20") == 32
        assert self.service._get_key_size("XChaCha20") == 32
        assert self.service._get_key_size("Unknown") == 32  # Default

    def test_aead_detection(self):
        """Test AEAD algorithm detection."""
        assert self.service._is_aead_algorithm("ChaCha20") == True
        assert self.service._is_aead_algorithm("XChaCha20") == True
        assert self.service._is_aead_algorithm("AES-256") == False
        assert self.service._is_aead_algorithm("AES-192") == False
        assert self.service._is_aead_algorithm("AES-128") == False

    def test_is_encrypted_file(self):
        """Test encrypted file detection."""
        # Create a temporary encrypted file
        import tempfile
        encrypted_data = self.service.encrypt_data(self.test_data, self.test_password, "AES-256")

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(encrypted_data)
            temp_path = temp_file.name

        try:
            assert self.service.is_encrypted_file(temp_path) == True

            # Test non-encrypted file
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as text_file:
                text_file.write("Plain text file")
                text_path = text_file.name

            try:
                assert self.service.is_encrypted_file(text_path) == False
            finally:
                os.unlink(text_path)

        finally:
            os.unlink(temp_path)

    def test_large_data_encryption(self):
        """Test encryption/decryption of large data."""
        large_data = "A" * 10000 + "Special chars: !@#$%^&*()" + "\n" * 1000
        encrypted = self.service.encrypt_data(large_data, self.test_password, "AES-256")
        decrypted = self.service.decrypt_data(encrypted, self.test_password)

        assert decrypted == large_data

    def test_algorithm_persistence(self):
        """Test that algorithm information is preserved in encrypted data."""
        for algorithm in ["AES-256", "AES-192", "AES-128", "ChaCha20", "XChaCha20"]:
            encrypted = self.service.encrypt_data(self.test_data, self.test_password, algorithm)
            decrypted = self.service.decrypt_data(encrypted, self.test_password)
            assert decrypted == self.test_data