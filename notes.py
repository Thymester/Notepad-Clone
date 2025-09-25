import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPlainTextEdit, QAction, QFileDialog, 
    QMessageBox, QInputDialog, QVBoxLayout, QWidget, QStatusBar,
    QFontDialog, QColorDialog, QCheckBox, QDialog, QLabel, QLineEdit,
    QPushButton, QHBoxLayout, QTextEdit, QSplitter, QMenuBar, QToolBar
)
from PyQt5.QtGui import QIcon, QKeySequence, QTextCursor, QFont, QTextCharFormat, QPixmap, QPainter, QPen, QTextDocument
from PyQt5.QtCore import Qt, QSettings, QTimer, pyqtSignal, QSize
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPageSetupDialog
import datetime


class ModernIcon:
    @staticmethod
    def create_icon(icon_type, size=24, color="#2C3E50"):
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


class FindReplaceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_editor = parent
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Find and Replace")
        self.setFixedSize(400, 200)
        layout = QVBoxLayout()
        
        # Find section
        find_layout = QHBoxLayout()
        find_layout.addWidget(QLabel("Find:"))
        self.find_input = QLineEdit()
        find_layout.addWidget(self.find_input)
        layout.addLayout(find_layout)
        
        # Replace section
        replace_layout = QHBoxLayout()
        replace_layout.addWidget(QLabel("Replace:"))
        self.replace_input = QLineEdit()
        replace_layout.addWidget(self.replace_input)
        layout.addLayout(replace_layout)
        
        # Options
        self.match_case = QCheckBox("Match case")
        self.wrap_around = QCheckBox("Wrap around")
        self.wrap_around.setChecked(True)
        layout.addWidget(self.match_case)
        layout.addWidget(self.wrap_around)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.find_next_btn = QPushButton("Find Next")
        self.replace_btn = QPushButton("Replace")
        self.replace_all_btn = QPushButton("Replace All")
        self.cancel_btn = QPushButton("Cancel")
        
        button_layout.addWidget(self.find_next_btn)
        button_layout.addWidget(self.replace_btn)
        button_layout.addWidget(self.replace_all_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Connect signals
        self.find_next_btn.clicked.connect(self.find_next)
        self.replace_btn.clicked.connect(self.replace_current)
        self.replace_all_btn.clicked.connect(self.replace_all)
        self.cancel_btn.clicked.connect(self.close)
        
    def find_next(self):
        if self.parent_editor:
            self.parent_editor.find_text_advanced(
                self.find_input.text(),
                self.match_case.isChecked(),
                self.wrap_around.isChecked()
            )
            
    def replace_current(self):
        if self.parent_editor:
            self.parent_editor.replace_current_selection(
                self.find_input.text(),
                self.replace_input.text(),
                self.match_case.isChecked()
            )
            
    def replace_all(self):
        if self.parent_editor:
            count = self.parent_editor.replace_all_text(
                self.find_input.text(),
                self.replace_input.text(),
                self.match_case.isChecked()
            )
            QMessageBox.information(self, "Replace All", f"Replaced {count} occurrences.")


class ModernNotepad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file_path = ""
        self.is_modified = False
        self.settings = QSettings("ModernNotepad", "Settings")
        self.find_replace_dialog = None
        self.last_find_text = ""
        self.zoom_level = 100
        
        self.init_ui()
        self.create_menus()
        self.create_toolbar()
        self.create_status_bar()
        self.load_settings()
        self.update_title()
        
        # Connect text change signal
        self.text_edit.textChanged.connect(self.on_text_changed)
        
    def init_ui(self):
        self.setWindowTitle("Modern Notepad")
        self.setGeometry(200, 200, 900, 700)
        
        # Set modern dark theme colors
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
                color: #212529;
            }
            QPlainTextEdit {
                background-color: #ffffff;
                border: 1px solid #e9ecef;
                border-radius: 4px;
                padding: 8px;
                font-family: 'Segoe UI', Consolas, 'Courier New', monospace;
                line-height: 1.4;
            }
            QMenuBar {
                background-color: #ffffff;
                border-bottom: 1px solid #e9ecef;
                padding: 4px;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 6px 12px;
                border-radius: 4px;`
            }
            QMenuBar::item:selected {
                background-color: #e9ecef;
            }
            QToolBar {
                background-color: #ffffff;
                border: none;
                border-bottom: 1px solid #e9ecef;
                spacing: 4px;
                padding: 8px;
            }
            QToolBar::separator {
                background-color: #e9ecef;
                width: 1px;
                margin: 4px;
            }
            QStatusBar {
                background-color: #f8f9fa;
                border-top: 1px solid #e9ecef;
                padding: 4px;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
            QDialog {
                background-color: #ffffff;
                border: 1px solid #e9ecef;
                border-radius: 8px;
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Text editor
        self.text_edit = QPlainTextEdit()
        self.text_edit.setLineWrapMode(QPlainTextEdit.WidgetWidth)
        layout.addWidget(self.text_edit)
        
        # Set modern font
        font = QFont("Segoe UI", 11)
        if not font.exactMatch():
            font = QFont("Consolas", 11)
        self.text_edit.setFont(font)
        
    def create_menus(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        new_action = QAction(ModernIcon.create_icon("new"), "&New\tCtrl+N", self)
        new_action.setShortcut(QKeySequence.New)
        new_action.setStatusTip("Create a new file")
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)
        
        new_window_action = QAction(ModernIcon.create_icon("new"), "New &Window\tCtrl+Shift+N", self)
        new_window_action.setShortcut(QKeySequence("Ctrl+Shift+N"))
        new_window_action.triggered.connect(self.new_window)
        file_menu.addAction(new_window_action)
        
        open_action = QAction(ModernIcon.create_icon("open"), "&Open...\tCtrl+O", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.setStatusTip("Open an existing file")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        save_action = QAction(ModernIcon.create_icon("save"), "&Save\tCtrl+S", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.setStatusTip("Save the current file")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        save_as_action = QAction(ModernIcon.create_icon("save"), "Save &As...\tCtrl+Shift+S", self)
        save_as_action.setShortcut(QKeySequence.SaveAs)
        save_as_action.triggered.connect(self.save_as_file)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        page_setup_action = QAction("Page Set&up...", self)
        page_setup_action.triggered.connect(self.page_setup)
        file_menu.addAction(page_setup_action)
        
        print_action = QAction(ModernIcon.create_icon("print"), "&Print...\tCtrl+P", self)
        print_action.setShortcut(QKeySequence.Print)
        print_action.triggered.connect(self.print_file)
        file_menu.addAction(print_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("&Edit")
        
        undo_action = QAction(ModernIcon.create_icon("undo"), "&Undo\tCtrl+Z", self)
        undo_action.setShortcut(QKeySequence.Undo)
        undo_action.triggered.connect(self.text_edit.undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction(ModernIcon.create_icon("redo"), "&Redo\tCtrl+Y", self)
        redo_action.setShortcut(QKeySequence("Ctrl+Y"))
        redo_action.triggered.connect(self.text_edit.redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        cut_action = QAction(ModernIcon.create_icon("cut"), "Cu&t\tCtrl+X", self)
        cut_action.setShortcut(QKeySequence.Cut)
        cut_action.triggered.connect(self.text_edit.cut)
        edit_menu.addAction(cut_action)
        
        copy_action = QAction(ModernIcon.create_icon("copy"), "&Copy\tCtrl+C", self)
        copy_action.setShortcut(QKeySequence.Copy)
        copy_action.triggered.connect(self.text_edit.copy)
        edit_menu.addAction(copy_action)
        
        paste_action = QAction(ModernIcon.create_icon("paste"), "&Paste\tCtrl+V", self)
        paste_action.setShortcut(QKeySequence.Paste)
        paste_action.triggered.connect(self.text_edit.paste)
        edit_menu.addAction(paste_action)
        
        delete_action = QAction("&Delete\tDel", self)
        delete_action.setShortcut(QKeySequence.Delete)
        delete_action.triggered.connect(self.delete_selected)
        edit_menu.addAction(delete_action)
        
        edit_menu.addSeparator()
        
        find_action = QAction(ModernIcon.create_icon("find"), "&Find...\tCtrl+F", self)
        find_action.setShortcut(QKeySequence.Find)
        find_action.triggered.connect(self.show_find_replace)
        edit_menu.addAction(find_action)
        
        find_next_action = QAction("Find &Next\tF3", self)
        find_next_action.setShortcut(QKeySequence("F3"))
        find_next_action.triggered.connect(self.find_next)
        edit_menu.addAction(find_next_action)
        
        find_previous_action = QAction("Find &Previous\tShift+F3", self)
        find_previous_action.setShortcut(QKeySequence("Shift+F3"))
        find_previous_action.triggered.connect(self.find_previous)
        edit_menu.addAction(find_previous_action)
        
        replace_action = QAction("&Replace...\tCtrl+H", self)
        replace_action.setShortcut(QKeySequence.Replace)
        replace_action.triggered.connect(self.show_find_replace)
        edit_menu.addAction(replace_action)
        
        goto_action = QAction("&Go To...\tCtrl+G", self)
        goto_action.setShortcut(QKeySequence("Ctrl+G"))
        goto_action.triggered.connect(self.goto_line)
        edit_menu.addAction(goto_action)
        
        edit_menu.addSeparator()
        
        select_all_action = QAction("Select &All\tCtrl+A", self)
        select_all_action.setShortcut(QKeySequence.SelectAll)
        select_all_action.triggered.connect(self.text_edit.selectAll)
        edit_menu.addAction(select_all_action)
        
        time_date_action = QAction("Time/&Date\tF5", self)
        time_date_action.setShortcut(QKeySequence("F5"))
        time_date_action.triggered.connect(self.insert_time_date)
        edit_menu.addAction(time_date_action)
        
        # Format menu
        format_menu = menubar.addMenu("F&ormat")
        
        self.word_wrap_action = QAction("&Word Wrap", self)
        self.word_wrap_action.setCheckable(True)
        self.word_wrap_action.setChecked(True)
        self.word_wrap_action.triggered.connect(self.toggle_word_wrap)
        format_menu.addAction(self.word_wrap_action)
        
        font_action = QAction("&Font...", self)
        font_action.triggered.connect(self.change_font)
        format_menu.addAction(font_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        zoom_menu = view_menu.addMenu("&Zoom")
        
        zoom_in_action = QAction(ModernIcon.create_icon("zoom_in"), "Zoom &In\tCtrl++", self)
        zoom_in_action.setShortcut(QKeySequence.ZoomIn)
        zoom_in_action.triggered.connect(self.zoom_in)
        zoom_menu.addAction(zoom_in_action)
        
        zoom_out_action = QAction(ModernIcon.create_icon("zoom_out"), "Zoom &Out\tCtrl+-", self)
        zoom_out_action.setShortcut(QKeySequence.ZoomOut)
        zoom_out_action.triggered.connect(self.zoom_out)
        zoom_menu.addAction(zoom_out_action)
        
        restore_zoom_action = QAction("&Restore Default Zoom\tCtrl+0", self)
        restore_zoom_action.setShortcut(QKeySequence("Ctrl+0"))
        restore_zoom_action.triggered.connect(self.restore_zoom)
        zoom_menu.addAction(restore_zoom_action)
        
        self.status_bar_action = QAction("&Status Bar", self)
        self.status_bar_action.setCheckable(True)
        self.status_bar_action.setChecked(True)
        self.status_bar_action.triggered.connect(self.toggle_status_bar)
        view_menu.addAction(self.status_bar_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About Modern Notepad", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def create_toolbar(self):
        toolbar = self.addToolBar("Main")
        toolbar.setMovable(False)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        toolbar.setIconSize(QSize(24, 24))
        
        # Add common actions to toolbar with modern icons
        new_action = QAction(ModernIcon.create_icon("new"), "New", self)
        new_action.setShortcut(QKeySequence.New)
        new_action.setToolTip("Create a new file (Ctrl+N)")
        new_action.triggered.connect(self.new_file)
        toolbar.addAction(new_action)
        
        open_action = QAction(ModernIcon.create_icon("open"), "Open", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.setToolTip("Open an existing file (Ctrl+O)")
        open_action.triggered.connect(self.open_file)
        toolbar.addAction(open_action)
        
        save_action = QAction(ModernIcon.create_icon("save"), "Save", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.setToolTip("Save the current file (Ctrl+S)")
        save_action.triggered.connect(self.save_file)
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()
        
        # Edit actions
        cut_action = QAction(ModernIcon.create_icon("cut"), "Cut", self)
        cut_action.setShortcut(QKeySequence.Cut)
        cut_action.setToolTip("Cut selected text (Ctrl+X)")
        cut_action.triggered.connect(self.text_edit.cut)
        toolbar.addAction(cut_action)
        
        copy_action = QAction(ModernIcon.create_icon("copy"), "Copy", self)
        copy_action.setShortcut(QKeySequence.Copy)
        copy_action.setToolTip("Copy selected text (Ctrl+C)")
        copy_action.triggered.connect(self.text_edit.copy)
        toolbar.addAction(copy_action)
        
        paste_action = QAction(ModernIcon.create_icon("paste"), "Paste", self)
        paste_action.setShortcut(QKeySequence.Paste)
        paste_action.setToolTip("Paste text (Ctrl+V)")
        paste_action.triggered.connect(self.text_edit.paste)
        toolbar.addAction(paste_action)
        
        toolbar.addSeparator()
        
        # Undo/Redo
        undo_action = QAction(ModernIcon.create_icon("undo"), "Undo", self)
        undo_action.setShortcut(QKeySequence.Undo)
        undo_action.setToolTip("Undo last action (Ctrl+Z)")
        undo_action.triggered.connect(self.text_edit.undo)
        toolbar.addAction(undo_action)
        
        redo_action = QAction(ModernIcon.create_icon("redo"), "Redo", self)
        redo_action.setShortcut(QKeySequence("Ctrl+Y"))
        redo_action.setToolTip("Redo last action (Ctrl+Y)")
        redo_action.triggered.connect(self.text_edit.redo)
        toolbar.addAction(redo_action)
        
        toolbar.addSeparator()
        
        # Find and zoom
        find_action = QAction(ModernIcon.create_icon("find"), "Find", self)
        find_action.setShortcut(QKeySequence.Find)
        find_action.setToolTip("Find text (Ctrl+F)")
        find_action.triggered.connect(self.show_find_replace)
        toolbar.addAction(find_action)
        
        print_action = QAction(ModernIcon.create_icon("print"), "Print", self)
        print_action.setShortcut(QKeySequence.Print)
        print_action.setToolTip("Print document (Ctrl+P)")
        print_action.triggered.connect(self.print_file)
        toolbar.addAction(print_action)
        
    def create_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Line and column info
        self.line_col_label = QLabel("Line 1, Column 1")
        self.status_bar.addPermanentWidget(self.line_col_label)
        
        # Zoom level
        self.zoom_label = QLabel("100%")
        self.status_bar.addPermanentWidget(self.zoom_label)
        
        # Update cursor position
        self.text_edit.cursorPositionChanged.connect(self.update_cursor_position)
        
    def update_cursor_position(self):
        cursor = self.text_edit.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber() + 1
        self.line_col_label.setText(f"Line {line}, Column {col}")
        
    def on_text_changed(self):
        if not self.is_modified:
            self.is_modified = True
            self.update_title()
            
    def update_title(self):
        title = "Modern Notepad"
        if self.current_file_path:
            filename = os.path.basename(self.current_file_path)
            title = f"{filename} - {title}"
        else:
            title = f"Untitled - {title}"
            
        if self.is_modified:
            title = f"*{title}"
            
        self.setWindowTitle(title)
        
    def new_file(self):
        if self.check_save_changes():
            self.text_edit.clear()
            self.current_file_path = ""
            self.is_modified = False
            self.update_title()
            
    def new_window(self):
        new_window = ModernNotepad()
        new_window.show()
        
    def open_file(self):
        if self.check_save_changes():
            file_path, _ = QFileDialog.getOpenFileName(
                self, 'Open File', '', 
                'Text files (*.txt);;All files (*.*)'
            )
            if file_path:
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        self.text_edit.setPlainText(content)
                        self.current_file_path = file_path
                        self.is_modified = False
                        self.update_title()
                        self.status_bar.showMessage(f"Opened: {file_path}", 2000)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Could not open file: {str(e)}")
                    
    def save_file(self):
        if self.current_file_path:
            return self.save_to_path(self.current_file_path)
        else:
            return self.save_as_file()
            
    def save_as_file(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, 'Save File', '', 
            'Text files (*.txt);;All files (*.*)'
        )
        if file_path:
            return self.save_to_path(file_path)
        return False
        
    def save_to_path(self, file_path):
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.text_edit.toPlainText())
                self.current_file_path = file_path
                self.is_modified = False
                self.update_title()
                self.status_bar.showMessage(f"Saved: {file_path}", 2000)
                return True
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save file: {str(e)}")
            return False
            
    def check_save_changes(self):
        if self.is_modified:
            reply = QMessageBox.question(
                self, "Modern Notepad",
                "Do you want to save changes to this file?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Save
            )
            
            if reply == QMessageBox.Save:
                return self.save_file()
            elif reply == QMessageBox.Cancel:
                return False
                
        return True
        
    def page_setup(self):
        printer = QPrinter()
        dialog = QPageSetupDialog(printer, self)
        dialog.exec_()
        
    def print_file(self):
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            self.text_edit.print_(printer)
            
    def delete_selected(self):
        cursor = self.text_edit.textCursor()
        if cursor.hasSelection():
            cursor.removeSelectedText()
        else:
            cursor.deleteChar()
            
    def show_find_replace(self):
        if not self.find_replace_dialog:
            self.find_replace_dialog = FindReplaceDialog(self)
        self.find_replace_dialog.show()
        self.find_replace_dialog.raise_()
        self.find_replace_dialog.activateWindow()
        
    def find_text_advanced(self, text, match_case=False, wrap_around=True):
        if not text:
            return
            
        self.last_find_text = text
        flags = QTextDocument.FindFlags()
        if match_case:
            flags |= QTextDocument.FindCaseSensitively
            
        cursor = self.text_edit.textCursor()
        found_cursor = self.text_edit.document().find(text, cursor, flags)
        
        if found_cursor.isNull() and wrap_around:
            # Start from beginning
            found_cursor = self.text_edit.document().find(text, 0, flags)
            
        if not found_cursor.isNull():
            self.text_edit.setTextCursor(found_cursor)
        else:
            QMessageBox.information(self, "Find", f"Cannot find '{text}'")
            
    def find_next(self):
        if self.last_find_text:
            self.find_text_advanced(self.last_find_text, wrap_around=True)
        else:
            self.show_find_replace()
            
    def find_previous(self):
        if self.last_find_text:
            cursor = self.text_edit.textCursor()
            flags = QTextDocument.FindBackward
            found_cursor = self.text_edit.document().find(self.last_find_text, cursor, flags)
            
            if found_cursor.isNull():
                # Wrap to end
                cursor.movePosition(QTextCursor.End)
                found_cursor = self.text_edit.document().find(
                    self.last_find_text, cursor, flags
                )
                
            if not found_cursor.isNull():
                self.text_edit.setTextCursor(found_cursor)
            else:
                QMessageBox.information(self, "Find", f"Cannot find '{self.last_find_text}'")
        else:
            self.show_find_replace()
            
    def replace_current_selection(self, find_text, replace_text, match_case=False):
        cursor = self.text_edit.textCursor()
        selected = cursor.selectedText()
        
        if selected == find_text or (not match_case and selected.lower() == find_text.lower()):
            cursor.insertText(replace_text)
            
        # Find next occurrence
        self.find_text_advanced(find_text, match_case)
        
    def replace_all_text(self, find_text, replace_text, match_case=False):
        if not find_text:
            return 0
            
        content = self.text_edit.toPlainText()
        if match_case:
            count = content.count(find_text)
            new_content = content.replace(find_text, replace_text)
        else:
            count = content.lower().count(find_text.lower())
            # Case-insensitive replace
            import re
            new_content = re.sub(re.escape(find_text), replace_text, content, flags=re.IGNORECASE)
            
        if count > 0:
            self.text_edit.setPlainText(new_content)
            
        return count
        
    def goto_line(self):
        current_line = self.text_edit.textCursor().blockNumber() + 1
        total_lines = self.text_edit.document().blockCount()
        
        line_number, ok = QInputDialog.getInt(
            self, "Go To Line", 
            f"Line number (1-{total_lines}):", 
            current_line, 1, total_lines
        )
        
        if ok:
            cursor = QTextCursor(self.text_edit.document().findBlockByLineNumber(line_number - 1))
            self.text_edit.setTextCursor(cursor)
            
    def insert_time_date(self):
        current_time = datetime.datetime.now()
        time_str = current_time.strftime("%I:%M %p %m/%d/%Y")
        cursor = self.text_edit.textCursor()
        cursor.insertText(time_str)
        
    def toggle_word_wrap(self):
        if self.word_wrap_action.isChecked():
            self.text_edit.setLineWrapMode(QPlainTextEdit.WidgetWidth)
        else:
            self.text_edit.setLineWrapMode(QPlainTextEdit.NoWrap)
            
    def change_font(self):
        current_font = self.text_edit.font()
        font, ok = QFontDialog.getFont(current_font, self)
        if ok:
            self.text_edit.setFont(font)
            
    def zoom_in(self):
        self.zoom_level = min(500, self.zoom_level + 10)
        self.apply_zoom()
        
    def zoom_out(self):
        self.zoom_level = max(10, self.zoom_level - 10)
        self.apply_zoom()
        
    def restore_zoom(self):
        self.zoom_level = 100
        self.apply_zoom()
        
    def apply_zoom(self):
        font = self.text_edit.font()
        base_size = 11
        new_size = int(base_size * self.zoom_level / 100)
        font.setPointSize(new_size)
        self.text_edit.setFont(font)
        self.zoom_label.setText(f"{self.zoom_level}%")
        
    def toggle_status_bar(self):
        if self.status_bar_action.isChecked():
            self.status_bar.show()
        else:
            self.status_bar.hide()
            
    def show_about(self):
        QMessageBox.about(
            self, "About Modern Notepad",
            "Modern Notepad\n\n"
            "A modern, feature-rich text editor built with PyQt5.\n"
            "Includes all standard Notepad features with modern improvements.\n\n"
            "© 2025 Modern Notepad"
        )
        
    def load_settings(self):
        # Load window geometry
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
            
        # Load font
        font_family = self.settings.value("font_family", "Segoe UI")
        font_size = self.settings.value("font_size", 11, type=int)
        font = QFont(font_family, font_size)
        self.text_edit.setFont(font)
        
        # Load word wrap setting
        word_wrap = self.settings.value("word_wrap", True, type=bool)
        self.word_wrap_action.setChecked(word_wrap)
        self.toggle_word_wrap()
        
        # Load status bar setting
        show_status = self.settings.value("show_status_bar", True, type=bool)
        self.status_bar_action.setChecked(show_status)
        self.toggle_status_bar()
        
    def save_settings(self):
        self.settings.setValue("geometry", self.saveGeometry())
        font = self.text_edit.font()
        self.settings.setValue("font_family", font.family())
        self.settings.setValue("font_size", font.pointSize())
        self.settings.setValue("word_wrap", self.word_wrap_action.isChecked())
        self.settings.setValue("show_status_bar", self.status_bar_action.isChecked())
        
    def closeEvent(self, event):
        if self.check_save_changes():
            self.save_settings()
            event.accept()
        else:
            event.ignore()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Modern Notepad")
    app.setOrganizationName("ModernNotepad")
    
    # Set modern application style
    app.setStyle('Fusion')
    
    # Create app icon
    app_icon = ModernIcon.create_icon("new", 32)
    app.setWindowIcon(app_icon)
    
    window = ModernNotepad()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

