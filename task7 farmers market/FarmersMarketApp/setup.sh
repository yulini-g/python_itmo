{
  "metadata": {
    "kernelspec": {
      "display_name": "Python (Pyodide)",
      "language": "python",
      "name": "python"
    },
    "language_info": {
      "codemirror_mode": {
        "name": "python",
        "version": 3
      },
      "file_extension": ".py",
      "mimetype": "text/x-python",
      "name": "python",
      "nbconvert_exporter": "python",
      "pygments_lexer": "ipython3",
      "version": "3.8"
    }
  },
  "nbformat_minor": 5,
  "nbformat": 4,
  "cells": [
    {
      "id": "b9670d85-ef29-4dfd-b4b5-e76d279c1f1a",
      "cell_type": "markdown",
      "source": "```python\n#!/bin/bash\n\necho \"==================================================\"\necho \"  Фермерские рынки США — установка\"\necho \"==================================================\"\necho \"\"\n\necho \"[1/2] Проверка установки Python...\"\nif ! command -v python3 &> /dev/null; then\n    echo \"❌ Python3 не найден!\"\n    echo \"\"\n    echo \"Установите Python 3.8 или выше:\"\n    echo \"  Ubuntu/Debian: sudo apt install python3\"\n    echo \"  macOS: brew install python3\"\n    echo \"\"\n    echo \"После установки запустите этот файл снова.\"\n    exit 1\nfi\n\necho \"✅ Python найден.\"\npython3 --version\necho \"\"\n\necho \"[2/2] Запуск приложения...\"\necho \"\"\npython3 \"Farmers Market.py\"\n\nif [ $? -ne 0 ]; then\n    echo \"\"\n    echo \"❌ Программа завершилась с ошибкой.\"\n    echo \"Проверьте наличие файла database.csv в папке с программой.\"\n    echo \"\"\nfi\n\nread -p \"Нажмите Enter для выхода...\"\npause```",
      "metadata": {}
    },
    {
      "id": "fc6fe193-e91f-42eb-8901-5286b817b7f9",
      "cell_type": "code",
      "source": "",
      "metadata": {
        "trusted": true
      },
      "outputs": [],
      "execution_count": null
    }
  ]
}