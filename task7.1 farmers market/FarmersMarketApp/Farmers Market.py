import json
import math as M
import csv

class Season:
    """
    Хранит информацию об одном сезоне работы рынка.
    
    >>> s = Season('01/01/2024', '09:00-17:00')
    >>> s.date
    '01/01/2024'
    >>> s.time
    '09:00-17:00'
    >>> s.is_valid()
    True

    >>> s2 = Season('', '')
    >>> s2.is_valid()
    False

    >>> s3 = Season('01/01/2024', '')
    >>> s3.is_valid()
    False
    
    >>> s4 = Season(None, '09:00-17:00')
    >>> s4.date
    ''
    >>> s4.time
    '09:00-17:00'
    """
    
    def __init__(self, date, time):
        self.date = date.strip() if date else ''
        self.time = time.strip() if time else ''
        
    def is_valid(self):
        """Возвращает True, если заполнены и дата, и время."""
        return self.date != '' and self.time != ''
class Market:
    """
    Хранит всю информацию об одном фермерском рынке.
    
    >>> m = Market('1018261', 'Test Market', '123 Main St', 'Boston', 'Massachusetts',
    ...            '02108', '-71.05', '42.35',
    ...            '01/01/2024', '09:00-17:00',
    ...            '06/01/2024', '10:00-16:00',
    ...            '', '',
    ...            '', '')
    >>> m.fmid
    '1018261'
    >>> m.market_name
    'Test Market'
    >>> m.city
    'Boston'
    >>> m.state
    'Massachusetts'
    >>> m.zip_code
    '02108'
    >>> len(m.seasons)
    4
    >>> m.seasons[0].is_valid()
    True
    >>> m.seasons[2].is_valid()
    False
    
    >>> data = {'FMID': '1000001', 'MarketName': 'Farm', 'street': '1 Lane', 'city': 'Portland',
    ...         'State': 'Oregon', 'zip': '97201', 'x': '-122.67', 'y': '45.52',
    ...         'Season1Date': '05/01', 'Season1Time': '8-5',
    ...         'Season2Date': '', 'Season2Time': '',
    ...         'Season3Date': '', 'Season3Time': '',
    ...         'Season4Date': '', 'Season4Time': ''}
    >>> m2 = Market.from_dict(data)
    >>> m2.fmid
    '1000001'
    >>> m2.market_name
    'Farm'
    >>> m2.seasons[0].is_valid()
    True
    >>> m2.seasons[1].is_valid()
    False
    """
    
    def __init__(self, fmid, market_name, street, city, state, zip_code, x, y,
                 season1date, season1time,
                 season2date, season2time,
                 season3date, season3time,
                 season4date, season4time):
        self.fmid = fmid
        self.market_name = market_name
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.x = x
        self.y = y
        self.seasons = [
            Season(season1date, season1time),
            Season(season2date, season2time),
            Season(season3date, season3time),
            Season(season4date, season4time)]
        
    @classmethod
    def from_dict(cls, data):
        """Создает Market из словаря (csv-строки)."""
        
        return cls(
            fmid = data.get('FMID', ''),
            market_name = data.get('MarketName', ''),
            street = data.get('street', ''),
            city = data.get('city', ''),
            state = data.get('State', ''),
            zip_code = data.get('zip', ''),
            x = data.get('x', ''),
            y = data.get('y', ''),
            season1date = data.get('Season1Date', ''),
            season1time = data.get('Season1Time', ''),
            season2date = data.get('Season2Date', ''),
            season2time = data.get('Season2Time', ''),
            season3date = data.get('Season3Date', ''),
            season3time = data.get('Season3Time', ''),
            season4date = data.get('Season4Date', ''),
            season4time = data.get('Season4Time', ''))
