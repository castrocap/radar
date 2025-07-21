@echo off
chcp 65001 > nul
setlocal EnableDelayedExpansion

:: Garante que estamos no diretório correto
cd /d "%~dp0"

:: Configura a janela
title RADAR - Análise Inteligente de Código
color 0F
mode con: cols=80 lines=30

:: Limpa a tela
cls

:: Arte ASCII e cabeçalho
echo.
echo    ██████╗  █████╗ ██████╗  █████╗ ██████╗ 
echo    ██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗
echo    ██████╔╝███████║██║  ██║███████║██████╔╝
echo    ██╔══██╗██╔══██║██║  ██║██╔══██║██╔══██╗
echo    ██║  ██║██║  ██║██████╔╝██║  ██║██║  ██║
echo    ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
echo.
echo    Análise Inteligente de Código
echo    Powered by Google Gemini
echo    ═══════════════════════════════════════════
echo.

:: Verifica Python
python --version > nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python não encontrado!
    echo.
    echo Para usar o RADAR, você precisa:
    echo 1. Instalar Python 3.9 ou superior
    echo 2. Adicionar Python ao PATH do sistema
    echo.
    echo Baixe Python em: https://python.org
    echo.
    echo Pressione qualquer tecla para sair...
    pause > nul
    exit /b 1
)

:: Ativa ambiente virtual
if exist guruenv\Scripts\activate.bat (
    call guruenv\Scripts\activate.bat
) else (
    echo Configurando ambiente pela primeira vez...
    echo [1/2] Criando ambiente virtual...
    python -m venv guruenv
    if errorlevel 1 (
        echo [ERRO] Falha ao criar ambiente virtual.
        echo.
        echo Pressione qualquer tecla para sair...
        pause > nul
        exit /b 1
    )
    call guruenv\Scripts\activate.bat
    echo [2/2] Instalando dependências...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERRO] Falha ao instalar dependências.
        echo.
        echo Pressione qualquer tecla para sair...
        pause > nul
        exit /b 1
    )
    echo ✓ Ambiente configurado com sucesso!
    echo.
)

:: Verifica/cria .env
if exist .env (
    for /f "tokens=2 delims==" %%a in ('type .env ^| findstr "GOOGLE_API_KEY"') do set "API_KEY=%%a"
)

:: Se não existe .env ou a chave está vazia, pede uma nova
if not defined API_KEY (
    goto :pedir_chave
)

:: Verifica se a chave parece válida
echo !API_KEY! | findstr /r /c:"^AIza[a-zA-Z0-9_-]\{35,40\}$" >nul
if errorlevel 1 (
    echo [!] A chave da API atual parece inválida.
    echo.
    goto :pedir_chave
)

:: Roda o programa
python main.py
if errorlevel 1 (
    echo.
    echo [ERRO] O programa encontrou um erro durante a execução.
    echo.
    echo Pressione qualquer tecla para sair...
    pause > nul
    exit /b 1
)
goto :fim

:pedir_chave
echo Para obter sua chave da API Google Gemini:
echo.
echo 1. Acesse: https://makersuite.google.com/app/apikey
echo 2. Faça login com sua conta Google
echo 3. Clique em "Create API Key"
echo 4. Copie a chave gerada
echo.
set /p "API_KEY=Cole sua chave aqui: "
echo.

:: Salva a nova chave
echo GOOGLE_API_KEY=!API_KEY!> .env
echo ✓ Chave configurada com sucesso!
echo.

:: Roda o programa
python main.py
if errorlevel 1 (
    echo.
    echo [ERRO] O programa encontrou um erro durante a execução.
    echo.
    echo Pressione qualquer tecla para sair...
    pause > nul
    exit /b 1
)

:fim
echo.
echo Pressione qualquer tecla para sair...
pause > nul
endlocal 