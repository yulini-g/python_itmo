from game.ship import Ship
import random

class Board:
    def __init__(self, size=10):
        self.size = size
        
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        
        self.ships = []
    
    def is_valid_position(self, ship):
        """Проверяет, можно ли разместить корабль на поле"""
        cells = ship.get_cells()
        
        for x, y in cells:
            if (x >= self.size or x < 0 or
                y >= self.size or y < 0):
                
                return False
            
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    nx, ny = x + i, y + j
                    
                    if (nx < 0 or nx >= self.size or
                        ny < 0 or ny >= self.size):
                        
                        continue
                    
                    if self.grid[ny][nx] == 1:
                        return False
        return True
        
    def place_ship(self, ship):
        """Размещает корабль на поле"""
        if not self.is_valid_position(ship):
            return False
        
        for x, y in ship.get_cells():
            self.grid[y][x] = 1
            
        self.ships.append(ship)
        return True
    
    def receive_shot(self, x, y):
        """
        Обрабатывает выстрел по клетке (x, y)
        0 - пустая клетка, 1 - расположен корабль, 2 - уже стреляли"""
        
        if self.grid[y][x] == 2:
            return 'already_shot'
        
        if self.grid[y][x] == 1:
            self.grid[y][x] = 2
            for ship in self.ships:
                if ship.is_hit(x, y):
                    ship.hits += 1
                    if ship.is_sunk():
                        return 'sunk'
                    return 'hit'
                
        else:
            self.grid[y][x] = 2
            return 'miss'
             
    def is_all_sunk(self):
        """Проверяет, все ли корабли потоплены"""
        for ship in self.ships:
            if not ship.is_sunk():
                return False
        return True
    
    def place_ships_randomly(self):
        """Случайная расстановка всех кораблей""" 
        ship_sizes = [1, 1, 1, 1,
                      2, 2, 2,
                      3, 3,
                      4]
        
        for size in ship_sizes:
            placed = False
            attempt = 0
            
            while not placed and attempt < 100:
                x = random.randint(0, self.size - 1)
                y = random.randint(0, self.size - 1)
                orientation = random.choice(['H', 'V'])
                
                ship = Ship(x, y, size, orientation)
                
                if self.place_ship(ship):
                    placed = True
                else:
                    attempt += 1
                    
            if not placed:
                self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
                self.ships = []
                return self.place_ships_randomly()
            
        return True
        
      