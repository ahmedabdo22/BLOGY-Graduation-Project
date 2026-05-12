@echo off
title Django Control Panel
color 0A

REM =========================
REM Django Project Path
REM =========================
cd /d C:\Users\it-oss\te\blogy

REM Activate Virtual Environment
call venv\Scripts\activate

:MENU
cls
echo =====================================
echo         DJANGO CONTROL PANEL
echo =====================================
echo.
echo 1 - Run Server
echo 2 - Make Migrations
echo 3 - Migrate
echo 4 - Create Superuser
echo 5 - Collect Static
echo 6 - Open Django Shell
echo 7 - Install Requirements
echo 8 - Exit
echo.
echo =====================================

set /p choice=Enter your choice: 

if "%choice%"=="1" goto RUNSERVER
if "%choice%"=="2" goto MAKEMIGRATIONS
if "%choice%"=="3" goto MIGRATE
if "%choice%"=="4" goto SUPERUSER
if "%choice%"=="5" goto STATIC
if "%choice%"=="6" goto SHELL
if "%choice%"=="7" goto REQUIREMENTS
if "%choice%"=="8" exit

echo Invalid choice!
pause
goto MENU

:RUNSERVER
cls
python manage.py runserver
pause
goto MENU

:MAKEMIGRATIONS
cls
python manage.py makemigrations
pause
goto MENU

:MIGRATE
cls
python manage.py migrate
pause
goto MENU

:SUPERUSER
cls
python manage.py createsuperuser
pause
goto MENU

:STATIC
cls
python manage.py collectstatic --noinput
pause
goto MENU

:SHELL
cls
python manage.py shell
pause
goto MENU

:REQUIREMENTS
cls
pip install -r requirements.txt
pause
goto MENU