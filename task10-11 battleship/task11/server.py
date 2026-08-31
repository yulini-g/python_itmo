import threading
import socket
import json
from game.ai import AIPlayer
from game.board import Board
from game.ship import Ship

def handle_client(client, address):
    """Реализует игру с одним клиентом"""
    print(f"Подключился клиент: {address}")
    
    # Создаём игровые поля
    server_board = Board()
    client_board = Board()

    # Расставляем корабли сервера
    server_board.place_ships_randomly()
    
    # Принимаем расстановку кораблей от клиента
    data = client.recv(1024)
    setup = json.loads(data.decode())
    
    if setup.get('action') == 'setup':
        client_board = Board()
        for ship_data in setup['ships']:
            ship = Ship(
                ship_data['x'],
                ship_data['y'],
                ship_data['size'],
                ship_data['orientation']
            )
            client_board.place_ship(ship)
        
        # Подтверждаем получение расстановки
        client.send(json.dumps({'status': 'ok'}).encode())
    
    # Создаём ИИ
    ai = AIPlayer(difficulty='medium')
    
    while True:
        # Получаем выстрел от клиента
        try:
            data = client.recv(1024)
            if not data:
                break
        except ConnectionResetError:
            print(f"Игрок отключился (соединение разорвано): {address}")
            break
        except Exception as e:
            print(f"Ошибка: {e}")
            break

        
        shot = json.loads(data.decode())
        x = shot['x']
        y = shot['y']
        
        print(f"Клиент стреляет: ({x}, {y})")
        
        # Обрабатываем выстрел
        result = server_board.receive_shot(x, y)
        
        # Если клиент попал или потопил - сервер не ходит
        if result in ['hit', 'sunk']:
            if server_board.is_all_sunk():
                response = {"result": result, "game_over": True, "winner": "client"}
            else:
                response = {"result": result, "game_over": False}
            client.send(json.dumps(response).encode())
            continue
        
        # Клиент промахнулся - ход сервера, накапливаем ходы
        server_moves = []
        
        while True:
            ai_move = ai.choose_move(client_board)
            if ai_move:
                ai_x, ai_y = ai_move
                ai_result = client_board.receive_shot(ai_x, ai_y)
                ai.update_result(ai_x, ai_y, ai_result)
                
                print(f"Сервер стреляет: ({ai_x}, {ai_y}) - {ai_result}")
                
                server_moves.append({"x": ai_x, "y": ai_y, "result": ai_result})
                
                # Проверяем, победил ли сервер
                if client_board.is_all_sunk():
                    response = {
                        "result": result,
                        "server_moves": server_moves,
                        "game_over": True,
                        "winner": "server"
                    }
                    client.send(json.dumps(response).encode())
                    break
                
                # Если сервер попал или потопил - ходит снова
                if ai_result in ['hit', 'sunk']:
                    continue
                else:
                    # Если сервер промахнулся - отправляем результат
                    response = {
                        "result": result,
                        "server_moves": server_moves,
                        "game_over": False
                    }
                    client.send(json.dumps(response).encode())
                    break
            else:
                # Нет доступных ходов
                response = {"result": result, "game_over": True, "winner": "client"}
                client.send(json.dumps(response).encode())
                break
        
        # Если сервер победил - выходим
        if client_board.is_all_sunk():
            break
    
    print(f"Игрок отключился: {address}")
    client.close()

# Создаём сокет
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 5555))
server.listen(5)

print("Сервер морского боя запущен! Ожидание игроков...")

while True:
    client, address = server.accept()
    thread = threading.Thread(target=handle_client, args=(client, address))
    thread.start()