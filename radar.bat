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
echo Verificando configuração da API...
echo.

:: Se .env não existe, cria
if not exist .env (
    echo Arquivo .env não encontrado. Vamos criar um...
    echo.
    echo Para obter sua chave:
    echo 1. Acesse https://makersuite.google.com/app/apikey
    echo 2. Faça login com sua conta Google
    echo 3. Clique em "Create API Key"
    echo 4. Copie a chave gerada
    echo.
    set /p API_KEY="Cole sua chave da API Google aqui: "
    echo GOOGLE_API_KEY=%API_KEY%> .env
    echo.
    echo Arquivo .env criado com sucesso!
    echo.
) else (
    :: Verifica se a chave parece válida
    findstr /C:"GOOGLE_API_KEY=AIza" .env > nul
    if errorlevel 1 (
        echo [AVISO] A chave da API no arquivo .env parece inválida!
        echo.
        echo O arquivo .env existe mas a chave não parece correta.
        echo A chave deve começar com 'AIza' e ter cerca de 40 caracteres.
        echo.
        echo Quer configurar uma nova chave? (S/N)
        set /p RESPOSTA="Digite S para sim ou N para não: "
        if /I "!RESPOSTA!"=="S" (
            del .env
            echo.
            echo Para obter sua chave:
            echo 1. Acesse https://makersuite.google.com/app/apikey
            echo 2. Faça login com sua conta Google
            echo 3. Clique em "Create API Key"
            echo 4. Copie a chave gerada
            echo.
            set /p API_KEY="Cole sua chave da API Google aqui: "
            echo GOOGLE_API_KEY=%API_KEY%> .env
            echo.
            echo Arquivo .env atualizado com sucesso!
            echo.
        ) else (
            echo.
            echo Configure o arquivo .env manualmente e rode novamente.
            pause
            exit /b 1
        )
    )
)

:: Roda o programa
python main.py

:: Espera input antes de fechar
echo.
pause 