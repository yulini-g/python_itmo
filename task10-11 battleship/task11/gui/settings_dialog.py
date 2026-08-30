from PySide6.QtWidgets import QDialog, QLabel, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PySide6.QtCore import Qt

class SettingsDialog(QDialog):
    def __init__(self, parent = None, current_difficulty='medium'):
        super().__init__(parent)
        self.setWindowTitle('Настройки')
        self.setFixedSize(400, 250)
        self.difficulty = current_difficulty
        
        title = QLabel('НАСТРОЙКИ')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
                            font-size: 24px;
                            font-weight: bold;
                            color: #14569c;
                            margin: 20px; """)
        
        difficulty_label = QLabel('Уровень сложности')
        difficulty_label.setStyleSheet("""
                                        font-size: 16px;
                                        color: #14569c; """)
        
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItem('Матрос', 'easy')
        self.difficulty_combo.addItem('Боцман', 'medium')
        self.difficulty_combo.addItem('Капитан', 'hard')
        
        self.difficulty_combo.setStyleSheet("""
                                            QComboBox {
                                                background-color: #bddcfc;
                                                color: #14569c;
                                                font-size: 16px;
                                                padding: 8px;
                                                border: None;
                                                border-radius: 5px;
                                                min-width: 200px;
                                            }
                                            QComboBox:hover {
                                                background-color: #a6cef7;
                                            }
                                            QComboBox::drop-down {
                                                border: none;
                                                width: 30px;
                                            }
                                            QComboBox::down-arrow {
                                                width: 8px;
                                                height: 8px;
                                                background-color: #14569c;
                                                border-radius: 4px;
                                                margin-right: 10px;
                                            }
                                            QComboBox QAbstractItemView {
                                                background-color: #ffffff;
                                                color: #14569c;
                                                font-size: 16px;
                                                padding: 5px;
                                                border: none;
                                                outline: none;
                                            }
                                            QComboBox QAbstractItemView::item {
                                                min-height: 30px;
                                                padding: 5px;
                                                padding-left: 10px;
                                            }
                                            QComboBox QAbstractItemView::item:hover {
                                                background-color: #f0f0f0;
                                                color: #14569c;
                                            }
                                            QComboBox QAbstractItemView::item:selected {
                                                background-color: #f0f0f0;
                                                color: #14569c;
                                                border-left: 3px solid #14569c;
                                                padding-left: 7px;
                                            }
                                        """)
        
        for i in range(self.difficulty_combo.count()):
            if self.difficulty_combo.itemData(i) == current_difficulty:
                self.difficulty_combo.setCurrentIndex(i)
                break
        
        save_btn = QPushButton('ОК')
        cancel_btn = QPushButton('Назад')
        
        button_style = """
                        QPushButton {
                            background-color: #bddcfc;
                            color: #14569c;
                            font-size: 14px;
                            padding: 8px;
                            border: None;
                            border-radius: 5px;
                            min-width: 50px;
                        }
                        QPushButton:hover {
                            background-color: #a6cef7;
                        }
                        QPushButton:pressed {
                            background-color: #7db7f5;
                        }
                    """

        save_btn.setStyleSheet(button_style)
        cancel_btn.setStyleSheet(button_style)
        
        # Кнопки ок и выход
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(save_btn)
        buttons_layout.addWidget(cancel_btn)
        buttons_layout.setSpacing(20)
        buttons_layout.setAlignment(Qt.AlignCenter)
        
        # Выбор сложности
        difficulty_layout = QVBoxLayout()
        difficulty_layout.addWidget(difficulty_label)
        difficulty_layout.addWidget(self.difficulty_combo)
        difficulty_layout.setSpacing(10)
        difficulty_layout.setAlignment(Qt.AlignCenter)
        
        # Главный
        main_layout = QVBoxLayout()
        main_layout.addWidget(title)
        main_layout.addLayout(difficulty_layout)
        main_layout.addStretch()
        main_layout.addLayout(buttons_layout)
        main_layout.addSpacing(20)
        
        self.setLayout(main_layout)
        
        self.setStyleSheet("""
                           QDialog {
                               background: #edf6ff;} """)
        
        save_btn.clicked.connect(self.save_settings)
        cancel_btn.clicked.connect(self.reject)
        
    def save_settings(self):
        """Сохранить настройки"""
        self.difficulty = self.difficulty_combo.currentData()
        self.accept()
    
    def get_difficulty(self):
        """Получить выбранную сложность"""
        return self.difficulty
    
    


