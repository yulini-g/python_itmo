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
echo Запуск сервера...
start "Морской бой - Сервер" python server.py

echo Ожидание запуска сервера...
timeout /t 2 /nolog >nul

echo Запуск клиента...
start "Морской бой - Клиент" python main.py

echo.
echo Приложение запущено!
pause