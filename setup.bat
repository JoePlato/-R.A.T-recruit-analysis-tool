@echo off
:: Check for Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Downloading Python 3.12.1...
    curl -o python-3.12.1.exe https://www.python.org/ftp/python/3.12.1/python-3.12.1-amd64.exe
    if %errorlevel% neq 0 (
        echo Failed to download Python installer. Ensure curl is installed.
        pause
        exit /b 1
    )
    echo Installing Python 3.12.1...
    start /wait python-3.12.1.exe /quiet InstallAllUsers=1 PrependPath=1
    if %errorlevel% neq 0 (
        echo Python installation failed. Please check the installer and try again.
        pause
        exit /b 1
    )
    echo Python installed successfully.
)

:: Verify Python version
python --version | find "3.12.1" >nul
if %errorlevel% neq 0 (
    echo Python 3.12.1 is not installed or not correctly set up. Please install it manually.
    pause
    exit /b 1
)

:: Check if the virtual environment already exists
if not exist env (
    echo Creating virtual environment...
    python -m venv env
    if %errorlevel% neq 0 (
        echo Failed to create virtual environment. Ensure Python is properly installed and added to PATH.
        pause
        exit /b 1
    )
)

:: Activate the virtual environment
echo Activating virtual environment...
call env\Scripts\activate

:: Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install dependencies. Check your requirements.txt file.
    pause
    exit /b 1
)

:: Start the Python server
echo Starting Python server...
start /b python server.py
if %errorlevel% neq 0 (
    echo Failed to start Python server. Ensure server.py is configured correctly.
    pause
    exit /b 1
)

:: Wait for the server to start (optional, tweak delay as needed)
timeout /t 2 >nul

:: Open the web app in the default browser
echo Launching web app...
start http://127.0.0.1:5000

:: Keep the script running (optional, in case you want to monitor)
echo Application is running. Press Ctrl+C to exit.
pause
