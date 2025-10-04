# Setup file associations for Notepad Clone
# This script sets up .txt and .enc files to open with Notepad Clone

param(
    [string]$ExePath = ""
)

Write-Host "Setting up file associations for Notepad Clone..." -ForegroundColor Green
Write-Host ""

# Get the current directory if not specified
if (-not $ExePath) {
    $currentDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    $ExePath = Join-Path $currentDir "dist\main.exe"
}

# Check if the executable exists
if (-not (Test-Path $ExePath)) {
    Write-Host "ERROR: main.exe not found at $ExePath" -ForegroundColor Red
    Write-Host "Please make sure you have built the executable first." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Found executable: $ExePath" -ForegroundColor Yellow
Write-Host ""

# Register the application
New-Item -Path "HKCR:\Applications\main.exe" -Force | Out-Null
Set-ItemProperty -Path "HKCR:\Applications\main.exe" -Name "" -Value "Modern Notepad"
New-Item -Path "HKCR:\Applications\main.exe\DefaultIcon" -Force | Out-Null
Set-ItemProperty -Path "HKCR:\Applications\main.exe\DefaultIcon" -Name "" -Value "`"$ExePath`",0"
New-Item -Path "HKCR:\Applications\main.exe\shell\open\command" -Force | Out-Null
Set-ItemProperty -Path "HKCR:\Applications\main.exe\shell\open\command" -Name "" -Value "`"$ExePath`" `"%1`""

# Associate .txt files
Set-ItemProperty -Path "HKCR:\.txt" -Name "" -Value "ModernNotepad.txt"
New-Item -Path "HKCR:\ModernNotepad.txt" -Force | Out-Null
Set-ItemProperty -Path "HKCR:\ModernNotepad.txt" -Name "" -Value "Text Document"
New-Item -Path "HKCR:\ModernNotepad.txt\DefaultIcon" -Force | Out-Null
Set-ItemProperty -Path "HKCR:\ModernNotepad.txt\DefaultIcon" -Name "" -Value "`"$ExePath`",0"
New-Item -Path "HKCR:\ModernNotepad.txt\shell\open\command" -Force | Out-Null
Set-ItemProperty -Path "HKCR:\ModernNotepad.txt\shell\open\command" -Name "" -Value "`"$ExePath`" `"%1`""

# Associate .enc files (encrypted files)
Set-ItemProperty -Path "HKCR:\.enc" -Name "" -Value "ModernNotepad.enc"
New-Item -Path "HKCR:\ModernNotepad.enc" -Force | Out-Null
Set-ItemProperty -Path "HKCR:\ModernNotepad.enc" -Name "" -Value "Encrypted Document"
New-Item -Path "HKCR:\ModernNotepad.enc\DefaultIcon" -Force | Out-Null
Set-ItemProperty -Path "HKCR:\ModernNotepad.enc\DefaultIcon" -Name "" -Value "`"$ExePath`",0"
New-Item -Path "HKCR:\ModernNotepad.enc\shell\open\command" -Force | Out-Null
Set-ItemProperty -Path "HKCR:\ModernNotepad.enc\shell\open\command" -Name "" -Value "`"$ExePath`" `"%1`""

Write-Host ""
Write-Host "File associations have been set up successfully!" -ForegroundColor Green
Write-Host ""
Write-Host ".txt files will now open with Notepad Clone" -ForegroundColor Cyan
Write-Host ".enc files will now open with Notepad Clone" -ForegroundColor Cyan
Write-Host ""
Write-Host "To set as default program:" -ForegroundColor Yellow
Write-Host "1. Right-click any .txt or .enc file" -ForegroundColor White
Write-Host "2. Select 'Open with' -> 'Choose another app'" -ForegroundColor White
Write-Host "3. Select 'Modern Notepad' from the list" -ForegroundColor White
Write-Host "4. Check 'Always use this app to open .txt/.enc files'" -ForegroundColor White
Write-Host ""
Read-Host "Press Enter to exit"