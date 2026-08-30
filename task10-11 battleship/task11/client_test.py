import socket
import json

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 5555))
print('\nПодключение выполнено успешно.\nЧтобы выйти введите "Выход".\n\nПриятной игры!')

while True:
    coords = input("\nВведите координаты (x y): ").strip().lower()
    if coords == 'выход':
        break
    
    parts = coords.split()
    if len(parts) != 2:
        print("Введите два числа через пробел!")
        continue
    
    x = int(parts[0])
    y = int(parts[1])
    shot = {"x": x, "y": y}
    
    client.send(json.dumps(shot).encode())
    data = client.recv(1024)
    response = json.loads(data.decode())
    
    # Выводим результат выстрела игрока
    if response['result'] == 'miss':
        print("Ваш выстрел - промах")
    elif response['result'] == 'hit':
        print("Ваш выстрел - попадание")
    elif response['result'] == 'sunk':
        print("Ваш выстрел - корабль потоплен!")
    
    # Проверяем конец игры
    if response.get('game_over'):
        print(f"\nИгра окончена! Победитель: {response['winner']}")
        break
    
    # Если игрок попал или потопил — ходит снова
    if response['result'] in ['hit', 'sunk']:
        continue
    
    # Обрабатываем ходы сервера
    server_moves = response.get('server_moves', [])
    for move in server_moves:
        ai_x = move['x']
        ai_y = move['y']
        ai_result = move['result']
        
        if ai_result == 'miss':
            print(f"Сервер выстрелил: {ai_x} {ai_y} - промах")
        elif ai_result == 'hit':
            print(f"Сервер выстрелил: {ai_x} {ai_y} - попадание")
        elif ai_result == 'sunk':
            print(f"Сервер выстрелил: {ai_x} {ai_y} - корабль потоплен!")

client.close()