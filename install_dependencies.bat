@echo off
echo Installing dependencies for BLAKE3 File Hash Renaming Tool...

:: Check admin privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Please run this script as Administrator!
    echo Right-click on the script and select "Run as administrator".
    pause
    exit /b 1
)

:: Check Python installation
where python >nul 2>&1
if %errorLevel% neq 0 (
    echo Python not found! Please install Python 3.6 or later.
    echo You can download Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Install required dependencies
echo Installing necessary Python packages...
python -m pip install --upgrade pip
python -m pip install blake3

echo.
echo Dependencies installed successfully!
echo Please double-click "start_tool.bat" to start the program and register context menu.
echo.
pause
