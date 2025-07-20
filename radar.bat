@echo off
chcp 65001 > nul
title RADAR - Análise de Código
color 0F

:: Vai para o diretório do script
cd /d "%~dp0"

:: Limpa a tela e mostra cabeçalho
cls
echo ========================================================
echo                RADAR - Análise de Código
echo ========================================================
echo.

:: Verifica arquivos necessários
echo Verificando arquivos...
if not exist main.py (
    echo [ERRO] Arquivo main.py não encontrado!
    goto :fim
)
if not exist agents.py (
    echo [ERRO] Arquivo agents.py não encontrado!
    goto :fim
)
if not exist requirements.txt (
    echo [ERRO] Arquivo requirements.txt não encontrado!
    goto :fim
)

:: Verifica Python
echo Verificando Python...
python --version > nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python não encontrado! Instale Python 3.9 ou superior.
    goto :fim
)

:: Verifica/cria ambiente virtual
echo Verificando ambiente virtual...
if exist guruenv\Scripts\activate.bat (
    echo Ativando ambiente virtual...
    call guruenv\Scripts\activate.bat
) else (
    echo Configurando novo ambiente...
    python -m venv guruenv
    if errorlevel 1 (
        echo [ERRO] Falha ao criar ambiente virtual!
        goto :fim
    )
    call guruenv\Scripts\activate.bat
    echo Instalando dependências...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERRO] Falha ao instalar dependências!
        goto :fim
    )
)

:: Verifica .env
echo Verificando configuração...
if not exist .env (
    echo [AVISO] Arquivo .env não encontrado!
    echo Criando arquivo .env...
    echo GOOGLE_API_KEY=sua_chave_aqui> .env
    echo.
    echo Configure sua chave da API no arquivo .env e rode novamente.
    goto :fim
)

:: Roda o RADAR
echo.
echo Iniciando análise...
echo.

python main.py
if errorlevel 1 (
    echo.
    echo [ERRO] O RADAR encontrou um problema! Veja os detalhes acima.
    goto :fim
)

echo.
echo Análise concluída com sucesso!

:fim
echo.
echo Pressione qualquer tecla para fechar...
pause > nul 