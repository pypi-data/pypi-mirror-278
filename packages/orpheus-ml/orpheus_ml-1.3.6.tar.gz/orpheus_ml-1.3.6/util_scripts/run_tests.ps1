# Initialize function for rollback in case of errors


# testconfigurations:
#------------------------------------------------------------
$filePath = "tests\config\test_configurations.py"
$nTrials = 4

# boolean: 1 = enable logging and disable console output, 0 = disable logging and enable console output
$enableLoggingAndDisableConsoleOutput = 0
$logFileDir = "logs\tests"


#------------------------------------------------------------

function Rollback {
    Write-Host "An error occurred. Rolling back changes..."
    # Add your rollback logic here, if needed.
    exit 1
}

$env:N_TRIALS = $nTrials
$env:LOG_FILE_DIR = $logFileDir
$env:ENABLE_LOGGING_AND_DISABLE_CONSOLE_OUTPUT = $enableLoggingAndDisableConsoleOutput


# Check if the file exists
if (-Not (Test-Path $filePath)) {
    Write-Host "File $filePath not found."
    Rollback
}

# Run Python tests
try {
    py tests\run_tests.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Tests failed!"
        Rollback
    }
}
catch {
    Write-Host "An error occurred while running the tests!"
    Rollback
}

Write-Host "All tests completed successfully."
