@echo off
REM Wrapper para Codex CLI com subscription OpenAI
REM Uso: run_codex.bat "pergunta aqui"
REM Autenticacao: codex auth login (browser OAuth)

if "%~1"=="" (
    echo Uso: run_codex.bat "pergunta aqui"
    exit /b 1
)

codex exec %* -s read-only
