@echo off

rem Define the URL for the get-pip.py script
set PIP_INSTALLER_URL=https://bootstrap.pypa.io/get-pip.py

rem Check if pip is already installed
python -m pip --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Pip is already installed.
    pause
    exit /b 0
)

rem Download get-pip.py
echo Downloading get-pip.py...
curl -o get-pip.py %PIP_INSTALLER_URL%
if %errorlevel% neq 0 (
    echo Failed to download get-pip.py. Please check your internet connection or download it manually.
    pause
    exit /b 1
)

rem Install pip
echo Installing pip...
python get-pip.py
if %errorlevel% neq 0 (
    echo Pip installation failed. Please check your Python installation and try again.
    pause
    exit /b 1
)

rem Clean up the temporary installation script
del get-pip.py

echo Pip installed successfully!