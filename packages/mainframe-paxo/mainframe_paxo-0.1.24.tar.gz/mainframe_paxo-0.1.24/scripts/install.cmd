@echo off
rem this is to set up the essential pre-requisites for for paxo: scop, python and pipx
rem we first install rye, which is a self-containeed python manager.  It will install python
rem for us.  please see https://rye-up.com/
rem
rem this file should be accessible in g: drive, so that it can be run from the command prompt
rem along with the rye installer.
rem put it in G:\Shared drives\Software\paxo

rem set the console title
title paxo initial setup
echo Welcome to paxo initial setup

setlocal
set batfile=%~dp0
set rye=%batfile%rye-x86_64-windows.exe

rem check if rye is installed
rye --version
if %errorlevel% equ 0 (
    echo rye is already installed
    goto :rye-installed
)

rem install it
rem set RYE_INSTALL_OPTION=--yes
call "%rye%" self install --yes

rem add rye to the path
set PATH=%USERPROFILE%\.rye\shims;%PATH%

:rye-installed
rem auto-update
call rye self update 

echo install paxo
rem force install, which will get the latest version even if already installed
call rye tools install -f mainframe-paxo
if %errorlevel% neq 0 (
    echo paxo installation failed
    goto :finish
)

goto :finish

:finish
if %errorlevel% neq 0 (
    echo paxo initial install failed
    pause
    exit /b %errorlevel%
)
echo paxo initial install succeeded
echo if you want to use paxo, you need to open a new console window
echo and run the 'paxo' command.
echo 'paxo initial-setup' will continue the setup of your machine.
pause
exit /b 0
