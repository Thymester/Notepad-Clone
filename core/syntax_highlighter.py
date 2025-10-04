from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor
from PyQt5.QtCore import QRegExp


class SyntaxHighlighter(QSyntaxHighlighter):
    """
    Syntax highlighter for various programming languages.
    """

    def __init__(self, parent=None, language="python"):
        super().__init__(parent)
        self.language = language
        self.highlighting_rules = []

        self.setup_highlighting_rules()

    def setup_highlighting_rules(self):
        """Setup highlighting rules based on language."""
        if self.language.lower() == "python":
            self.setup_python_highlighting()
        elif self.language.lower() == "javascript":
            self.setup_javascript_highlighting()
        elif self.language.lower() == "cpp":
            self.setup_cpp_highlighting()
        else:
            # Plain text - no highlighting
            self.highlighting_rules = []

    def setup_python_highlighting(self):
        """Setup Python syntax highlighting rules."""
        self.highlighting_rules = []

        # Keywords
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#0000FF"))  # Blue
        keyword_format.setFontWeight(QFont.Bold)
        keywords = [
            "and", "as", "assert", "break", "class", "continue", "def",
            "del", "elif", "else", "except", "False", "finally", "for",
            "from", "global", "if", "import", "in", "is", "lambda", "None",
            "nonlocal", "not", "or", "pass", "raise", "return", "True",
            "try", "while", "with", "yield"
        ]
        for keyword in keywords:
            pattern = QRegExp(r'\b' + keyword + r'\b')
            self.highlighting_rules.append((pattern, keyword_format))

        # Strings
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#008000"))  # Green
        self.highlighting_rules.append((QRegExp(r'".*"'), string_format))
        self.highlighting_rules.append((QRegExp(r"'.*'"), string_format))

        # Comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#808080"))  # Gray
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((QRegExp(r'#.*'), comment_format))

        # Functions
        function_format = QTextCharFormat()
        function_format.setForeground(QColor("#800080"))  # Purple
        function_format.setFontWeight(QFont.Bold)
        self.highlighting_rules.append((QRegExp(r'\bdef\s+(\w+)'), function_format))

        # Classes
        class_format = QTextCharFormat()
        class_format.setForeground(QColor("#FF8000"))  # Orange
        class_format.setFontWeight(QFont.Bold)
        self.highlighting_rules.append((QRegExp(r'\bclass\s+(\w+)'), class_format))

    def setup_javascript_highlighting(self):
        """Setup JavaScript syntax highlighting rules."""
        self.highlighting_rules = []

        # Keywords
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#0000FF"))  # Blue
        keyword_format.setFontWeight(QFont.Bold)
        keywords = [
            "break", "case", "catch", "class", "const", "continue", "debugger",
            "default", "delete", "do", "else", "export", "extends", "false",
            "finally", "for", "function", "if", "import", "in", "instanceof",
            "let", "new", "null", "return", "super", "switch", "this", "throw",
            "true", "try", "typeof", "var", "void", "while", "with", "yield"
        ]
        for keyword in keywords:
            pattern = QRegExp(r'\b' + keyword + r'\b')
            self.highlighting_rules.append((pattern, keyword_format))

        # Strings
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#008000"))  # Green
        self.highlighting_rules.append((QRegExp(r'".*"'), string_format))
        self.highlighting_rules.append((QRegExp(r"'.*'"), string_format))

        # Comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#808080"))  # Gray
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((QRegExp(r'//.*'), comment_format))
        self.highlighting_rules.append((QRegExp(r'/\*.*\*/'), comment_format))

        # Functions
        function_format = QTextCharFormat()
        function_format.setForeground(QColor("#800080"))  # Purple
        function_format.setFontWeight(QFont.Bold)
        self.highlighting_rules.append((QRegExp(r'\bfunction\s+(\w+)'), function_format))

    def setup_cpp_highlighting(self):
        """Setup C++ syntax highlighting rules."""
        self.highlighting_rules = []

        # Keywords
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#0000FF"))  # Blue
        keyword_format.setFontWeight(QFont.Bold)
        keywords = [
            "alignas", "alignof", "and", "and_eq", "asm", "auto", "bitand",
            "bitor", "bool", "break", "case", "catch", "char", "char16_t",
            "char32_t", "class", "compl", "const", "constexpr", "const_cast",
            "continue", "decltype", "default", "delete", "do", "double",
            "dynamic_cast", "else", "enum", "explicit", "export", "extern",
            "false", "float", "for", "friend", "goto", "if", "inline", "int",
            "long", "mutable", "namespace", "new", "noexcept", "not", "not_eq",
            "nullptr", "operator", "or", "or_eq", "private", "protected",
            "public", "register", "reinterpret_cast", "return", "short",
            "signed", "sizeof", "static", "static_assert", "static_cast",
            "struct", "switch", "template", "this", "thread_local", "throw",
            "true", "try", "typedef", "typeid", "typename", "union", "unsigned",
            "using", "virtual", "void", "volatile", "wchar_t", "while", "xor", "xor_eq"
        ]
        for keyword in keywords:
            pattern = QRegExp(r'\b' + keyword + r'\b')
            self.highlighting_rules.append((pattern, keyword_format))

        # Strings
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#008000"))  # Green
        self.highlighting_rules.append((QRegExp(r'".*"'), string_format))
        self.highlighting_rules.append((QRegExp(r"'.*'"), string_format))

        # Comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#808080"))  # Gray
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((QRegExp(r'//.*'), comment_format))
        self.highlighting_rules.append((QRegExp(r'/\*.*\*/'), comment_format))

        # Preprocessor
        preprocessor_format = QTextCharFormat()
        preprocessor_format.setForeground(QColor("#FF0000"))  # Red
        self.highlighting_rules.append((QRegExp(r'#.*'), preprocessor_format))

    def highlightBlock(self, text):
        """Apply highlighting to a block of text."""
        for pattern, format in self.highlighting_rules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

    def set_language(self, language):
        """Change the highlighting language."""
        self.language = language
        self.setup_highlighting_rules()
        self.rehighlight()