class Review:
    """
    Хранит данные об оценке и отзыве на один рынок.
    
    === Тесты __init__ ===
    
    >>> r = Review('1018261', 'Иван', 'Петров', 5, 'Отлично!')
    >>> r.fmid
    '1018261'
    >>> r.first_name
    'Иван'
    >>> r.last_name
    'Петров'
    >>> r.rating
    5
    >>> r.text
    'Отлично!'

    >>> r2 = Review('1000001', 'Анна', 'Сидорова', 3, '')
    >>> r2.rating
    3
    >>> r2.text
    ''

    >>> r3 = Review('', '', '', 1, '')
    >>> r3.fmid
    ''
    >>> r3.first_name
    ''
    >>> r3.rating
    1

    === Тесты from_dict ===

    >>> data = {'fmid': '1018261', 'first_name': 'Иван', 'last_name': 'Петров',
    ...         'rating': 4, 'text': 'Хорошо'}
    >>> r = Review.from_dict(data)
    >>> r.fmid
    '1018261'
    >>> r.first_name
    'Иван'
    >>> r.rating
    4
    >>> r.text
    'Хорошо'

    >>> data2 = {'fmid': '', 'first_name': '', 'last_name': '', 'rating': 0, 'text': ''}
    >>> r2 = Review.from_dict(data2)
    >>> r2.fmid
    ''
    >>> r2.rating
    0

    >>> data3 = {}
    >>> r3 = Review.from_dict(data3)
    >>> r3.fmid
    ''
    >>> r3.rating
    0

    === Тесты to_dict ===

    >>> r = Review('1018261', 'Иван', 'Петров', 5, 'Супер!')
    >>> d = r.to_dict()
    >>> d['fmid']
    '1018261'
    >>> d['first_name']
    'Иван'
    >>> d['last_name']
    'Петров'
    >>> d['rating']
    5
    >>> d['text']
    'Супер!'

    >>> r2 = Review('', '', '', 1, '')
    >>> d2 = r2.to_dict()
    >>> d2['fmid']
    ''
    >>> d2['rating']
    1
    >>> d2['text']
    ''
    """
    
    def __init__(self, fmid, first_name, last_name, rating, text):
        self.fmid = fmid
        self.first_name = first_name
        self.last_name = last_name
        self.rating = rating
        self.text = text
        
    @classmethod
    def from_dict(cls, data):
        """Создает объект Review из словаря json."""
        
        return cls(
            fmid = data.get('fmid', ''),
            first_name = data.get('first_name', ''),
            last_name = data.get('last_name', ''),
            rating = data.get('rating', 0),
            text = data.get('text', ''))
        
    def to_dict(self):
        """Преобразует объект Review в словарь для сохранения в json."""
        
        return {
            'fmid': self.fmid,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'rating': self.rating,
            'text': self.text}
