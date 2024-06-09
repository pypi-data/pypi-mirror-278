@echo off

:: Set line length variable
set LINE_LENGTH=120
set SRC_DIR=src
set SORT_IMPORTS=0

echo Starting to clean and format Python files...

:: Check if isort is installed
where /q isort
if ErrorLevel 1 (
    echo Error: isort is not installed. Please install it first.
    exit /b 1
)

:: Check if black is installed
where /q black
if ErrorLevel 1 (
    echo Error: black is not installed. Please install it first.
    exit /b 1
)

:: Check if autoflake is installed
where /q autoflake
if ErrorLevel 1 (
    echo Error: autoflake is not installed. Please install it first.
    exit /b 1
)

:: Use autoflake to remove unused imports for all .py files within the SRC_DIR directory and its subdirectories
echo Running autoflake...
autoflake --remove-all-unused-imports --in-place --recursive %SRC_DIR%

:: Use isort to sort imports for all .py files within the SRC_DIR directory and its subdirectories
if %SORT_IMPORTS%==1 (
    echo Running isort...
    isort --recursive %SRC_DIR%
)

:: Use black to format all .py files within the SRC_DIR directory and its subdirectories
echo Running black...
black --line-length %LINE_LENGTH% %SRC_DIR%

echo Done.
