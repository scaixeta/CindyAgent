@echo off
REM Wrapper para OpenCode com MINIMAX_API_KEY do .scr\.env
REM Uso: run_opencode.bat "pergunta" [modelo]
REM Exemplo: run_opencode.bat "What is 2+2?" minimax/MiniMax-M2.7

setlocal enabledelayedexpansion

REM Carregar MINIMAX_API_KEY do .scr\.env
for /f "usebackq tokens=1,2 delims==" %%a in ("%~dp0.scr\.env") do (
    if "%%a"=="MINIMAX_API_KEY" set "MINIMAX_API_KEY=%%b"
)

if "%MINIMAX_API_KEY%"=="" (
    echo ERRO: MINIMAX_API_KEY nao encontrada em %~dp0.scr\.env
    exit /b 1
)

set MODEL=%~2
if "%MODEL%"=="" set MODEL=minimax/MiniMax-M2.7

REM Chamar PowerShell para exportar a variavel e correr o opencode no mesmo processo
powershell -NoProfile -Command ^
    "$env:MINIMAX_API_KEY='%MINIMAX_API_KEY%'; opencode run --model %MODEL% %~1"
