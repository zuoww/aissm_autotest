@echo off
if "%1"=="start" (
	if "%2"=="" (
		%~dp0\RunWeb.exe %~dp0
	) else (
		%~dp0\RunWeb.exe %~dp0 "web"
	)
)
if "%1"=="restart" (
	ping -n 5 127.1>nul
	%~dp0\RunWeb.exe %~dp0)
if "%1"=="" (%~dp0\TestServer.exe %~dp0)
pause