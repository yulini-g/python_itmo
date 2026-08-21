import random

class AIPlayer:
    def __init__(self, difficulty='medium'):
        self.difficulty = difficulty
        self.hits = []
        self.even_cells = True
        self.direction = None
        
    def choose_move(self, board):
        """Выбрать ход для компьютера"""
        if self.hits:
            move = self.finish_ship(board)
            if move:
                return move
            
        return self.random_move(board)

            
    def random_move(self, board):
        """Случайный выстрел по неоткрытым клеткам"""
        available = []
        for x in range(board.size):
            for y in range(board.size):
                if board.grid[y][x] in [0, 1]:
                    available.append((x, y))
                    
        if available:
            return random.choice(available)
        return None

    def finish_ship(self, board):
        """Добивание раненого корабля"""
        if not self.hits:
            return None
        
        if len(self.hits) == 1:
            return self.shoot_around_first_hit(board)
        
        return self.shoot_along_ship(board)
    
    def shoot_around_first_hit(self, board):
        """Стреляем вокруг первого попадания"""
        x, y = self.hits[0]
        neighbors = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1)]
        
        for nx, ny in neighbors:
            if self.is_valid_target(board, nx, ny):
                return (nx, ny)
            
        self.hits = []
        return self.random_move(board)
    
    def shoot_along_ship(self, board):
        """Стреляем вдоль корабля по направлению"""
        # Определяем направление по первым двум попаданиям
        x1, y1 = self.hits[0]
        x2, y2 = self.hits[1]
        
        if x1 == x2:
            self.direction = 'V'
        else:
            self.direction = 'H'
            
        if self.direction == 'H':
            min_x = min(hit[0] for hit in self.hits)
            max_x = max(hit[0] for hit in self.hits)
            y = self.hits[0][1]
            
            # Попытка слева (горизонтально)
            if self.is_valid_target(board, min_x - 1, y):
                return (min_x - 1, y)
            # Попытка справа (горизонтально)
            if self.is_valid_target(board, max_x + 1, y):
                return (max_x + 1, y)
        
        else:
            min_y = min(hit[1] for hit in self.hits)
            max_y = max(hit[1] for hit in self.hits)
            x = self.hits[0][0]
            
            # Попытка сверху (вертикально)
            if self.is_valid_target(board, x, min_y - 1):
                return (x, min_y - 1)
            # Попытка снизу (вертикально)
            if self.is_valid_target(board, x, max_y + 1):
                return (x, max_y + 1)
            
        return self.random_move(board)
        
    def is_valid_target(self, board, x, y):
        """Проверяет, можно ли стрелять в клетку"""
        if (x < 0 or
            x >= board.size or
            y < 0 or
            y >= board.size):
            
            return False
        
        if board.grid[y][x] in [0, 1]:
            return True
        
        return False
    
    def update_result(self, x, y, result):
        """Обновить состояние ИИ после выстрела"""
        if result == 'hit':
            self.hits.append((x, y))
        elif result == 'sunk':
            self.hits.clear()
            self.direction = None    
    
    
    
    
    
    # def chess_order_move(self, board): # Добработка для будующих версий
    #     """Стрельба через клетку (шахматный порядок)"""
    #     if self.even_cells:
    #         available = []
    #         for x in range(board.size):
    #             for y in range(board.size):
    #                 if ((x + y) % 2 == 0 and
    #                     board.grid[y][x] in [0, 1]):
    #                     available.append((x, y))
            
    #         if available:
    #             return random.choice(available)
    #         else:
    #             self.even_cells = False
    #     return self.random_move(board)