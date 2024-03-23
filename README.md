# Notepad Application Overview

This is a simple Notepad application developed using Python and PyQt5. It provides basic text editing functionalities along with additional features like syntax highlighting, code execution, and auto-indentation for Python code.

## Features

1. **Text Editing:**
   - Create new files.
   - Open existing text files.
   - Save files.
   - Basic editing operations like cut, copy, paste, undo, redo, select all, find, and go to line.

2. **Syntax Highlighting:**
   - Automatically detects the programming language and highlights the syntax accordingly using Pygments library.

3. **Code Execution:**
   - Execute Python code directly within the application and view the output.

4. **Auto-Indentation:**
   - Automatically formats selected Python code with proper indentation using autopep8 library.

5. **User Interface:**
   - Clean and simple user interface.
   - Customizable font size.
   - Dark-themed syntax highlighting for various programming languages.

## Usage

1. **File Operations:**
   - Create new files: Click on `File > New`.
   - Open existing files: Click on `File > Open`.
   - Save files: Click on `File > Save`.
   - Exit the application: Click on `File > Exit`.

2. **Editing Operations:**
   - Undo: `Ctrl + Z` or `Edit > Undo`.
   - Redo: `Ctrl + Y` or `Edit > Redo`.
   - Cut: `Ctrl + X` or `Edit > Cut`.
   - Copy: `Ctrl + C` or `Edit > Copy`.
   - Paste: `Ctrl + V` or `Edit > Paste`.
   - Select All: `Ctrl + A` or `Edit > Select All`.
   - Find: `Ctrl + F` or `Edit > Find`.
   - Go to Line: `Edit > Go to Line`.

3. **Code Execution:**
   - Run Python code: `Ctrl + R` or `Edit > Run Code`.

4. **Syntax Highlighting:**
   - Highlight selected code: `Ctrl + H` or `Edit > Highlight`.

## How to Run

1. Ensure you have Python installed on your system.
2. Install required dependencies.
3. Run the application.

## Dependencies

- PyQt5: Python bindings for the Qt application framework.
- Pygments: Syntax highlighting library.
- Langdetect: Language detection library.
- Autopep8: Automatic Python code formatter.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the Apache License 2.0. See the LICENSE file for details.
