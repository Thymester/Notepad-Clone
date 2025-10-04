# File Associations Setup for Notepad Clone

This guide explains how to set up Windows file associations so that .txt and .enc files open automatically with Notepad Clone.

## Prerequisites

1. **Build the executable first**: Run PyInstaller to create `dist\main.exe`
   ```bash
   pyinstaller --onefile --noconsole --icon=icon.ico main.py
   ```

2. **Run as Administrator**: File association scripts require administrator privileges to modify the Windows registry.

## Setup Methods

### Method 1: Batch File (Recommended)

1. Right-click `setup_file_associations.bat`
2. Select "Run as administrator"
3. The script will automatically detect the executable location and set up associations

### Method 2: PowerShell Script

1. Right-click `setup_file_associations.ps1`
2. Select "Run with PowerShell" (as administrator)
3. Or run from PowerShell terminal:
   ```powershell
   .\setup_file_associations.ps1
   ```

### Method 3: Manual Setup

If the scripts don't work, you can manually set associations:

1. **For .txt files:**
   - Right-click any .txt file
   - Select "Open with" → "Choose another app"
   - Click "More apps" → "Look for another app on this PC"
   - Navigate to `dist\main.exe` and select it
   - Check "Always use this app to open .txt files"

2. **For .enc files:**
   - Follow the same steps as above for any .enc file

## What Gets Set Up

The scripts create the following registry entries:

- **Application Registration**: Registers `main.exe` as "Modern Notepad"
- **File Type Associations**:
  - `.txt` files → Text Documents
  - `.enc` files → Encrypted Documents
- **Icons**: Uses the custom notepad icon for all associated files
- **Commands**: Configures the executable to receive file paths as arguments

## Troubleshooting

### Script Fails to Run
- Make sure you're running as Administrator
- Check that `dist\main.exe` exists
- Try the manual method instead

### Files Still Don't Open
- Restart Windows Explorer or log out/in
- Check that the executable path in registry is correct
- Try the manual association method

### Icons Don't Show
- The icon may take time to appear in Windows Explorer
- Restart your computer if icons don't update

## Supported File Types

- **.txt**: Plain text files
- **.enc**: Encrypted files created by Notepad Clone

## Security Note

The file association setup modifies your Windows registry. The scripts only create entries for Notepad Clone and don't modify existing associations unless you explicitly choose to make it the default program.