@echo off
chcp 65001 >nul
echo ====================================
echo   Морской бой - Установка
echo ====================================
echo.
echo Проверка Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python не найден. Установите Python 3.8+ с python.org
    pause
    exit /b 1
)
echo Установка зависимостей...
python -m pip install -r requirements.txt
echo.
echo Запуск приложения...
python main.py
pause