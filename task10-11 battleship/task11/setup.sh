#!/bin/bash
echo "===================================="
echo "  Морской бой - Установка"
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
echo "Запуск приложения..."
python3 main.py