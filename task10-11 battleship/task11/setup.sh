#!/bin/bash

echo "===================================="
echo "  Морской бой - Запуск"
echo "===================================="
echo ""

echo "Проверка Python..."
if ! command -v python3 &> /dev/null; then
    echo "Python не найден. Установите Python 3.8+"
    exit 1
fi

echo "Установка зависимостей..."
pip3 install -r requirements.txt

echo ""
echo "Запуск сервера в фоне..."
python3 server.py &
SERVER_PID=$!

echo "Ожидание запуска сервера..."
sleep 2

echo "Запуск клиента..."
python3 main.py

echo ""
echo "Завершение сервера..."
kill $SERVER_PID

echo "Приложение завершено."