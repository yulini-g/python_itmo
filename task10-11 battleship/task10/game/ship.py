class Ship:
    def __init__(self, x, y, size, orientation='H'): 
        self.x = x                     # Координата головы по x
        self.y = y                     # Координата головы по y
        self.size = size               # Размер корабля от 1 до 4
        self.orientation = orientation # Положение: H - горизонтально, V - вертикально

        self.hits = 0                  # Количество попаданий
    
    def get_cells(self):
        """Возвращает все клетки, которые занимает корабль"""
        cells = []
        for i in range(self.size):
            if self.orientation == 'H':
                cells.append((self.x + i, self.y))
            else:
                cells.append((self.x, self.y + i))
        return cells
                   
    def rotate(self):
        """Поворот корабля вокруг "головы" """ 
        if self.orientation == 'H':
            self.orientation = 'V'
        else:
            self.orientation = 'H'

    def is_hit(self, x, y):
        """Проверяет, попали ли по кораблю"""
        return (x, y) in self.get_cells()
        
    def is_sunk(self):
        """Проверяет, потоплен ли корабль"""
        return self.hits >= self.size
        