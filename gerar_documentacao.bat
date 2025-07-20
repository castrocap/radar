@echo off
chcp 65001 >nul
title GURU - Documentação Técnica
color 1F

REM Ativa o ambiente virtual
call guruenv\Scripts\activate

REM Executa o programa principal
python main.py

pause
exit 