class MarketDatabase:
    """
    Хранит список рынков.
    Осуществляет следующие действия с рынками:
        - Загрузка
        - Сохранение
        - Поиск по параметрам
        - Сортировка по параметрам
    ---------------------------------    
    === Тесты get_by_id ===

    >>> db = MarketDatabase()
    >>> db.markets = [Market('1018261', 'Market A', '', '', '', '', '', '',
    ...                      '', '', '', '', '', '', '', '')]
    >>> m = db.get_by_id('1018261')
    >>> m.market_name
    'Market A'

    >>> m = db.get_by_id('9999999')
    >>> m is None
    True

    >>> db2 = MarketDatabase()
    >>> db2.get_by_id('1018261') is None
    True

    === Тесты get_page ===

    >>> db = MarketDatabase()
    >>> m = Market('1', 'A', '', '', '', '', '', '', '', '', '', '', '', '', '', '')
    >>> for i in range(25):
    ...     db.markets.append(Market(str(i), f'M{i}', '', '', '', '', '', '', '', '', '', '', '', '', '', ''))
    >>> len(db.get_page(1))
    10
    >>> len(db.get_page(3))
    5
    >>> len(db.get_page(4))
    0

    === Тесты search_by_city_state ===

    >>> db = MarketDatabase()
    >>> m1 = Market('1', 'M1', '', 'Boston', 'Massachusetts', '', '', '', '', '', '', '', '', '', '', '')
    >>> m2 = Market('2', 'M2', '', 'Portland', 'Oregon', '', '', '', '', '', '', '', '', '', '', '')
    >>> m3 = Market('3', 'M3', '', 'Boston', 'Massachusetts', '', '', '', '', '', '', '', '', '', '', '')
    >>> db.markets = [m1, m2, m3]
    >>> len(db.search_by_city_state('Boston', 'Massachusetts'))
    2
    >>> len(db.search_by_city_state('Portland', 'Oregon'))
    1
    >>> len(db.search_by_city_state('Portland', ''))
    1
    >>> len(db.search_by_city_state('', 'Oregon'))
    1
    >>> len(db.search_by_city_state('', 'California'))
    0
    >>> len(db.search_by_city_state('Chicago', ''))
    0

    === Тесты get_by_zip ===

    >>> db = MarketDatabase()
    >>> m1 = Market('1', 'M1', '', '', '', '02108', '', '', '', '', '', '', '', '', '', '')
    >>> db.markets = [m1]
    >>> m = db.get_by_zip('02108')
    >>> m.market_name
    'M1'
    >>> db.get_by_zip('00000') is None
    True

    === Тесты search_by_zip ===

    >>> db = MarketDatabase()
    >>> m1 = Market('1', 'M1', '', '', '', '02108', '', '', '', '', '', '', '', '', '', '')
    >>> m2 = Market('2', 'M2', '', '', '', '02108', '', '', '', '', '', '', '', '', '', '')
    >>> m3 = Market('3', 'M3', '', '', '', '97201', '', '', '', '', '', '', '', '', '', '')
    >>> db.markets = [m1, m2, m3]
    >>> len(db.search_by_zip('02108'))
    2
    >>> len(db.search_by_zip('97201'))
    1
    >>> len(db.search_by_zip('00000'))
    0

    === Тесты find_haversine ===

    >>> db = MarketDatabase()
    >>> boston = Market('1', '', '', '', '', '', '-71.0589', '42.3601', '', '', '', '', '', '', '', '')
    >>> nyc = Market('2', '', '', '', '', '', '-74.0060', '40.7128', '', '', '', '', '', '', '', '')
    >>> round(db.find_haversine(boston, nyc), 1)
    190.2
    >>> la = Market('3', '', '', '', '', '', '-118.2437', '34.0522', '', '', '', '', '', '', '', '')
    >>> round(db.find_haversine(nyc, la), 1)
    2445.7

    === Тесты sort_markets ===

    >>> db = MarketDatabase()
    >>> m1 = Market('1', 'C Market', '', 'Boston', 'MA', '02108', '', '', '', '', '', '', '', '', '', '')
    >>> m2 = Market('2', 'A Market', '', 'Albany', 'NY', '12201', '', '', '', '', '', '', '', '', '', '')
    >>> m3 = Market('3', 'B Market', '', 'Portland', 'OR', '97201', '', '', '', '', '', '', '', '', '', '')
    >>> db.markets = [m1, m2, m3]
    >>> sorted_by_name = db.sort_markets('market_name')
    >>> sorted_by_name[0].market_name
    'A Market'
    >>> sorted_by_name[2].market_name
    'C Market'
    >>> sorted_by_city = db.sort_markets('city')
    >>> sorted_by_city[0].city
    'Albany'
    >>> sorted_by_city[2].city
    'Portland'
    >>> sorted_by_zip = db.sort_markets('zip_code', is_reversed=True)
    >>> sorted_by_zip[0].zip_code
    '97201'
    >>> sorted_by_zip[2].zip_code
    '02108'

    === Тесты delete_market ===

    >>> db = MarketDatabase()
    >>> m1 = Market('1', 'M1', '', '', '', '', '', '', '', '', '', '', '', '', '', '')
    >>> m2 = Market('2', 'M2', '', '', '', '', '', '', '', '', '', '', '', '', '', '')
    >>> db.markets = [m1, m2]
    >>> db.raw_data = {'1': {}, '2': {}}
    >>> db.delete_market('1')
    True
    >>> len(db.markets)
    1
    >>> db.markets[0].fmid
    '2'
    >>> '1' in db.raw_data
    False
    >>> db.delete_market('999')
    False
    >>> len(db.markets)
    1
    """

    def __init__(self):
        """ 
        Хранит словари целиком.
        Ключ = FMID (для сохранения).
        Нужно для будущего расширения, где понадобится работа с другими столбцами базы данных.
        При расширении будут добавлены атрибуты в Market и строки в save_to_csv.
        """
        self.markets = []
        self.raw_data = {}
        
    def load_from_csv(self, filename):
        """Читает csv и заполняет список рынков."""

        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                clean_row = {}
                for key, value in row.items():
                    clean_key = key.strip()
                    if value:
                        clean_value = value.strip()
                    else:
                        clean_value = ''
                    clean_row[clean_key] = clean_value
                    
                fmid = clean_row.get('FMID', '').strip()
                market_name = clean_row.get('MarketName', '')
                
                if fmid and market_name and fmid.isdigit():
                    self.raw_data[fmid] = clean_row
                    market = Market.from_dict(clean_row)
                    self.markets.append(market)
                    
    def save_to_csv(self, filename):
        """Сохраняет список рынков в файл csv."""
        
        if not self.markets:
            print('Отсутствует список рынков.')
            return
        
        first_fmid = list(self.raw_data.keys())[0]           # Берем первый попавшийся ключ
        filenames = list(self.raw_data[first_fmid].keys())   # Получаем названия столбцов
        
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=filenames)
            writer.writeheader()
            for market in self.markets:
                row = self.raw_data[market.fmid].copy()
                row['FMID'] = market.fmid
                row['MarketName'] = market.market_name
                row['street'] = market.street
                row['city'] = market.city
                row['State'] = market.state
                row['zip'] = market.zip_code
                row['x'] = market.x
                row['y'] = market.y
                row['Season1Date'] = market.seasons[0].date
                row['Season1Time'] = market.seasons[0].time
                row['Season2Date'] = market.seasons[1].date
                row['Season2Time'] = market.seasons[1].time
                row['Season3Date'] = market.seasons[2].date
                row['Season3Time'] = market.seasons[2].time
                row['Season4Date'] = market.seasons[3].date
                row['Season4Time'] = market.seasons[3].time
                writer.writerow(row)
                
    def get_by_id(self, fmid):
        """Находит рынок по ID."""
        
        for market in self.markets:
            if market.fmid == fmid:
                return market
        return None
    
    def get_page(self, page):
        """Возвращает список рынков для заданной страницы."""
        
        start = (page - 1) * 10
        end = start + 10
        return self.markets[start : end]
    
    def search_by_city_state(self, city, state):
        """Поиск рынков по городу и/или штату"""
        
        result = []
        city = city.lower().strip()
        state = state.lower().strip()
        
        if city != '' and state != '':
            for market in self.markets:
                if market.city.lower() == city:
                    if market.state.lower() == state:
                        result.append(market)
        
        elif city != '':
            for market in self.markets:
                if market.city.lower() == city:
                    result.append(market)
        
        elif state != '':
            for market in self.markets:
                if market.state.lower() == state:
                    result.append(market)
                    
        return result
    
    def get_by_zip(self, zip_code):
        """Поиск рынка по точному совпадению ZIP (для получения координат). Возвращает один словарь-рынок."""
        
        for market in self.markets:
            if market.zip_code == zip_code:
                return market
        return None
    
    def search_by_zip(self, zip_code):
        """Поиск всех рынков с точным совпадением ZIP. Возвращает список рынков."""
        
        result = []
        for market in self.markets:
            if market.zip_code == zip_code:
                result.append(market)
        return result
    
    def search_by_distance_from_market(self, base_market, radius):
        """Поиск рынков в радиусе от конкретного рынка."""
        result = []
        for market in self.markets:
            if market.x != '' and market.y != '':
                if self.find_haversine(base_market, market) <= radius:
                    result.append(market)
        return result
        
    def search_by_distance_from_zip(self, zip_code, radius):
        """Поиск рынков в радиусе от всех рынков с данным ZIP."""
        base_markets = self.search_by_zip(zip_code)
        result = set()
        
        for base_market in base_markets:
            nearby = self.search_by_distance_from_market(base_market, radius)
            result.update(nearby)
            
        return list(result)
    
    def find_haversine(self, market1, market2):
        """Вычисляет расстояние между двумя рынками в милях."""
        
        R = 3959
        
        x1 = float(market1.x)
        y1 = float(market1.y)
        x2 = float(market2.x)
        y2 = float(market2.y)
        
        x = M.radians(x2 - x1)
        y = M.radians(y2 - y1)
        
        haversine = 2 * R * M.asin(
            min(1.0, max(-1.0, (
                         (M.sin(y / 2)) ** 2 +
                         M.cos(M.radians(y1)) *
                         M.cos(M.radians(y2)) * 
                         (M.sin(x / 2)) ** 2
            ) ** 0.5))
        )
        
        return haversine
    
    def sort_markets(self, key, is_reversed=False, reviews_database=None):
        """
        Сортировка рынков по заданному ключу.
        key: 'market_name', 'city', 'state', 'zip_code', 'rating'
        """
        
        def get_key(market):
            if key == 'rating':
                if reviews_database is not None:
                    data = reviews_database.get_for_market(market.fmid)
                    return data['average_rating']
                return 0.0
            else:
                return getattr(market, key, '')
        
        if key == 'rating':
            filtered = self.markets[:]
        else:
            filtered = []
            for market in self.markets:
                value = getattr(market, key, '')
                if value:
                    filtered.append(market)
        return sorted(filtered, key=get_key, reverse=is_reversed)
    
    def delete_market(self, fmid):
        """Удаляет рынок по FMID. Возвращает True если удалён."""
        
        for i, market in enumerate(self.markets):
            if market.fmid == fmid:
                self.markets.pop(i)
                if fmid in self.raw_data:
                    del self.raw_data[fmid]
                return True
        return False
