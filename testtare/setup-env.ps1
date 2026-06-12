# Environment variable setup script - Windows PowerShell
# Usage: .\setup-env.ps1

# Get the directory where this script is located
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$distPath = Join-Path $scriptPath "dist"

# Check if executable exists
$exePath = Join-Path $distPath "trae-session.exe"
if (-not (Test-Path $exePath)) {
    Write-Host "Error: Cannot find executable file $exePath"
    Write-Host "Please run build.ps1 first to compile"
    exit 1
}

# Get current user's PATH environment variable
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")

# Check if already added
if ($currentPath -notlike "*$distPath*") {
    # Add to PATH
    [Environment]::SetEnvironmentVariable("Path", "$currentPath;$distPath", "User")
    Write-Host "Added $distPath to user PATH environment variable"
    Write-Host "Please restart terminal or re-login for changes to take effect"
} else {
    Write-Host "$distPath is already in PATH environment variable"
}

Write-Host "`nSetup complete!"
Write-Host "You can now use 'trae-session' command from anywhere"
