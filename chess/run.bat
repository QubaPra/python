@echo off
:title
cls
echo Szachy i skaner pozycji - Jakub Prazuch
echo.
echo 1. Gra w szachy
echo 2. Gra w szachy vs SI
echo 3. AI skan pozycji
echo.
choice /c 123 /n /m "Wybierz opcje (1-3): "

if errorlevel 3 goto option3
if errorlevel 2 goto option2
if errorlevel 1 goto option1

:option1
cd code
start main.py
goto title

:option2
cd code
start main_ai_w.py
goto title

:option3
cd code
start fen.py
goto title

:end
