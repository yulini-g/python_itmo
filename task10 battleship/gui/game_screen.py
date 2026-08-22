import sys
from PySide6.QtWidgets import QApplication, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QPalette
from game.board import Board
from game.ai import AIPlayer

class GameScreen(QWidget):
    def __init__(self, difficulty='medium'):
        super().__init__()
        self.setWindowTitle('Морской бой')
        
        # Создаём игровые поля
        self.player_board = Board()
        self.ai_board = Board()
        self.ai = AIPlayer(difficulty=difficulty)
        
        # Расставляем корабли
        self.player_board.place_ships_randomly()
        self.ai_board.place_ships_randomly()
        
        # Статус игры
        self.status_label = QLabel('🎯 Ваш ход! Стреляйте по полю противника')
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            font-size: 18px;
            color: #14569c;
            margin: 15px;
            font-weight: bold;
        """)
        
        # Кнопки для полей
        self.player_buttons = {}
        self.ai_buttons = {}
        
        # Создаём контейнеры для полей
        player_container = self.create_board_container("ВАШЕ ПОЛЕ", self.player_board, is_player=True)
        ai_container = self.create_board_container("ПОЛЕ ПРОТИВНИКА", self.ai_board, is_player=False)
        
        # Layout для двух полей
        boards_layout = QHBoxLayout()
        boards_layout.setSpacing(30)
        boards_layout.addWidget(player_container)
        boards_layout.addWidget(ai_container)
        
        # Кнопка "Назад в меню"
        self.back_btn = QPushButton('🔙 Назад в меню')
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: #9dc8f5;
                color: #14569c;
                font-size: 16px;
                padding: 12px;
                border-radius: 10px;
                margin-top: 15px;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #b6d8fc;
            }
        """)
        
        # Главный layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.status_label)
        main_layout.addLayout(boards_layout)
        main_layout.addWidget(self.back_btn, alignment=Qt.AlignCenter)
        main_layout.addStretch()
        
        self.setLayout(main_layout)
        
        # Фон
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('#edf6ff'))
        self.setPalette(palette)
        
        # Показываем корабли игрока
        self.show_player_ships()
    
    def create_board_container(self, title, board, is_player):
        """Создать контейнер с полем и заголовком"""
        container = QWidget()
        container.setStyleSheet("""
            QWidget {
                background-color: #d4e8fc;
                border: 2px solid #14569c;
                border-radius: 15px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Заголовок
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 18px;
            color: #14569c;
            font-weight: bold;
            border: none;
        """)
        layout.addWidget(title_label)
        
        # Сетка поля (виджет)
        grid_widget = self.create_board_grid(board, is_player)
        layout.addWidget(grid_widget)
        layout.addStretch()
        
        container.setLayout(layout)
        return container
    
    def create_board_grid(self, board, is_player):
        """Создает сетку кнопок для поля"""
        grid_widget = QWidget()
        grid_widget.setStyleSheet("""
            QWidget {
                background-color: #edf6ff;
                border: none;
            }
        """)
        
        grid_layout = QGridLayout()
        grid_layout.setSpacing(3)
        grid_layout.setContentsMargins(10, 10, 10, 10)
        
        grid_layout.setAlignment(Qt.AlignCenter)
        
        empty_style = """
            QPushButton {
                background-color: #bddcfc;
                border: 1px solid #14569c;
                border-radius: 5px;
                min-width: 40px;
                max-width: 40px;
                min-height: 40px;
                max-height: 40px;
            }
            QPushButton:hover {
                background-color: #a6cef7;
                border: 2px solid #14569c;
            }
        """
        
        for row in range(board.size):
            for col in range(board.size):
                btn = QPushButton()
                btn.setFixedSize(42, 42)
                
                if is_player:
                    self.player_buttons[(row, col)] = btn
                else:
                    btn.clicked.connect(lambda checked, x=row, y=col: self.on_ai_board_click(x, y))
                    self.ai_buttons[(row, col)] = btn
                    btn.setStyleSheet(empty_style)
                
                grid_layout.addWidget(btn, row, col)
        
        grid_widget.setLayout(grid_layout)
        return grid_widget  # возвращаем виджет!
    
    def get_button_style(self, state):
        """Возвращает стиль кнопки в зависимости от состояния"""
        base_style = """
            QPushButton {
                border-radius: 5px;
                min-width: 40px;
                max-width: 40px;
                min-height: 40px;
                max-height: 40px;
                font-weight: bold;
            }
        """
        
        styles = {
            'empty': base_style + """
                QPushButton {
                    background-color: #bddcfc;
                    border: 1px solid #14569c;
                }
                QPushButton:hover {
                    background-color: #a6cef7;
                }
            """,
            'ship': base_style + """
                QPushButton {
                    background-color: #14569c;
                    border: 1px solid #14569c;
                }
            """,
            'miss': base_style + """
                QPushButton {
                    background-color: #ffffff;
                    border: 1px solid #14569c;
                }
            """,
            'hit': base_style + """
                QPushButton {
                    background-color: #ff6b6b;
                    border: 1px solid #cc0000;
                }
            """,
            'sunk': base_style + """
                QPushButton {
                    background-color: #cc0000;
                    border: 1px solid #990000;
                }
            """
        }
        return styles.get(state, styles['empty'])
    
    def show_player_ships(self):
        """Показать корабли игрока на его поле"""
        for row in range(self.player_board.size):
            for col in range(self.player_board.size):
                if self.player_board.grid[row][col] == 1:
                    self.player_buttons[(row, col)].setStyleSheet(
                        self.get_button_style('ship')
                    )
                else:
                    self.player_buttons[(row, col)].setStyleSheet(
                        self.get_button_style('empty')
                    )
    
    def on_ai_board_click(self, x, y):
        """Обработка клика по полю компьютера"""
        if self.ai_board.grid[y][x] in [2, 3]:
            return
        
        result = self.ai_board.receive_shot(x, y)
        
        if result == 'miss':
            self.ai_buttons[(x, y)].setStyleSheet(self.get_button_style('miss'))
            self.status_label.setText('💨 Промах! Ход противника...')
            # Только при промахе ход переходит к компьютеру
            QTimer.singleShot(700, self.ai_move)
        elif result == 'hit':
            self.ai_buttons[(x, y)].setStyleSheet(self.get_button_style('hit'))
            self.status_label.setText('🎯 Попадание! Стреляйте ещё раз!')
        elif result == 'sunk':
            self.ai_buttons[(x, y)].setStyleSheet(self.get_button_style('sunk'))
            self.status_label.setText('💥 Корабль потоплен! Стреляйте ещё раз!')
        
        if self.ai_board.is_all_sunk():
            self.status_label.setText('🏆 ПОБЕДА! Вы потопили все корабли противника!')
            return
    
    def ai_move(self):
        """Ход компьютера"""
        move = self.ai.choose_move(self.player_board)
        
        if move:
            x, y = move
            result = self.player_board.receive_shot(x, y)
            self.ai.update_result(x, y, result)
            
            if result == 'miss':
                self.player_buttons[(y, x)].setStyleSheet(self.get_button_style('miss'))
                self.status_label.setText('💨 Противник промахнулся! Ваш ход!')

            elif result == 'hit':
                self.player_buttons[(y, x)].setStyleSheet(self.get_button_style('hit'))
                self.status_label.setText('🎯 Противник попал! Он ходит снова...')
                QTimer.singleShot(700, self.ai_move)
            elif result == 'sunk':
                self.player_buttons[(y, x)].setStyleSheet(self.get_button_style('sunk'))
                self.status_label.setText('💥 Противник потопил ваш корабль! Он ходит снова...')
                QTimer.singleShot(700, self.ai_move)
            
            if self.player_board.is_all_sunk():
                self.status_label.setText('😢 ПОРАЖЕНИЕ! Противник потопил все ваши корабли!')
                
        def show_game(self):
            self.stacked_widget.removeWidget(self.game_screen)
            self.game_screen.deleteLater()
            
            self.game_screen = GameScreen(difficulty=self.current_difficulty)
            self.stacked_widget.addWidget(self.game_screen)
            self.game_screen.back_btn.clicked.connect(self.show_menu)
            self.stacked_widget.setCurrentWidget(self.game_screen)
