import socket
import json

class NetworkClient:
    def __init__(self, host='localhost', port=5555):
        # Подключение к серверу
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        print("Подключено к серверу")
        
    def send_board(self, board):
        """Отправить расстановку кораблей на сервер"""
        ships = []
        for ship in board.ships:
            ships.append({
                'x': ship.x,
                'y': ship.y,
                'size': ship.size,
                'orientation': ship.orientation
            })
        
        grid_data = json.dumps({'action': 'setup', 'ships': ships})
        self.client.send(grid_data.encode())
        # Ждем подтверждение
        response = self.client.recv(1024)
        return json.loads(response.decode())
    
    def send_shot(self, x, y):
        """Отправить выстрел и получить ответ"""
        # Отправляем выстрел
        shot = {'x': x, 'y': y}
        self.client.send(json.dumps(shot).encode())
        
        # Получаем ответ
        data = self.client.recv(1024)
        response = json.loads(data.decode())
        
        return response
    
    def close(self):
        """Закрыть соединение"""
        self.client.close()