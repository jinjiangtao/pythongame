# Build script - Windows PowerShell
# Install dependencies
pip install -r requirements.txt

# Compile to executable
pyinstaller --onefile --name trae-session trae_session.py

Write-Host "`nBuild complete!"
Write-Host "Executable located at: dist\trae-session.exe"
