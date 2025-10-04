from PyQt5.QtGui import QIcon, QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt


class ModernIcon:
    """
    A class for creating modern, custom icons for the notepad application.
    """

    @staticmethod
    def create_icon(icon_type, size=24, color="#2C3E50"):
        """
        Create a custom icon based on the specified type.

        Args:
            icon_type (str): The type of icon to create
            size (int): The size of the icon in pixels
            color (str): The color of the icon (not currently used)

        Returns:
            QIcon: The created icon
        """
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen(Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)

        if icon_type == "new":
            # Modern document icon
            painter.setBrush(Qt.white)
            painter.drawRoundedRect(4, 2, size-8, size-4, 2, 2)
            painter.drawLine(8, 8, size-8, 8)
            painter.drawLine(8, 12, size-8, 12)
            painter.drawLine(8, 16, size-6, 16)

        elif icon_type == "open":
            # Modern folder icon
            painter.setBrush(Qt.lightGray)
            painter.drawRoundedRect(2, 8, size-4, size-10, 2, 2)
            painter.drawRoundedRect(6, 6, 8, 4, 1, 1)

        elif icon_type == "save":
            # Modern floppy/save icon
            painter.setBrush(Qt.lightGray)
            painter.drawRoundedRect(3, 2, size-6, size-4, 2, 2)
            painter.setBrush(Qt.white)
            painter.drawRect(6, 2, size-12, 8)
            painter.setBrush(Qt.darkGray)
            painter.drawRect(8, 12, size-16, size-16)

        elif icon_type == "print":
            # Modern printer icon
            painter.setBrush(Qt.lightGray)
            painter.drawRoundedRect(4, 8, size-8, size-12, 2, 2)
            painter.setBrush(Qt.white)
            painter.drawRect(6, 4, size-12, 6)
            painter.drawRect(8, size-8, size-16, 4)

        elif icon_type == "find":
            # Modern search icon
            painter.setBrush(Qt.transparent)
            painter.drawEllipse(4, 4, 12, 12)
            pen.setWidth(3)
            painter.setPen(pen)
            painter.drawLine(14, 14, size-4, size-4)

        elif icon_type == "cut":
            # Modern scissors icon
            painter.setBrush(Qt.transparent)
            painter.drawEllipse(4, 4, 6, 6)
            painter.drawEllipse(4, 14, 6, 6)
            painter.drawLine(10, 10, size-4, 4)
            painter.drawLine(10, 14, size-4, size-4)

        elif icon_type == "copy":
            # Modern copy icon
            painter.setBrush(Qt.white)
            painter.drawRoundedRect(6, 6, size-10, size-10, 1, 1)
            painter.setBrush(Qt.lightGray)
            painter.drawRoundedRect(2, 2, size-10, size-10, 1, 1)

        elif icon_type == "paste":
            # Modern clipboard icon
            painter.setBrush(Qt.lightGray)
            painter.drawRoundedRect(4, 6, size-8, size-8, 2, 2)
            painter.setBrush(Qt.white)
            painter.drawRoundedRect(8, 2, size-16, 6, 1, 1)

        elif icon_type == "undo":
            # Modern undo arrow
            painter.setBrush(Qt.transparent)
            painter.drawArc(6, 6, 12, 12, 90*16, 180*16)
            painter.drawLine(6, 12, 2, 8)
            painter.drawLine(6, 12, 2, 16)

        elif icon_type == "redo":
            # Modern redo arrow
            painter.setBrush(Qt.transparent)
            painter.drawArc(6, 6, 12, 12, 90*16, -180*16)
            painter.drawLine(18, 12, 22, 8)
            painter.drawLine(18, 12, 22, 16)

        elif icon_type == "zoom_in":
            # Modern zoom in icon
            painter.setBrush(Qt.transparent)
            painter.drawEllipse(4, 4, 12, 12)
            painter.drawLine(10, 8, 10, 12)
            painter.drawLine(8, 10, 12, 10)
            pen.setWidth(3)
            painter.setPen(pen)
            painter.drawLine(14, 14, size-4, size-4)

        elif icon_type == "zoom_out":
            # Modern zoom out icon
            painter.setBrush(Qt.transparent)
            painter.drawEllipse(4, 4, 12, 12)
            painter.drawLine(8, 10, 12, 10)
            pen.setWidth(3)
            painter.setPen(pen)
            painter.drawLine(14, 14, size-4, size-4)

        painter.end()
        return QIcon(pixmap)