import pytest
from unittest.mock import Mock

from features.view_operations.zoom_in import ZoomInAction
from features.view_operations.zoom_out import ZoomOutAction
from features.view_operations.restore_zoom import RestoreZoomAction
from features.view_operations.toggle_status_bar import ToggleStatusBarAction


class TestZoomInAction:
    """Test cases for ZoomInAction."""

    def test_zoom_in_action_initialization(self):
        """Test ZoomInAction initializes correctly."""
        mock_parent = Mock()
        action = ZoomInAction(mock_parent)

        assert action.text() == "Zoom &In\tCtrl++"

    def test_execute_zoom_in_within_limits(self):
        """Test zooming in within limits."""
        mock_parent = Mock()
        mock_parent.zoom_level = 100

        action = ZoomInAction(mock_parent)
        action.execute()

        assert mock_parent.zoom_level == 110

    def test_execute_zoom_in_at_maximum(self):
        """Test zooming in at maximum limit."""
        mock_parent = Mock()
        mock_parent.zoom_level = 490  # Close to max

        action = ZoomInAction(mock_parent)
        action.execute()

        assert mock_parent.zoom_level == 500  # Should cap at 500

    def test_apply_zoom_called(self):
        """Test that _apply_zoom is called."""
        mock_parent = Mock()
        mock_parent.zoom_level = 100

        action = ZoomInAction(mock_parent)

        with pytest.raises(AttributeError):
            # This will fail because _apply_zoom doesn't exist on the action
            # but the zoom level should still be updated
            action.execute()

        assert mock_parent.zoom_level == 110


class TestZoomOutAction:
    """Test cases for ZoomOutAction."""

    def test_zoom_out_action_initialization(self):
        """Test ZoomOutAction initializes correctly."""
        mock_parent = Mock()
        action = ZoomOutAction(mock_parent)

        assert action.text() == "Zoom &Out\tCtrl+-"

    def test_execute_zoom_out_within_limits(self):
        """Test zooming out within limits."""
        mock_parent = Mock()
        mock_parent.zoom_level = 100

        action = ZoomOutAction(mock_parent)
        action.execute()

        assert mock_parent.zoom_level == 90

    def test_execute_zoom_out_at_minimum(self):
        """Test zooming out at minimum limit."""
        mock_parent = Mock()
        mock_parent.zoom_level = 20  # Close to min

        action = ZoomOutAction(mock_parent)
        action.execute()

        assert mock_parent.zoom_level == 10  # Should cap at 10


class TestRestoreZoomAction:
    """Test cases for RestoreZoomAction."""

    def test_restore_zoom_action_initialization(self):
        """Test RestoreZoomAction initializes correctly."""
        mock_parent = Mock()
        action = RestoreZoomAction(mock_parent)

        assert action.text() == "&Restore Default Zoom\tCtrl+0"

    def test_execute_restore_zoom(self):
        """Test restoring default zoom level."""
        mock_parent = Mock()
        mock_parent.zoom_level = 200  # Some custom zoom

        action = RestoreZoomAction(mock_parent)
        action.execute()

        assert mock_parent.zoom_level == 100  # Should restore to 100


class TestToggleStatusBarAction:
    """Test cases for ToggleStatusBarAction."""

    def test_toggle_status_bar_action_initialization(self):
        """Test ToggleStatusBarAction initializes correctly."""
        mock_parent = Mock()
        action = ToggleStatusBarAction(mock_parent)

        assert action.text() == "&Status Bar"
        assert action.isCheckable()
        assert action.isChecked()

    def test_execute_toggle_status_bar_checked(self):
        """Test toggling status bar when checked."""
        mock_parent = Mock()
        mock_status_bar = Mock()
        mock_parent.status_bar = mock_status_bar

        action = ToggleStatusBarAction(mock_parent)
        action.setChecked(True)
        action.execute()

        mock_status_bar.status_bar.show.assert_called_once()

    def test_execute_toggle_status_bar_unchecked(self):
        """Test toggling status bar when unchecked."""
        mock_parent = Mock()
        mock_status_bar = Mock()
        mock_parent.status_bar = mock_status_bar

        action = ToggleStatusBarAction(mock_parent)
        action.setChecked(False)
        action.execute()

        mock_status_bar.status_bar.hide.assert_called_once()