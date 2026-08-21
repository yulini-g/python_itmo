from game.ship import Ship
from game.board import Board

board = Board()
board.place_ships_randomly()

print("=== РАСПОЛОЖЕНИЕ КОРАБЛЕЙ ===")
for i, ship in enumerate(board.ships):
    print(f"Корабль {i+1}: размер={ship.size}, клетки={ship.get_cells()}")

print("\n=== ВЫСТРЕЛЫ ===")
for y in range(10):
    for x in range(10):
        result = board.receive_shot(x, y)
        if result in ['hit', 'sunk']:
            print(f"({x}, {y}) - {result}")

print("\n=== СОСТОЯНИЕ КОРАБЛЕЙ ===")
for i, ship in enumerate(board.ships):
    status = "ПОТОПЛЕН" if ship.is_sunk() else "не потоплен"
    print(f"Корабль {i+1}: размер={ship.size}, попаданий={ship.hits}, {status}")

print(f"\nВсе потоплены: {board.is_all_sunk()}")