class ReviewDatabase:
    """
    Хранит список оценок и отзывов.
    Осуществляет следующие действия с оценками и отзывами :
        - Загрузка
        - Сохранение
        - Поиск рейтинга и отзывов на конкретный рынок
        - Добавление оценки и/или отзыва
        - Удаление оценки и/или отзыва
    --------------------------------- 
    === Тесты add_review ===

    >>> rdb = ReviewDatabase()
    >>> rdb.add_review('1018261', 'Иван', 'Петров', 5, 'Отлично!')
    True
    >>> len(rdb.reviews)
    1
    >>> rdb.reviews[0].fmid
    '1018261'
    >>> rdb.reviews[0].first_name
    'Иван'
    >>> rdb.reviews[0].rating
    5

    >>> rdb.add_review('1018261', 'Анна', 'Сидорова', 0, 'Плохо')
    False
    >>> len(rdb.reviews)
    1

    >>> rdb.add_review('1018261', 'Анна', 'Сидорова', 6, 'Супер!')
    False
    >>> len(rdb.reviews)
    1

    >>> rdb.add_review('1000001', 'Петр', 'Иванов', 3, '')
    True
    >>> len(rdb.reviews)
    2
    >>> rdb.reviews[1].text
    ''

    >>> rdb.add_review('1000001', '', '', 1, '')
    True
    >>> rdb.reviews[2].first_name
    ''
    >>> rdb.reviews[2].rating
    1

    === Тесты delete_reviews ===

    >>> rdb = ReviewDatabase()
    >>> rdb.add_review('1', 'A', 'B', 5, 'ok')
    True
    >>> rdb.add_review('1', 'C', 'D', 4, 'good')
    True
    >>> rdb.add_review('2', 'E', 'F', 3, 'fine')
    True
    >>> len(rdb.reviews)
    3
    >>> rdb.delete_reviews('1')
    >>> len(rdb.reviews)
    1
    >>> rdb.reviews[0].fmid
    '2'
    >>> rdb.delete_reviews('999')
    >>> len(rdb.reviews)
    1

    === Тесты get_for_market ===

    >>> rdb = ReviewDatabase()
    >>> rdb.add_review('1018261', 'Иван', 'Петров', 4, 'Хорошо')
    True
    >>> rdb.add_review('1018261', 'Анна', 'Сидорова', 2, 'Так себе')
    True
    >>> rdb.add_review('1000001', 'Петр', 'Иванов', 5, 'Отлично!')
    True

    >>> data = rdb.get_for_market('1018261')
    >>> data['average_rating']
    3.0
    >>> len(data['reviews'])
    2
    >>> data['reviews'][0].first_name
    'Иван'
    >>> data['reviews'][1].rating
    2

    >>> data = rdb.get_for_market('1000001')
    >>> data['average_rating']
    5.0
    >>> len(data['reviews'])
    1

    >>> data = rdb.get_for_market('9999999')
    >>> data['average_rating']
    0.0
    >>> len(data['reviews'])
    0
    """
    
    def __init__(self):
        self.reviews = []
        
    def load_from_json(self, filename):
        """Загружает отзывы из JSON-файла."""
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                reviews_data = json.load(f)
            for item in reviews_data:
                review = Review.from_dict(item)
                self.reviews.append(review)
        except FileNotFoundError:
            print('\nФайл с отзывами не найден.')
            print('Это нормально при первом запуске.')
            print('Файл будет создан автоматически, когда вы оставите первый отзыв.')
        
    def save_to_json(self, filename):
        """Сохраняет отзывы в JSON-файл."""
        
        reviews_data = []
        for review in self.reviews:
            dict_review = review.to_dict()
            reviews_data.append(dict_review)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(reviews_data, f, ensure_ascii=False, indent=4)
            
    def add_review(self, fmid, first_name, last_name, rating, text):
        """Добавляет новый отзыв. Возвращает True если отзыв добавлен успешно."""
        
        if rating < 1 or rating > 5:
            return False
        review = Review(fmid, first_name, last_name, rating, text)
        self.reviews.append(review)
        return True
    
    def delete_reviews(self, fmid):
        """Удаляет все отзывы для рынка."""
        
        for review in self.reviews.copy():
            if review.fmid == fmid:
                self.reviews.remove(review)
            
    def get_for_market(self, fmid):
        """
        Возвращает словарь со средним рейтингом и списком отзывов для рынка. 
        {'average_rating': float, 'reviews': list}
        """
        
        
        market_reviews = []
        total = 0
        
        for review in self.reviews:
            if review.fmid == fmid:
                total += review.rating
                market_reviews.append(review)
                
        if len(market_reviews) == 0:
            average = 0.0
        else:
            average = round(total / len(market_reviews), 1)
            
        return {
            'average_rating': average,
            'reviews': market_reviews
        }
