# Initialize variables
$venvFolder = ".venv"
$vscodeFolder = ".vscode"
$backupFolder = ".vscode_backup"
$PythonPath = ""  # Set this to the path of the exact Python version you want to use

# Function to roll back changes
function Rollback {
    Write-Host "Error occurred. Rolling back changes..."
    if (Test-Path $backupFolder) {
        Copy-Item -Path "$backupFolder\*" -Destination $vscodeFolder -Recurse -Force
        Remove-Item -Path $backupFolder -Recurse -Force
    }
    if (Test-Path $venvFolder) {
        Remove-Item -Path $venvFolder -Recurse -Force
    }
    exit 1
}

# Verify that the specified Python path exists and is executable
if (-Not (Test-Path $PythonPath)) {
    Write-Host "Specified Python path does not exist: $PythonPath"
    exit 1
}

# Check the Python version
function ExtractPythonVersion($versionString) {
    return $versionString -replace "Python ", ""
}

$versionOutput = & $PythonPath --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to execute Python at $PythonPath"
    exit 1
}

$pythonVersion = ExtractPythonVersion $versionOutput
Write-Host "Using Python installation: $PythonPath with version $pythonVersion"

# Create a virtual environment
& $PythonPath -m venv $venvFolder
if ($LASTEXITCODE -ne 0) { Rollback }

# Activate the virtual environment
& .\$venvFolder\Scripts\Activate
if ($LASTEXITCODE -ne 0) { Rollback }

# Backup existing .vscode folder, if it exists
if (Test-Path $vscodeFolder) {
    Copy-Item -Path $vscodeFolder -Destination $backupFolder -Recurse -Force
}

# Create .vscode directory and JSON files
New-Item -Path $vscodeFolder -ItemType Directory -Force
@'
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File (myenv)",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "env": {
                "PYDEVD_DISABLE_FILE_VALIDATION": "1",
                "PYDEVD_WARN_SLOW_RESOLVE_TIMEOUT": "60",
                "PYDEVD_WARN_SLOW_EVALUATION_TIMEOUT": "60"
            },
            "justMyCode": false
        }
    ]
}
'@ | Set-Content -Path "$vscodeFolder\launch.json"

@'
{
    "python.testing.unittestArgs": [
        "-v",
        "-s",
        "./tests",
        "-p",
        "*_test.py"
    ],
    "python.testing.pytestEnabled": false,
    "python.testing.unittestEnabled": true,
    "python.analysis.typeCheckingMode": "off",
    "python.terminal.activateEnvironment": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    },
    "[python]": {
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "ms-python.black-formatter"
    }
}
'@ | Set-Content -Path "$vscodeFolder\settings.json"

# # Install packages
# pip install -r .\requirements.txt 
# if ($LASTEXITCODE -ne 0) { Rollback }

# pip install -r .\requirements-dev.txt
# if ($LASTEXITCODE -ne 0) { Rollback }

# If we reach this point, everything was successful; remove the backup
if (Test-Path $backupFolder) {
    Remove-Item -Path $backupFolder -Recurse -Force
}

Write-Host "Setup completed successfully."
