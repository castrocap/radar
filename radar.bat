@echo off
chcp 65001 > nul
title RADAR - Análise de Código
color 0F
setlocal EnableDelayedExpansion

:: Função para mostrar erro e pausar
:erro
echo.
echo [ERRO] %~1
pause
exit /b 1

:: Verifica se está no diretório correto
cd /d "%~dp0"

cls
echo ========================================================
echo                RADAR - Análise de Código
echo ========================================================
echo.

:: Verifica Python
echo Verificando ambiente...
python --version > nul 2>&1
if errorlevel 1 (
    call :erro "Python não encontrado! Instale Python 3.9 ou superior."
)

:: Verifica se requirements.txt existe
if not exist requirements.txt (
    call :erro "Arquivo requirements.txt não encontrado!"
)

:: Verifica se main.py existe
if not exist main.py (
    call :erro "Arquivo main.py não encontrado!"
)

:: Ativa ambiente virtual
if exist guruenv\Scripts\activate.bat (
    echo Ativando ambiente virtual...
    call guruenv\Scripts\activate.bat
) else (
    echo Configurando novo ambiente...
    python -m venv guruenv
    if errorlevel 1 (
        call :erro "Falha ao criar ambiente virtual!"
    )
    call guruenv\Scripts\activate.bat
    echo Instalando dependências...
    pip install -r requirements.txt
    if errorlevel 1 (
        call :erro "Falha ao instalar dependências!"
    )
)

:: Roda o RADAR
echo.
echo Iniciando análise...
echo.

:: Captura saída do Python em variável
set "temp_file=%TEMP%\radar_output.txt"
python main.py > "%temp_file%" 2>&1

:: Mostra saída e mantém na tela
type "%temp_file%"
del "%temp_file%" > nul 2>&1

echo.
echo Pressione qualquer tecla para fechar...
pause > nul
endlocal 