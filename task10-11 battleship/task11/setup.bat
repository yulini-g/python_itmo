@echo off
chcp 65001 >nul
echo ====================================
echo   Морской бой - Запуск
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
echo Запуск сервера в фоне...
start /b python server.py

echo Ожидание запуска сервера...
timeout /t 2 /nolog >nul

echo Запуск клиента...
python main.py

echo.
echo Завершение всех процессов Python...
taskkill /f /im python.exe >nul 2>&1

echo Приложение завершено.
pause