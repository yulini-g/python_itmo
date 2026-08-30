import json
import os
from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton
from PySide6.QtCore import Qt

class RecordsManager:
    def __init__(self, filename='records.json'):
        self.filename = filename
        self.records = self.load()
        
    def load(self):
        """Загрузить рекорды из JSON"""
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
            
            for difficulty in data:
                if isinstance(data[difficulty], list):
                    data[difficulty].sort(key=lambda x: x['score'])
            return data
            
        return {
            'easy': [],
            'medium': [],
            'hard': []}
        
    def save(self):
        """Сохранить рекорды в JSON"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.records, f, ensure_ascii=False, indent=4)
    
    def add_record(self, difficulty, name, score):
        """Добавить рекорд"""
        if difficulty not in self.records:
            self.records[difficulty] = []
            
        self.records[difficulty].append({
            'name': name,
            'score': score})
        
        self.records[difficulty].sort(key=lambda x: x['score'])
        self.records[difficulty] = self.records[difficulty][:10]
        
        self.save()
        
    def get_records(self, difficulty):
        """Получить рекорды для сложности"""
        return self.records.get(difficulty, [])
    
class RecordsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Таблица рекордов')
        self.setFixedSize(700, 400)
        
        self.records_manager = RecordsManager()
        
        # Заголовок
        title = QLabel('🏆 ТАБЛИЦА РЕКОРДОВ 🏆')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
                            font-size: 24px;
                            font-weight: bold;
                            color: #14569c;
                            margin: 20px; """)
        
        # Три колонки
        columns_layout = QHBoxLayout()
        columns_layout.setSpacing(20)
        
        columns_layout.addWidget(self.create_column('Матрос', 'easy'))
        columns_layout.addWidget(self.create_column('Боцман', 'medium'))
        columns_layout.addWidget(self.create_column('Капитан', 'hard'))
        
        # Кнопка закрыть
        close_btn = QPushButton('Закрыть')
        close_btn.setStyleSheet("""
                                QPushButton {
                                    background-color: #9dc8f5;
                                    color: #14569c;
                                    font-size: 16px;
                                    padding: 10px;
                                    border-radius: 10px;
                                    min-width: 150px;
                                    border: 2px solid #14569c;}
                                    
                                QPushButton:hover {
                                    background-color: #b6d8fc; }""")
        close_btn.clicked.connect(self.close)
        
        # Главный layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(title)
        main_layout.addLayout(columns_layout)
        main_layout.addStretch()
        main_layout.addWidget(close_btn, alignment=Qt.AlignCenter)
        main_layout.addSpacing(20)
        
        self.setLayout(main_layout)
        
        self.setStyleSheet("""
                           QDialog{
                               background-color: #edf6ff; }""")
        
    def create_column(self, difficulty_name, difficulty_key):
        """Создать колонку с рекордами"""
        column = QWidget()
        column.setStyleSheet("""
                            QWidget {
                                background-color: #d4e8fc;
                                border: 2px solid #14569c;
                                border-radius: 15px; }""")
        
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Заголовок сложности
        difficulty_label = QLabel(difficulty_name)
        difficulty_label.setAlignment(Qt.AlignCenter)
        difficulty_label.setStyleSheet("""
                                    font-size: 20px;
                                    font-weight: bold;
                                    color: #14569c;
                                    border: none; """)
        layout.addWidget(difficulty_label)
        
        records = self.records_manager.get_records(difficulty_key)
        
        if not records:
            empty_label = QLabel('Результатов ещё нет...\nСтаньте первым!')
            empty_label.setAlignment(Qt.AlignCenter)
            empty_label.setStyleSheet("""
                font-size: 14px;
                color: #14569c;
                border: none;
                margin: 20px;
            """)
            layout.addWidget(empty_label)    
        else:
            medals = {0: '🥇', 1: '🥈', 2: '🥉'}
            for i in range(5):
                if i < len(records):
                    text = ''
                    record = records[i]
                    text = f'{i+1}. {record["name"]} — {record["score"]} ходов'
                    if i in medals:
                        text += f' {medals[i]}'
                else:
                    text = f'{i+1}. —'
                    
                player_label = QLabel(text)
                if i < len(records):
                    player_label.setStyleSheet("""
                        font-size: 14px;
                        color: #14569c;
                        border: none;
                        padding: 3px;
                    """)
                else:
                    player_label.setStyleSheet("""
                        font-size: 14px;
                        color: #999999;
                        border: none;
                        padding: 3px;
                    """)
                layout.addWidget(player_label)
                
        layout.addStretch()
        column.setLayout(layout)
        return column


                    
        
        
        
                        
        
