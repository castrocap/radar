@echo off
chcp 65001 > nul

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
if not exist .env (
    echo.
    echo Arquivo .env não encontrado. Vamos criar um...
    echo.
    set /p API_KEY="Cole sua chave da API Google aqui: "
    echo GOOGLE_API_KEY=%API_KEY%> .env
    echo.
    echo Arquivo .env criado com sucesso!
    echo.
)

:: Roda o programa
python main.py

:: Espera input antes de fechar
echo.
pause 