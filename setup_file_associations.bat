@echo off
REM Setup file associations for Notepad Clone
REM This script sets up .txt and .enc files to open with Notepad Clone

echo Setting up file associations for Notepad Clone...
echo.

REM Get the current directory (where the executable should be)
set "APP_DIR=%~dp0"
set "EXE_PATH=%APP_DIR%dist\main.exe"

REM Check if the executable exists
if not exist "%EXE_PATH%" (
    echo ERROR: main.exe not found in %APP_DIR%dist\
    echo Please make sure you have built the executable first.
    pause
    exit /b 1
)

echo Found executable: %EXE_PATH%
echo.

REM Register the application
reg add "HKCR\Applications\main.exe" /v "" /d "Modern Notepad" /f
reg add "HKCR\Applications\main.exe\DefaultIcon" /v "" /d "\"%EXE_PATH%\",0" /f
reg add "HKCR\Applications\main.exe\shell\open\command" /v "" /d "\"%EXE_PATH%\" \"%%1\"" /f

REM Associate .txt files
reg add "HKCR\.txt" /v "" /d "ModernNotepad.txt" /f
reg add "HKCR\ModernNotepad.txt" /v "" /d "Text Document" /f
reg add "HKCR\ModernNotepad.txt\DefaultIcon" /v "" /d "\"%EXE_PATH%\",0" /f
reg add "HKCR\ModernNotepad.txt\shell\open\command" /v "" /d "\"%EXE_PATH%\" \"%%1\"" /f

REM Associate .enc files (encrypted files)
reg add "HKCR\.enc" /v "" /d "ModernNotepad.enc" /f
reg add "HKCR\ModernNotepad.enc" /v "" /d "Encrypted Document" /f
reg add "HKCR\ModernNotepad.enc\DefaultIcon" /v "" /d "\"%EXE_PATH%\",0" /f
reg add "HKCR\ModernNotepad.enc\shell\open\command" /v "" /d "\"%EXE_PATH%\" \"%%1\"" /f

echo.
echo File associations have been set up successfully!
echo.
echo .txt files will now open with Notepad Clone
echo .enc files will now open with Notepad Clone
echo.
echo To set as default program:
echo 1. Right-click any .txt or .enc file
echo 2. Select "Open with" -> "Choose another app"
echo 3. Select "Modern Notepad" from the list
echo 4. Check "Always use this app to open .txt/.enc files"
echo.
pause