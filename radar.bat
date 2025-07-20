@echo off
chcp 65001 > nul
title RADAR - Análise de Código
color 0F
setlocal EnableDelayedExpansion

:: Função para mostrar erro e pausar
:erro
echo.
echo [ERRO] %~1
echo.
echo Arquivos encontrados no diretório:
dir /b
echo.
pause
exit /b 1

:: Verifica se está no diretório correto
cd /d "%~dp0"

cls
echo ========================================================
echo                RADAR - Análise de Código
echo ========================================================
echo.

:: Lista arquivos necessários
set "arquivos_necessarios=main.py agents.py requirements.txt"
set "faltando="

:: Verifica cada arquivo
for %%f in (%arquivos_necessarios%) do (
    if not exist "%%f" (
        set "faltando=!faltando! %%f"
    )
)

:: Se faltam arquivos, mostra erro
if not "!faltando!"=="" (
    echo [ERRO] Arquivos necessários não encontrados:!faltando!
    echo.
    echo Arquivos presentes no diretório:
    dir /b
    echo.
    pause
    exit /b 1
)

:: Verifica Python
echo Verificando ambiente...
python --version > nul 2>&1
if errorlevel 1 (
    call :erro "Python não encontrado! Instale Python 3.9 ou superior."
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

:: Executa com saída detalhada
python main.py 2>&1
if errorlevel 1 (
    echo.
    echo [ERRO] O RADAR encontrou um problema! Veja os detalhes acima.
    echo.
    pause
    exit /b 1
)

echo.
echo Pressione qualquer tecla para fechar...
pause > nul
endlocal 