import json
import os

class ConfigManager:
    def __init__(self, filename='config.json'):
        self.filename = filename
        self.config = self.load()
    
    def load(self):
        """Загрузить конфигурацию из JSON"""
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        # Значения по умолчанию
        return {
            'difficulty': 'medium'
        }
    
    def save(self):
        """Сохранить конфигурацию в JSON"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)
    
    def get_difficulty(self):
        """Получить сложность"""
        return self.config.get('difficulty', 'medium')
    
    def set_difficulty(self, difficulty):
        """Установить сложность"""
        self.config['difficulty'] = difficulty
        self.save()
