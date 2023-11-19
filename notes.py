import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QAction, QFileDialog, QMessageBox, QInputDialog
from PyQt5.QtGui import QIcon, QKeySequence, QTextCursor, QTextCharFormat
from PyQt5.QtCore import Qt
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from langdetect import detect
import autopep8
import subprocess

class NotepadApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.current_file_path = ""

        self.init_ui()
        self.create_menus()
    
    def execute_code(self):
        text = self.text_edit.toPlainText()

        if not text:
            return

        try:
            process = subprocess.Popen(["python", "-c", text], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            output = stdout + stderr

            if output:
                self.show_output(output)
        except Exception as e:
            self.show_output(str(e))

    def show_output(self, output):
        QMessageBox.information(self, "Code Execution Result", output)

    def highlight_text(self):
        print("Highlight method triggered")
        cursor = self.text_edit.textCursor()
        selected_text = cursor.selectedText()

        if selected_text:
            detected_language = self.detect_language(selected_text)
            lexer = self.get_lexer_by_name(detected_language)
            formatter = HtmlFormatter()

            highlighted_code = highlight(selected_text, lexer, formatter)

            format = QTextCharFormat()
            format.setForeground(Qt.black)

    def auto_indent(self):
        cursor = self.text_edit.textCursor()
        selected_text = cursor.selectedText()

        if selected_text:
            detected_language = self.detect_language(selected_text)
            if detected_language == 'python':
                formatted_code = autopep8.fix_code(selected_text, options={'indent_size': 4})
                cursor.removeSelectedText()
                cursor.insertText(formatted_code)

    def get_lexer_by_name(self, lang_name):
        try:
            lexer = get_lexer_by_name(lang_name)
        except:
            lexer = get_lexer_by_name('python')
        return lexer

    def init_ui(self):
        self.setWindowTitle("Notepad")
        self.setGeometry(100, 100, 800, 600)

        self.text_edit = QPlainTextEdit(self)
        self.setCentralWidget(self.text_edit)

        self.font = self.text_edit.font()
        self.font.setPointSize(12)
        self.text_edit.setFont(self.font)

        self.language_colors = {
            'python': Qt.darkBlue,
            'java': Qt.darkRed,
            'c': Qt.darkGreen,
            'c++': Qt.darkMagenta,
            'c#': Qt.darkYellow,
            'javascript': Qt.darkCyan,
            'php': Qt.darkGray,
            'ruby': Qt.darkBlue,
            'go': Qt.darkRed,
            'swift': Qt.darkGreen,
            'kotlin': Qt.darkMagenta,
            'rust': Qt.darkYellow,
            'scala': Qt.darkCyan,
            'haskell': Qt.darkGray,
            'r': Qt.darkBlue,
            'dart': Qt.darkRed,
            'typescript': Qt.darkGreen,
            'elixir': Qt.darkMagenta,
            'clojure': Qt.darkYellow,
            'julia': Qt.darkCyan,
            'perl': Qt.darkGray,
            'lua': Qt.darkBlue,
            'crystal': Qt.darkRed,
            'ocaml': Qt.darkGreen,
            'erlang': Qt.darkMagenta,
            'bash': Qt.darkYellow,
            'powershell': Qt.darkCyan,
            'plaintext': Qt.darkGray
        }

    def create_menus(self):
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")

        new_action = QAction(QIcon(), "New", self)
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        open_action = QAction(QIcon(), "Open", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction(QIcon(), "Save", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        exit_action = QAction(QIcon(), "Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit menu
        edit_menu = menubar.addMenu("Edit")

        undo_action = QAction("Undo", self)
        undo_action.setShortcut(QKeySequence.Undo)
        undo_action.triggered.connect(self.text_edit.undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction("Redo", self)
        redo_action.setShortcut(QKeySequence.Redo)
        redo_action.triggered.connect(self.text_edit.redo)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        run_code_action = QAction("Run Code", self)
        run_code_action.setShortcut(QKeySequence("Ctrl+R"))
        run_code_action.triggered.connect(self.execute_code)
        edit_menu.addAction(run_code_action)

        edit_menu.addSeparator()

        cut_action = QAction("Cut", self)
        cut_action.setShortcut(QKeySequence.Cut)
        cut_action.triggered.connect(self.text_edit.cut)
        edit_menu.addAction(cut_action)

        copy_action = QAction("Copy", self)
        copy_action.setShortcut(QKeySequence.Copy)
        copy_action.triggered.connect(self.text_edit.copy)
        edit_menu.addAction(copy_action)

        paste_action = QAction("Paste", self)
        paste_action.setShortcut(QKeySequence.Paste)
        paste_action.triggered.connect(self.text_edit.paste)
        edit_menu.addAction(paste_action)

        select_all_action = QAction("Select All", self)
        select_all_action.setShortcut(QKeySequence.SelectAll)
        select_all_action.triggered.connect(self.text_edit.selectAll)
        edit_menu.addAction(select_all_action)

        edit_menu.addSeparator()

        find_action = QAction("Find", self)
        find_action.setShortcut(QKeySequence.Find)
        find_action.triggered.connect(self.find_text)
        edit_menu.addAction(find_action)

        goto_line_action = QAction("Go to Line", self)
        goto_line_action.triggered.connect(self.goto_line)
        edit_menu.addAction(goto_line_action)

        highlight_action = QAction("Highlight", self)
        highlight_action.setShortcut(QKeySequence("Ctrl+H"))
        highlight_action.triggered.connect(self.highlight_text)
        edit_menu.addAction(highlight_action)

    def new_file(self):
        self.text_edit.clear()
        self.current_file_path = ""
        self.update_title()  # Update the title when creating a new file

    def save_file(self):
        text = self.text_edit.toPlainText()
        if self.current_file_path:
            with open(self.current_file_path, 'w') as file:
                file.write(text)
            QMessageBox.information(self, "Info", "File saved successfully.")
        else:
            self.current_file_path, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'Text files (*.txt)')
            if self.current_file_path:
                with open(self.current_file_path, 'w') as file:
                    file.write(text)
                QMessageBox.information(self, "Info", "File saved successfully.")
                self.update_title()  # Update the title after saving

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Text files (*.txt)')
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_edit.setPlainText(content)
                self.current_file_path = file_path
                self.update_title()  # Update the title after opening

    def update_title(self):
        file_name = "Untitled" if not self.current_file_path else self.current_file_path.split('/')[-1]
        self.setWindowTitle(f"{file_name} - Notepad")

    def zoom_in(self):
        self.text_edit.zoomIn(1)

    def zoom_out(self):
        self.text_edit.zoomOut(1)

    def toggle_word_wrap(self):
        self.text_edit.setLineWrapMode(QPlainTextEdit.WidgetWidth if self.word_wrap_action.isChecked() else QPlainTextEdit.NoWrap)

    def find_text(self):
        search_text, ok = QInputDialog.getText(self, "Find Text", "Enter text to find:")
        if ok and search_text:
            cursor = self.text_edit.document().find(search_text)
            if not cursor.isNull():
                self.text_edit.setTextCursor(cursor)
            else:
                QMessageBox.information(self, "Info", "Text not found.")

    def goto_line(self):
        line_number, ok = QInputDialog.getInt(self, "Go to Line", "Enter line number:", 1, 1)
        if ok:
            cursor = QTextCursor(self.text_edit.document().findBlockByLineNumber(line_number - 1))
            self.text_edit.setTextCursor(cursor)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NotepadApp()
    window.show()
    sys.exit(app.exec_())
