from game.board import Board
from game.ai import AIPlayer

# Создаём поле для игрока
player_board = Board()
player_board.place_ships_randomly()

# Создаём ИИ
ai = AIPlayer(difficulty='medium')

print("=== ИГРА КОМПЬЮТЕРА ПРОТИВ ПОЛЯ ===")
print(f"Кораблей на поле: {len(player_board.ships)}")

# ИИ стреляет до победы
moves = 0
while not player_board.is_all_sunk():
    move = ai.choose_move(player_board)
    if move:
        x, y = move
        result = player_board.receive_shot(x, y)
        ai.update_result(x, y, result)
        moves += 1
        
        if result in ['hit', 'sunk']:
            print(f"Ход {moves}: ({x}, {y}) - {result}")
        
        if moves > 100:
            print("Слишком много ходов!")
            break
    else:
        print("Нет доступных ходов!")
        break

print(f"\nВсего ходов: {moves}")
print(f"Все корабли потоплены: {player_board.is_all_sunk()}")