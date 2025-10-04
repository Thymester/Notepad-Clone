import pytest
from unittest.mock import Mock, patch

from features.view_operations.dark_mode import DarkModeAction


class TestDarkModeAction:
    """Test cases for DarkModeAction."""

    def test_dark_mode_action_initialization(self):
        """Test DarkModeAction initializes correctly."""
        mock_parent = Mock()
        action = DarkModeAction(mock_parent)

        assert action.text() == "&Dark Mode"
        assert action.toolTip() == "Toggle dark mode theme"
        assert action.is_dark_mode == False

    def test_execute_toggles_to_dark_mode(self):
        """Test execute toggles to dark mode."""
        mock_parent = Mock()
        action = DarkModeAction(mock_parent)
        action.is_dark_mode = False  # Start in light mode

        with patch.object(action, 'update_theme') as mock_update_theme:
            action.execute()

            assert action.is_dark_mode == True
            mock_update_theme.assert_called_once()

    def test_execute_toggles_to_light_mode(self):
        """Test execute toggles back to light mode."""
        mock_parent = Mock()
        action = DarkModeAction(mock_parent)
        action.is_dark_mode = True  # Start in dark mode

        with patch.object(action, 'update_theme') as mock_update_theme:
            action.execute()

            assert action.is_dark_mode == False
            mock_update_theme.assert_called_once()

    def test_update_theme_dark_mode(self):
        """Test update_theme applies dark theme."""
        mock_parent = Mock()
        action = DarkModeAction(mock_parent)
        action.is_dark_mode = True

        action.update_theme()

        # Verify dark theme was applied
        mock_parent.setStyleSheet.assert_called_once()
        stylesheet = mock_parent.setStyleSheet.call_args[0][0]

        # Check for dark theme elements
        assert "background-color: #2b2b2b" in stylesheet
        assert "color: #ffffff" in stylesheet
        assert action.text() == "&Light Mode"
        assert "Switch to light mode" in action.toolTip()

    def test_update_theme_light_mode(self):
        """Test update_theme applies light theme."""
        mock_parent = Mock()
        action = DarkModeAction(mock_parent)
        action.is_dark_mode = False

        action.update_theme()

        # Verify light theme was applied
        mock_parent.setStyleSheet.assert_called_once()
        stylesheet = mock_parent.setStyleSheet.call_args[0][0]

        # Check for light theme elements
        assert "background-color: #f8f9fa" in stylesheet
        assert "color: #212529" in stylesheet
        assert action.text() == "&Dark Mode"
        assert "Toggle dark mode" in action.toolTip()

    def test_get_dark_theme_stylesheet(self):
        """Test get_dark_theme_stylesheet returns valid CSS."""
        action = DarkModeAction(None)
        stylesheet = action.get_dark_theme_stylesheet()

        assert isinstance(stylesheet, str)
        assert len(stylesheet) > 0
        # Check for key dark theme selectors
        assert "QMainWindow" in stylesheet
        assert "QPlainTextEdit" in stylesheet
        assert "#2b2b2b" in stylesheet  # Dark background
        assert "#ffffff" in stylesheet  # White text

    def test_get_light_theme_stylesheet(self):
        """Test get_light_theme_stylesheet returns valid CSS."""
        action = DarkModeAction(None)
        stylesheet = action.get_light_theme_stylesheet()

        assert isinstance(stylesheet, str)
        assert len(stylesheet) > 0
        # Check for key light theme selectors
        assert "QMainWindow" in stylesheet
        assert "QPlainTextEdit" in stylesheet
        assert "#f8f9fa" in stylesheet  # Light background
        assert "#212529" in stylesheet  # Dark text

    def test_dark_theme_includes_tab_styling(self):
        """Test that dark theme includes tab widget styling."""
        action = DarkModeAction(None)
        stylesheet = action.get_dark_theme_stylesheet()

        assert "QTabWidget::pane" in stylesheet
        assert "QTabBar::tab" in stylesheet
        assert "#1e1e1e" in stylesheet  # Tab content background

    def test_light_theme_includes_tab_styling(self):
        """Test that light theme includes tab widget styling."""
        action = DarkModeAction(None)
        stylesheet = action.get_light_theme_stylesheet()

        assert "QTabWidget::pane" in stylesheet
        assert "QTabBar::tab" in stylesheet
        assert "#ffffff" in stylesheet  # Tab content background

    def test_dark_theme_comprehensive_styling(self):
        """Test that dark theme styles all major UI components."""
        action = DarkModeAction(None)
        stylesheet = action.get_dark_theme_stylesheet()

        # Check for comprehensive component coverage
        components = [
            "QMenuBar", "QMenu", "QToolBar", "QStatusBar",
            "QPushButton", "QDialog", "QLabel", "QComboBox"
        ]

        for component in components:
            assert component in stylesheet, f"Dark theme missing {component} styling"

    def test_light_theme_comprehensive_styling(self):
        """Test that light theme styles all major UI components."""
        action = DarkModeAction(None)
        stylesheet = action.get_light_theme_stylesheet()

        # Check for comprehensive component coverage
        components = [
            "QMenuBar", "QMenu", "QToolBar", "QStatusBar",
            "QPushButton", "QDialog", "QComboBox"
        ]

        for component in components:
            assert component in stylesheet, f"Light theme missing {component} styling"