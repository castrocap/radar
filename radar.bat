@echo off
chcp 65001 > nul
setlocal EnableDelayedExpansion

:: Configura a janela
title RADAR - Análise de Código
color 0F
mode con: cols=70 lines=25

:: Limpa a tela
cls

:: Mostra cabeçalho
echo ========================================================
echo                RADAR - Análise de Código
echo ========================================================
echo.

:: Verifica Python
python --version > nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python não encontrado!
    echo Instale Python 3.9 ou superior.
    pause
    exit /b 1
)

:: Ativa ambiente virtual
if exist guruenv\Scripts\activate.bat (
    call guruenv\Scripts\activate.bat
) else (
    python -m venv guruenv
    call guruenv\Scripts\activate.bat
    pip install -r requirements.txt
)

:: Verifica/cria .env
echo Verificando configuração da API...
echo.

:: Tenta ler a chave atual
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
    echo [AVISO] A chave da API no arquivo .env parece inválida!
    echo.
    echo A chave deve começar com 'AIza' e ter cerca de 40 caracteres.
    echo.
    goto :pedir_chave
)

:: Roda o programa
python main.py
goto :fim

:pedir_chave
echo Para obter sua chave:
echo 1. Acesse https://makersuite.google.com/app/apikey
echo 2. Faça login com sua conta Google
echo 3. Clique em "Create API Key"
echo 4. Copie a chave gerada
echo.
set /p "API_KEY=Cole sua chave da API Google aqui: "
echo.

:: Salva a nova chave
echo GOOGLE_API_KEY=!API_KEY!> .env
echo Chave salva com sucesso!
echo.

:: Roda o programa
python main.py

:fim
echo.
pause
endlocal 