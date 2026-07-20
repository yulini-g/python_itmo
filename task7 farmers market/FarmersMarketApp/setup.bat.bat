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
      "source": "```python\n@echo off\nchcp 65001 >nul\ntitle Фермерские рынки — установка\n\necho ==================================================\necho   Фермерские рынки США — установка\necho ==================================================\necho.\n\n:: Проверка Python\necho [1/2] Проверка установки Python...\npython --version >nul 2>&1\nif errorlevel 1 (\n    echo ❌ Python не найден!\n    echo.\n    echo Пожалуйста, установите Python 3.8 или выше.\n    echo Скачать: https://www.python.org/downloads/\n    echo.\n    echo После установки запустите этот файл снова.\n    pause\n    exit /b 1\n)\n\necho ✅ Python найден.\npython --version\necho.\n\n:: Запуск приложения\necho [2/2] Запуск приложения...\necho.\npython \"Farmers Market.py\"\n\n:: Если программа закрылась с ошибкой\nif errorlevel 1 (\n    echo.\n    echo ❌ Программа завершилась с ошибкой.\n    echo Проверьте наличие файла database.csv в папке с программой.\n    echo.\n)\n\npause```",
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