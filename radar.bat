@echo off
chcp 65001 > nul
setlocal

:: Verifica se está no diretório correto
cd /d "%~dp0"

:: Ativa ambiente virtual
if exist guruenv\Scripts\activate.bat (
    call guruenv\Scripts\activate.bat
) else (
    echo Configurando ambiente...
    python -m venv guruenv
    call guruenv\Scripts\activate.bat
    pip install -r requirements.txt
)

:: Roda o RADAR
python main.py

:: Mantém janela aberta em caso de erro
if errorlevel 1 pause

endlocal 