class Interface:
    """Консольный интерфейс для взаимодействия с пользователем."""  
    
    def __init__(self, database, reviews_database):
        self.database = database
        self.reviews_database = reviews_database
    
    def run(self):
        """Главный цикл программы (меню)."""
        
        while True:
            print()
            print('=' * 50)
            print('ФЕРМЕРСКИЕ РЫНКИ')
            print('=' * 50)
            print('1. Просмотр всех рынков')
            print('2. Поиск по городу и штату')
            print('3. Поиск по ZIP')
            print('4. Поиск по удаленности')
            print('5. Сортировка рынков')
            print('6. Удалить рынок')
            print('7. Выход')
            print('=' * 50)
            
            choice = input('Выберите действие (1-7): ').strip()
            while choice not in ['1', '2', '3', '4', '5', '6', '7']:
                choice = input('Неверная команда. Введите число от 1 до 7: ').strip()
            
            if choice == '1':
                self._menu_show_all()
            elif choice == '2':
                self._menu_search_city_state()
            elif choice == '3':
                self._menu_search_zip()
            elif choice == '4':
                self._menu_search_distance()
            elif choice == '5':
                self._menu_sort()
            elif choice == '6':
                self._menu_delete()
            elif choice == '7':
                print('\nДо свидания!\n')
                break     
    
    def _menu_show_all(self, markets=None):
        """Постраничный просмотр всех рынков."""
        if markets is None:
            markets = self.database.markets
        
        ratings = {}
        for market in markets:
            ratings[market.fmid] = self.reviews_database.get_for_market(market.fmid)['average_rating']        
        
        total_pages = len(markets) // 10
        if len(markets) % 10 != 0:
            total_pages += 1
        page = 1
        
        while True:
            start = (page - 1) * 10
            end = start + 10
            on_page = markets[start:end]
            
            print(f'\nСтраница {page} из {total_pages}')
            print('-' * 100)
            for i, market in enumerate(on_page):
                index = start + i + 1
                print(f"{index} | {market.market_name} | {market.city} | {market.state} | {market.zip_code} | ★ {ratings[market.fmid]}")
                print('-' * 100)
                
            cmd = input('1. Следующая\n2. Предыдущая\n3. Показать детали\n4. В меню\n').strip()
            while cmd not in ['1', '2', '3', '4']:
                print('\nНеверная команда.')
                cmd = input('1. Следующая\n2. Предыдущая\n3. Показать детали\n4. В меню\n').strip()
            
            if cmd == '4':
                break
            elif cmd == '1':
                if page < total_pages:
                    page += 1
                else:
                    print('\nВы уже на последней странице.')
            elif cmd == '2':
                if page > 1:
                    page -= 1
                else:
                    print('\nВы уже на первой странице.')
            elif cmd == '3':
                index = input('Номер рынка (0 - отмена): ').strip()
                if index == '0':
                    continue
                if index.isdigit():
                    index = int(index)
                    if 1 <= index <= len(markets):
                        market = markets[index - 1]
                        self._show_details(market)
                    else:
                        print('Некорректный номер.')
                else:
                    print('Неверная команда.')

    def _show_details(self, market):
        """Показывает детали рынка, отзывы и предлагает оставить оценку."""
        
        print('\n' + '=' * 50)
        print('Название:', market.market_name)
        print('FMID:', market.fmid)
        print('Адрес:', market.street)
        print('Город:', market.city)
        print('Штат:', market.state)
        print('ZIP:', market.zip_code)
        
        for i, season in enumerate(market.seasons):
            if season.is_valid():
                print(f'Сезон {i + 1}:', season.date, '|', season.time)
        
        print('=' * 50)
        
        market_data = self.reviews_database.get_for_market(market.fmid)
        print('Количество отзывов:', len(market_data['reviews']))
        print('Средний рейтинг рынка:', market_data['average_rating'])

        print('=' * 50)
        
        if len(market_data['reviews']) > 0:
            answer = input('Посмотреть отзывы?\n1. Да\n2. Нет\n').strip()
            while answer not in ['1', '2']:
                print('Неверная команда.')
                answer = input('Посмотреть отзывы?\n1. Да\n2. Нет\n').strip()
            if answer == '1':
                for review in market_data['reviews']:
                    print(f"{review.first_name} {review.last_name} | Оценка: {review.rating}")
                    if review.text:
                        print(f"Отзыв: {review.text}")
                    print('.' * 50)
                    
        answer = input('Хотите оценить этот рынок?\n1. Да\n2. Нет\n').strip()
        while answer not in ['1', '2']:
            print('Неверная команда.')
            answer = input('Хотите оценить этот рынок?\n1. Да\n2. Нет\n').strip()
        if answer == '1':
            self._leave_review(market)
            
    def _leave_review(self, market):
        """Добавляет оценку и/или отзыв на рынок."""
        
        first_name = input('Введите имя: ').strip().title()
        last_name = input('Введите фамилию: ').strip().title()
        
        while first_name == '':
            print('Имя не может быть пустым!')
            first_name = input('Введите имя: ').strip().title()
            
        while last_name == '':
            print('Фамилия не может быть пустой!')
            last_name = input('Введите фамилию: ').strip().title()
            
        rating = None
        while rating is None:
            try:
                r = int(input('Введите число от 1 до 5: ').strip())
                while r > 5 or r < 1:
                    print('Рейтинг должен быть от 1 до 5!')
                    r = int(input('Введите число от 1 до 5: ').strip())
                rating = r
            except ValueError:
                print('Ошибка: введите число!')
        print('Спасибо, оценка поставлена!')
        
        choice = input('Хотите оставить развернутый отзыв об этом рынке?\n1. Да\n2. Нет\n')
        while choice not in ['1', '2']:
            print('Неверная команда.')
            choice = input('Хотите оставить развернутый отзыв об этом рынке?\n1. Да\n2. Нет\n')
            
        if choice == '1':
            text = input('Введите отзыв: ').strip()        
        else:
            text = ''
            
        self.reviews_database.add_review(market.fmid, first_name, last_name, rating, text)
        self.reviews_database.save_to_json('reviews.json')
        
        print('=' * 50)
        print('Ваш отзыв добавлен!')    
        print('=' * 50)    

    def _menu_search_city_state(self):
        """Поиск рынков по городу и штату."""
        
        print('\nПОИСК ПО ГОРОДУ И ШТАТУ\n')
        city = input('Введите город (0 - любой) ').strip().lower()
        state = input('Введите штат (0 - любой) ').strip().lower()
        
        while (city == '' and state == '') or (city == '0' and state == '0'):
            print('Ошибка: Введите хотя бы город или штат!')
            city = input('Введите город (0 - любой) ').strip().lower()
            state = input('Введите штат (0 - любой) ').strip().lower()
            
        if city == '0':
            city = ''
        if state == '0':
            state = ''
            
        result = self.database.search_by_city_state(city, state)
        self._show_search_result(result)
          
    def _show_search_result(self, result):
        """Показывает результаты поиска с возможностью просмотра деталей."""
        
        if len(result) == 0:
                print('Ничего не найдено.')
                return
            
        print('\nНайдено рынков:', len(result))
        print('-' * 100)
        for i, market in enumerate(result):
            print(f'{i + 1} | {market.market_name} | {market.state} | {market.city}')
            print('-' * 100)
         
        if len(result) == 1:
            choice = input('Хотите посмотреть детали рынка?\n1. Да\n2. Нет\n').strip()
            while choice not in ['1', '2']:
                print('Ошибка: неверная команда!')
                choice = input('Хотите посмотреть детали рынка?\n1. Да\n2. Нет\n').strip()
            
        else:
            choice = input('Хотите выбрать рынок для просмотра деталей?\n1. Да\n2. Нет\n').strip()
            while choice not in ['1', '2']:
                print('Ошибка: неверная команда!')
                choice = input('Хотите выбрать рынок для просмотра деталей?\n1. Да\n2. Нет\n').strip()
            
        if choice == '2':
            return
        else:
            while True:
                if len(result) == 1:
                    market = result[0]
                    break
                n = input('\nВведите номер рынка: ').strip()
                while True:
                    if not n.isdigit():
                        print('Ошибка: введите число!')
                        n = input('Введите номер рынка: ')
                        continue
                    
                    n = int(n)
                    if n > len(result) or n < 1:
                        print('Ошибка: неверный номер рынка!')
                        n = input('Введите номер рынка: ')
                        continue
                    else:
                        market = result[n - 1]
                        break
                break

            self._show_details(market)
    
    def _ask_zip_code(self):
        """Запрашивает ZIP-код и проверяет его наличие в базе. 
        Возвращает zip_code или None (если пользователь отказался от повторного поиска)."""
        while True:
            zip_code = input('Введите ZIP-код: ').strip()
            while not zip_code.isdigit() or len(zip_code) != 5:
                print('Ошибка: некорректный ZIP-код.')
                zip_code = input('Введите ZIP-код: ').strip()
            
            found = self.database.search_by_zip(zip_code)
            
            if len(found) == 0:
                print('Извините, данного ZIP-кода нет в базе данных.')
                choice = input('Хотите ввести другой ZIP-код?\n1. Да\n2. Нет\n').strip()
                while choice not in ['1', '2']:
                    print('Некорректная команда.')
                    choice = input('Хотите ввести другой ZIP-код?\n1. Да\n2. Нет\n').strip()
                if choice == '2':
                    return None
            else:
                return zip_code
    
    def _menu_search_zip(self):
        """Поиск рынков по точному совпадению ZIP."""
        
        print('\nПОИСК ПО ZIP\n')

        zip_code = self._ask_zip_code()
        if zip_code is None:
            return
        
        found = self.database.search_by_zip(zip_code)
        self._show_search_result(found)
                
    def _menu_search_distance(self):
        """Поиск рынков в радиусе от заданного ZIP."""
        
        print('\nПОИСК ПО УДАЛЕННОСТИ\n')
        
        zip_code = self._ask_zip_code()
        if zip_code is None:
            return
        
        found = self.database.search_by_zip(zip_code)
            
        if len(found) > 1:
            print(f'Найдено {len(found)} рынков с ZIP-кодом {zip_code}:\n')
            for i, market in enumerate(found):
                print(f'{i + 1} | {market.market_name} | {market.state} | {market.city}') 
                print('-' * 100)
                
            choice = input('Хотите выбрать конкретный рынок и искать от него или искать от всех рынков сразу?\n1. Выбрать конкретный рынок\n2. Искать от всех рынков с данным ZIP-кодом\n').strip()
            while choice not in ['1', '2']:
                print('Некорректная команда.')
                choice = input('Хотите выбрать конкретный рынок и искать от него или искать от всех рынков сразу?\n1. Выбрать конкретный рынок\n2. Искать от всех рынков с данным ZIP-кодом\n').strip()
        else:
            choice = '1'
            
            
        while True:
            radius = input('Введите радиус области поиска в милях: ').strip()
            dots = 0
            ok = True
            for char in radius:
                if char == '.':
                    dots += 1
                elif not char.isdigit():
                    ok = False
            if (ok and
                dots <= 1 and
                radius != '' and
                radius != '.'):
                    radius = float(radius)
                    break
            else:
                print('Некорректная команда.\n') 
                
        if len(found) == 1:
            result = self.database.search_by_distance_from_market(found[0], radius)
        elif choice == '1':
            index = input('Введите номер рынка: ').strip()
            while True:
                if not index.isdigit():
                    print('Ошибка: введите число!\n')
                    index = input('Введите номер рынка: ').strip()
                    continue
                index = int(index)    
                if index > len(found) or index < 1:
                    print('Ошибка: некорректный номер рынка!\n')
                    index = input('Введите номер рынка: ').strip()
                    continue
                break
            base_market = found[index - 1]
            result = self.database.search_by_distance_from_market(base_market, radius)

        else:
            result = self.database.search_by_distance_from_zip(zip_code, radius)
            
        self._show_search_result(result)
        
    def _menu_sort(self):
        """Сортировка рынков по выбранному ключу."""
        
        print('\nСОРТИРОВКА РЫНКОВ\n')
        print('Доступные ключи сортировки:')
        print('1. Город')
        print('2. Штат')
        print('3. Название рынка')
        print('4. ZIP-код')
        print('5. Рейтинг')
        print('0. Выход в меню')
        
        keys = {
            '1': 'city',
            '2': 'state',
            '3': 'market_name',
            '4': 'zip_code',
            '5': 'rating'
        }
        
        key_names = {
            'city': 'Город',
            'state': 'Штат',
            'market_name': 'Название рынка',
            'zip_code': 'ZIP-код',
            'rating': 'Рейтинг'
        }
        
        choice = input('\nВыберите ключ сортировки (1-5): ').strip()
        while choice not in keys and choice != '0':
            print('Неверная команда.')
            choice = input('Выберите ключ сортировки (1-5): ').strip()
        
        if choice == '0':
            return
        
        key = keys[choice]

        order = input('\nСортировать:\n1. По возрастанию\n2. По убыванию\n3. Отмена\n').strip()
        while order not in ['1', '2', '3']:
            print('Неверная команда.')
            order = input('Сортировать:\n1. По возрастанию\n2. По убыванию\n3. Отмена\n').strip()
        
        if order == '3':
            return

        is_reversed = order == '2'
        
        result = self.database.sort_markets(key, is_reversed, self.reviews_database)
    
        if not result:
            print('Нет данных для отображения.')
            return
        
        print(f"\nСортировка по параметру: {key_names.get(key, key)}")
        if not is_reversed:
            print('Порядок по возрастанию.')
        else:
            print('Порядок по убыванию.')

        self._menu_show_all(result)

    def _menu_delete(self):
        """Удаление рынка и/или отзывов."""
        
        print('\nУДАЛЕНИЕ РЫНКА')
        
        page = 1
        total_pages = len(self.database.markets) // 10
        if len(self.database.markets) % 10 != 0:
            total_pages += 1
        
        while True:
            on_page = self.database.get_page(page)
            print(f'\nСтраница {page} из {total_pages}')
            print('-' * 100)
            for i, market in enumerate(on_page):
                index = (page - 1) * 10 + i + 1
                print(f"{index} | {market.market_name} | {market.city} | {market.state}")
                print('-' * 100)
            
            cmd = input('1. Следующая\n2. Предыдущая\n3. Выбрать для удаления\n4. В меню\n').strip()
            while cmd not in ['1', '2', '3', '4']:
                print('\nНеверная команда.')
                cmd = input('1. Следующая\n2. Предыдущая\n3. Выбрать для удаления\n4. В меню\n').strip()
            
            if cmd == '4':
                break
            elif cmd == '1':
                if page < total_pages:
                    page += 1
                else:
                    print('\nВы уже на последней странице.')
            elif cmd == '2':
                if page > 1:
                    page -= 1
                else:
                    print('\nВы уже на первой странице.')
            elif cmd == '3':
                index = input('Номер рынка (0 - отмена): ').strip()
                if index == '0':
                    continue
                if index.isdigit():
                    index = int(index)
                    if 1 <= index <= len(self.database.markets):
                        market = self.database.markets[index - 1]
                        
                        choice = input('\nУдалить:\n1. Рынок и отзывы\n2. Только отзывы\n3. Отмена\n').strip()
                        while choice not in ['1', '2', '3']:
                            print('Неверная команда.')
                            choice = input('Удалить:\n1. Рынок и отзывы\n2. Только отзывы\n3. Отмена\n').strip()
                        
                        if choice == '3':
                            continue
                        elif choice == '2':
                            self.reviews_database.delete_reviews(market.fmid)
                            self.reviews_database.save_to_json('reviews.json')
                            print('\nВсе отзывы на рынок удалены.')
                            break
                        elif choice == '1':
                            self.reviews_database.delete_reviews(market.fmid)
                            self.reviews_database.save_to_json('reviews.json')
                            self.database.delete_market(market.fmid)
                            self.database.save_to_csv('database.csv')
                            print('\nРынок и все отзывы на него удалены.')
                            break
                    else:
                        print('Некорректный номер.')
                else:
                    print('Неверная команда.')
    
if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
    
if __name__ == '__main__':
    database = MarketDatabase()
    database.load_from_csv('database.csv')
    
    reviews_database = ReviewDatabase()
    reviews_database.load_from_json('reviews.json')
    
    app = Interface(database, reviews_database)
    app.run()