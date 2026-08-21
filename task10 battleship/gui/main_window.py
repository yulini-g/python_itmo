import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QStackedWidget
from PySide6.QtCore import Qt
from gui.game_screen import GameScreen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Морской бой')
        # self.setFixedSize(1000, 700) 
        
        # Переключение экранов
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Экран меню
        self.menu_screen = QWidget()
        self.setup_menu_screen()
        
        # Игровой экран
        self.game_screen = GameScreen()
        
        # Добавляем экраны в стопку
        self.stacked_widget.addWidget(self.menu_screen)   # индекс 0
        self.stacked_widget.addWidget(self.game_screen)   # индекс 1
        
        # Подключаем кнопку "Назад"
        self.game_screen.back_btn.clicked.connect(self.show_menu)
        
    def setup_menu_screen(self):    
        # Заголовок
        self.title = QLabel('⚓  МОРСКОЙ БОЙ  ⚓')
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("""
            font-size: 36px;
            font-weight: bold;
            color: #14569c;
            margin-top: 30px;
            margin-bottom: -2px;
        """)

        # Подзаголовок
        self.subtitle = QLabel('игра против компьютера')
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.subtitle.setStyleSheet("""
            font-size: 18px;
            color: #14569c;
            margin-bottom: 5px;
        """)
        
        # Кнопки
        self.show_game_btn = QPushButton('Новая игра')
        self.settings_btn = QPushButton('Настройки')
        self.records_btn = QPushButton('Рекорды')
        self.exit_btn = QPushButton('Выход')
        
        # Стиль кнопок
        button_style = """
            QPushButton {
                background-color: #9dc8f5;
                color: #14569c;
                font-size: 20px;
                padding: 15px;
                border-radius: 10px;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #b6d8fc;
            }
            QPushButton:pressed {
                background-color: #7db7f5;
            }
        """
        
        for button in [self.show_game_btn, 
                       self.settings_btn, 
                       self.records_btn, 
                       self.exit_btn]:
            button.setStyleSheet(button_style)       
            button.setFixedHeight(60)

        # Layout для кнопок
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(15)
        buttons_layout.setAlignment(Qt.AlignCenter)
                
        buttons_layout.addWidget(self.show_game_btn)
        buttons_layout.addWidget(self.settings_btn)
        buttons_layout.addWidget(self.records_btn)
        buttons_layout.addWidget(self.exit_btn)
        
        # Главный layout
        menu_layout = QVBoxLayout()
        menu_layout.addWidget(self.title)
        menu_layout.addWidget(self.subtitle)
        menu_layout.addSpacing(30)
        menu_layout.addLayout(buttons_layout)
        menu_layout.addStretch()
        
        # Устанавливаем layout в menu_screen
        self.menu_screen.setLayout(menu_layout)
        
        # Фон для меню
        self.menu_screen.setAutoFillBackground(True)
        palette = self.menu_screen.palette()
        from PySide6.QtGui import QColor, QPalette
        palette.setColor(QPalette.Window, QColor('#edf6ff'))
        self.menu_screen.setPalette(palette)
        
        # Сигналы
        self.show_game_btn.clicked.connect(self.show_game)
        self.settings_btn.clicked.connect(self.settings)
        self.records_btn.clicked.connect(self.records)
        self.exit_btn.clicked.connect(self.close)
    
    def show_game(self):
        """Показать игровой экран"""
        self.stacked_widget.setCurrentIndex(1)
    
    def show_menu(self):
        """Показать меню"""
        self.stacked_widget.setCurrentIndex(0)
    
    def settings(self):
        print("Открываем настройки")
        # Здесь будет окно настроек
    
    def records(self):
        print("Показываем рекорды")
        # Здесь будет окно рекордов

