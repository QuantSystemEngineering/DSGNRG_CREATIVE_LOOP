@echo off
echo 🔁 DSGNRG Creative Loop Agent Setup
echo =====================================

echo.
echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Setup complete! Here's how to use your Creative Loop Agent:
echo.
echo CLI Usage:
echo   python loop_cli.py status report
echo   python loop_cli.py input sketch 30 "Your sketch description"
echo.
echo Web Dashboard:
echo   python loop_server.py
echo   Then open http://localhost:5000
echo.
echo Press any key to run a status report...
pause > nul

python loop_cli.py status report

echo.
echo Press any key to exit...
pause > nul