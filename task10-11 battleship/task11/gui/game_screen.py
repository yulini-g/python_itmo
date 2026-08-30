import sys
from game.board import Board
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QPalette
from gui.network_client import NetworkClient
from gui.records_dialog import RecordsManager
from PySide6.QtWidgets import QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QInputDialog

class GameScreen(QWidget):
    def __init__(self, difficulty='medium'):
        super().__init__()
        self.setWindowTitle('Морской бой')
        self.game_over = False
        self.player_moves = 0
        self.difficulty = difficulty
        
        # Создаём игровые поля
        self.player_board = Board()
        self.ai_board = Board()
        self.network = NetworkClient()
        
        # Расставляем корабли игрока
        self.player_board.place_ships_randomly()
        # Отправляем расстановку на сервер
        self.network.send_board(self.player_board)
        
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
        
        # Кнопка "Переставить корабли"
        self.rearrange_btn = QPushButton('🔄 Переставить корабли')
        self.rearrange_btn.setStyleSheet("""
            QPushButton {
                background-color: #9dc8f5;
                color: #14569c;
                font-size: 16px;
                padding: 12px;
                border-radius: 10px;
                min-width: 200px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #b6d8fc;
            }
            QPushButton:pressed {
                background-color: #7db7f5;
            }
        """)
        self.rearrange_btn.clicked.connect(self.rearrange_ships)
        
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
        main_layout.addWidget(self.rearrange_btn, alignment=Qt.AlignCenter)

        
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
        return grid_widget
    
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
        if self.game_over:
            return
        
        if self.ai_board.grid[y][x] in [2, 3]:
            return
        
        # Отправляем выстрел на сервер
        response = self.network.send_shot(x, y)
        result = response['result']
        
        self.rearrange_btn.hide()
        self.player_moves += 1
        
        # Обновление кнопки на поле противника
        if result == 'miss':
            self.ai_buttons[(x, y)].setStyleSheet(self.get_button_style('miss'))
            self.status_label.setText('💨 Промах! Ход противника...')
            self.ai_board.grid[y][x] = 3
            QTimer.singleShot(2000, lambda: self.process_server_moves(response.get('server_moves', [])))
        elif result == 'hit':
            self.ai_buttons[(x, y)].setStyleSheet(self.get_button_style('hit'))
            self.status_label.setText('🎯 Попадание! Стреляйте ещё раз!')
            self.ai_board.grid[y][x] = 2
        elif result == 'sunk':
            self.ai_buttons[(x, y)].setStyleSheet(self.get_button_style('sunk'))
            self.status_label.setText('💥 Корабль потоплен! Стреляйте ещё раз!')
            self.ai_board.grid[y][x] = 2

        # Проверка конца игры
        if response.get('game_over'):
            if response['winner'] == 'client':
                self.status_label.setText('🏆 ПОБЕДА! Вы потопили все корабли противника!')
                self.save_record()
            else:
                self.status_label.setText('💀 ПОРАЖЕНИЕ! Противник потопил все ваши корабли!')
            self.game_over = True
            return
        
        # Если игрок попал или потопил, он ходит снова
        if result in ['hit', 'sunk']:
            return
    
    def process_server_moves(self, server_moves, index=0):
        """Обработка ходов сервера с задержкой"""    
        if self.game_over:
            return
        
        if index >= len(server_moves):
            return
        
        move = server_moves[index]
        ai_x = move['x']
        ai_y = move['y']
        ai_result = move['result']
        
        if ai_result == 'miss':
            self.player_buttons[(ai_y, ai_x)].setStyleSheet(self.get_button_style('miss'))
            self.player_board.grid[ai_y][ai_x] = 3
            self.status_label.setText('💨 Противник промахнулся! Ваш ход!')
        elif ai_result == 'hit':
            self.player_buttons[(ai_y, ai_x)].setStyleSheet(self.get_button_style('hit'))
            self.player_board.grid[ai_y][ai_x] = 2
            self.status_label.setText('🎯 Противник попал в ваш корабль!')
        elif ai_result == 'sunk':
            self.player_buttons[(ai_y, ai_x)].setStyleSheet(self.get_button_style('sunk'))
            self.player_board.grid[ai_y][ai_x] = 2
            self.status_label.setText('💥 Противник потопил ваш корабль!')
        
        # Следующий ход с задержкой
        if index + 1 < len(server_moves):
            QTimer.singleShot(2000, lambda: self.process_server_moves(server_moves, index + 1))
    
    def rearrange_ships(self):
        """Переставляет корабли игрока случайно"""
        if self.game_over:
            return
        
        self.player_board = Board()
        self.player_board.place_ships_randomly()
        self.show_player_ships()
        self.status_label.setText('🎯 Корабли переставлены! Начинайте игру!')
    
    def save_record(self):
        """Сохранить рекорд после победы"""
        name, ok = QInputDialog.getText(
            self,
            'Победа!',
            f'Вы победили за {self.player_moves} ходов!\nВведите Ваше имя: '
        )
        
        if ok and name:
            records_manager = RecordsManager()
            records_manager.add_record(self.difficulty, name, self.player_moves)