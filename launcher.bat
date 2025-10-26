@echo off
cls
echo.
echo 🔁 DSGNRG CREATIVE LOOP LAUNCHER
echo ================================
echo.
echo Choose your interface:
echo.
echo [1] 📊 Web Dashboard (Recommended)
echo [2] 💻 Command Line Interface  
echo [3] 📈 Quick Status Report
echo [4] ➕ Log Daily Inputs
echo [5] 🔧 Setup/Install Dependencies
echo [0] Exit
echo.
set /p choice="Enter your choice (0-5): "

if "%choice%"=="1" goto dashboard
if "%choice%"=="2" goto cli
if "%choice%"=="3" goto report
if "%choice%"=="4" goto inputs
if "%choice%"=="5" goto setup
if "%choice%"=="0" goto exit
goto invalid

:dashboard
echo.
echo 🚀 Starting web dashboard...
echo Open http://localhost:5000 in your browser
echo Press Ctrl+C to stop the server
echo.
python loop_server.py
goto end

:cli
echo.
echo 💻 Command Line Interface
echo Type 'python loop_cli.py --help' for all commands
echo.
cmd /k "cd /d %~dp0"
goto end

:report
echo.
python loop_cli.py status report
echo.
pause
goto end

:inputs
echo.
echo ➕ Quick Input Logging
echo.
echo [1] 🎵 Sonic Sketch
echo [2] 🖼️ Visual Moodboard  
echo [3] 📖 Lore Fragment
echo.
set /p input_choice="Choose input type (1-3): "

if "%input_choice%"=="1" goto sketch
if "%input_choice%"=="2" goto visual
if "%input_choice%"=="3" goto lore
goto inputs

:sketch
set /p duration="Duration in minutes (default 30): "
if "%duration%"=="" set duration=30
set /p description="Sketch description: "
python loop_cli.py input sketch %duration% "%description%"
echo.
pause
goto end

:visual
set /p theme="Visual theme: "
echo Enter image files (space-separated):
set /p images="Images: "
python loop_cli.py input visual "%theme%" --images %images%
echo.
pause
goto end

:lore
set /p character="Character name: "
set /p fragment="Lore fragment: "
set /p arc="Narrative arc: "
python loop_cli.py input lore "%character%" "%fragment%" "%arc%"
echo.
pause
goto end

:setup
echo.
echo 🔧 Running setup...
call setup.bat
goto end

:invalid
echo.
echo ❌ Invalid choice. Please enter 0-5.
echo.
pause
goto end

:exit
echo.
echo 👋 Keep the creative loop flowing!
exit /b 0

:end
echo.
echo Press any key to return to launcher...
pause > nul
cls

:menu
echo.
echo 🔁 DSGNRG CREATIVE LOOP LAUNCHER
echo ================================
echo.
echo Choose your interface:
echo.
echo [1] 📊 Web Dashboard (Recommended)
echo [2] 💻 Command Line Interface  
echo [3] 📈 Quick Status Report
echo [4] ➕ Log Daily Inputs
echo [5] 🔧 Setup/Install Dependencies
echo [0] Exit
echo.
set /p choice="Enter your choice (0-5): "

if "%choice%"=="1" goto dashboard
if "%choice%"=="2" goto cli
if "%choice%"=="3" goto report
if "%choice%"=="4" goto inputs
if "%choice%"=="5" goto setup
if "%choice%"=="0" goto exit
goto invalid