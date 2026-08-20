import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QGridLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette

class GameScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Морской бой')
        self.setFixedSize(475, 600)
        
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('#edf6ff'))
        self.setPalette(palette)
        
        # Заголовок
        self.title = QLabel('ВАШЕ ПОЛЕ')
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("""
                                    font-size: 20px;
                                    color: #14569c;
                                    margin-top: 2px;
                                    margin-bottom: 2px;
                                    """)
        
        # Стиль кнопок
        self.default_style = """
            QPushButton {
                background-color: #bddcfc;
                border: 0.5px solid #14569c;
                border-radius: 3px;
                min-width: 40px;
                max-width: 40px;
                min-height: 40px;
                max-height: 40px;}
            
            QPushButton:hover {
                background-color: #a6cef7;}
        """
        
        self.clicked_style = """
            QPushButton {
                background-color: #14569c;
                border: 0.5px solid #14569c;
                border-radius: 3px;
                min-width: 40px;
                max-width: 40px;
                min-height: 40px;
                max-height: 40px;}
        """
        
        # Сетка поля и кнокпи
        grid_container = QWidget()
        grid_container.setStyleSheet("""
            QWidget {
                background-color: #edf6ff;
            }
        """)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(3)
        
        grid_container.setLayout(grid_layout)  
        
        self.buttons = {}
        
        for row in range(10):
            for col in range(10):
                btn = QPushButton()
                btn.setFixedSize(40, 40)
                btn.setStyleSheet(self.default_style)
                
                btn.clicked.connect(lambda checked, x=row, y=col: self.on_cell_clicked(x, y))

                grid_layout.addWidget(btn, row, col)
                self.buttons[(row, col)] = btn
                
        # Кнопка "Назад в меню"
        self.back_btn = QPushButton('Назад в меню')
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: #bddcfc;
                color: #14569c;
                font-size: 20px;
                padding: 10px;
                border-radius: 10px;
                margin-top: 20px;}
                
            QPushButton:hover {
                background-color: #b6d8fc;}
            
            QPushButton:pressed {
                background-color: #7db7f5;}
        """)
        
        # Главный layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title)
        main_layout.addWidget(grid_container)  
        main_layout.addWidget(self.back_btn)
        main_layout.addStretch()
        
        self.setLayout(main_layout)
  
    def on_cell_clicked(self, x, y):
        """Обработка клика по клетке"""
        print(f"Клик по клетке: {x}, {y}")
        # Меняем цвет кнопки при клике
        self.buttons[(x, y)].setStyleSheet(self.clicked_style)
    
