@echo off
chcp 65001 >nul
title Фермерские рынки — установка

echo ==================================================
echo   Фермерские рынки США — установка
echo ==================================================
echo.

:: Проверка Python
echo [1/2] Проверка установки Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден!
    echo.
    echo Пожалуйста, установите Python 3.8 или выше.
    echo Скачать: https://www.python.org/downloads/
    echo.
    echo После установки запустите этот файл снова.
    pause
    exit /b 1
)

echo ✅ Python найден.
python --version
echo.

:: Запуск приложения
echo [2/2] Запуск приложения...
echo.
python "Farmers Market.py"

:: Если программа закрылась с ошибкой
if errorlevel 1 (
    echo.
    echo ❌ Программа завершилась с ошибкой.
    echo Проверьте наличие файла database.csv в папке с программой.
    echo.
)

pause