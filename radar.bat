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

:: Limpa a tela e mostra cabeçalho
cls
echo ========================================================
echo                RADAR - Análise de Código
echo ========================================================
echo.

:: Verifica se está no diretório correto
echo Verificando diretório...
cd /d "%~dp0"

:: Lista arquivos necessários
echo Verificando arquivos...
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
    call :erro "Arquivos necessários não encontrados:!faltando!"
)

:: Verifica Python
echo Verificando Python...
python --version > nul 2>&1
if errorlevel 1 (
    call :erro "Python não encontrado! Instale Python 3.9 ou superior."
)

:: Verifica ambiente virtual
echo Verificando ambiente virtual...
if exist guruenv\Scripts\activate.bat (
    echo Ativando ambiente virtual...
    call guruenv\Scripts\activate.bat
    if errorlevel 1 (
        call :erro "Falha ao ativar ambiente virtual!"
    )
) else (
    echo Configurando novo ambiente...
    python -m venv guruenv
    if errorlevel 1 (
        call :erro "Falha ao criar ambiente virtual!"
    )
    call guruenv\Scripts\activate.bat
    if errorlevel 1 (
        call :erro "Falha ao ativar ambiente virtual!"
    )
    echo Instalando dependências...
    pip install -r requirements.txt
    if errorlevel 1 (
        call :erro "Falha ao instalar dependências!"
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
    echo.
    pause
    exit /b 1
)

:: Roda o RADAR
echo.
echo Iniciando análise...
echo.

:: Executa com saída detalhada
python main.py
if errorlevel 1 (
    call :erro "O RADAR encontrou um problema! Veja os detalhes acima."
)

echo.
echo Análise concluída com sucesso!
echo.
echo Pressione qualquer tecla para fechar...
pause > nul
endlocal 