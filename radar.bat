@echo off
chcp 65001 > nul
setlocal EnableDelayedExpansion

:: Verifica se está no diretório correto
cd /d "%~dp0"

echo Iniciando RADAR...
echo.

:: Verifica Python
python --version > nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python não encontrado! Instale Python 3.9 ou superior.
    pause
    exit /b 1
)

:: Verifica se requirements.txt existe
if not exist requirements.txt (
    echo [ERRO] Arquivo requirements.txt não encontrado!
    pause
    exit /b 1
)

:: Ativa ambiente virtual
if exist guruenv\Scripts\activate.bat (
    echo Ativando ambiente virtual...
    call guruenv\Scripts\activate.bat
) else (
    echo Configurando novo ambiente...
    python -m venv guruenv
    if errorlevel 1 (
        echo [ERRO] Falha ao criar ambiente virtual!
        pause
        exit /b 1
    )
    call guruenv\Scripts\activate.bat
    echo Instalando dependências...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERRO] Falha ao instalar dependências!
        pause
        exit /b 1
    )
)

:: Verifica se main.py existe
if not exist main.py (
    echo [ERRO] Arquivo main.py não encontrado!
    pause
    exit /b 1
)

:: Roda o RADAR
echo.
echo Iniciando análise...
echo.
python main.py
if errorlevel 1 (
    echo.
    echo [ERRO] O RADAR encontrou um problema!
    echo Para mais detalhes, verifique a mensagem acima.
    pause
    exit /b 1
)

endlocal 