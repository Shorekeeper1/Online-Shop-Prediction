@echo off
setlocal
cd /d "%~dp0" || exit /b 1

if not exist ".venv\Scripts\python.exe" (
    echo Creating the Python environment...
    python -m venv .venv
    if errorlevel 1 goto setup_failed
)

".venv\Scripts\python.exe" -c "import pandas, requests, streamlit" >nul 2>&1
if errorlevel 1 (
    echo Installing the Streamlit dependencies...
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt
    if errorlevel 1 goto setup_failed
)

echo Open http://localhost:8501 if your browser does not open automatically.
".venv\Scripts\python.exe" -m streamlit run app.py --server.address 127.0.0.1 --browser.gatherUsageStats false
if errorlevel 1 goto launch_failed
exit /b 0

:setup_failed
echo Setup failed. Check the error above. A Python installation and internet access are needed for the first run.
pause
exit /b 1

:launch_failed
echo Streamlit could not start. Check the error above.
pause
exit /b 1
