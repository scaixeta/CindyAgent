@echo off
setlocal

echo [1/4] Reiniciando Hermes Gateway...
wsl -d Ubuntu-22.04 --user root -- bash -lc "pkill -9 -f '/root/.hermes/hermes-agent/venv/bin/hermes gateway' 2>/dev/null || true"

start "Hermes Gateway" wsl -d Ubuntu-22.04 --user root -- /root/.hermes/hermes-agent/venv/bin/hermes gateway run

echo [2/4] Aguardando gateway subir...
timeout /t 5 /nobreak >nul

echo [3/4] Ativando Cindy no runtime Hermes...
python "%~dp0KB\hermes\activate_cindy_runtime.py"
if errorlevel 1 (
  echo Falha ao ativar a Cindy.
  exit /b 1
)

echo [4/4] Status atual do gateway:
wsl -d Ubuntu-22.04 --user root -- /root/.hermes/hermes-agent/venv/bin/hermes gateway status

echo.
echo Hermes iniciado. Cindy ativada.
echo Janela do gateway aberta separadamente.

endlocal
