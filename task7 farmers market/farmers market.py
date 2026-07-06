import json
import math as M
#================== РАБОТА С ДАННЫМИ =========================
def read_markets(filename):  # Читает CSV с табуляцией и возвращает список словарей.
    """
    >>> markets = read_markets('test.csv')

    >>> len(markets)
    49

    >>> markets[15]['FMID']
    '1019351'

    >>> markets[30]['MarketName']
    'Alexandria Farmers Market'

    >>> markets[40]['city']
    'Anaconda'
    """   
    result = []
    
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    
    header_line = lines[0].strip()
    headers = header_line.split(',')
    
    # Чистим заголовки от пробелов
    clean_headers = []
    for h in headers:
        clean_headers.append(h.strip())
    
    for i in range(1, len(lines)):
        line = lines[i].strip()
        if line == '':
            continue
        
        values = line.split(',')
        market = {}
        
        for j in range(len(clean_headers)):
            header = clean_headers[j]
            if j < len(values):
                value = values[j]
                # Убираем кавычки и пробелы по краям
                value = value.strip()
                value = value.strip('"')
                market[header] = value
            else:
                market[header] = ''
        
        result.append(market)
    
    return result
def save_markets(filename, markets):  # Сохраняет список словарей в csv файл.
    with open(filename, 'w', encoding='utf-8') as f:

        if len(markets) > 0:
            headers = list(markets[0].keys())

            # Записываем заголовки
            headline = ','.join(headers)
            f.write(headline + '\n')

            # Записываем каждый рынок
            for market in markets:
                values = []
                for header in headers:
                    values.append(market.get(header, ''))
                line = ','.join(values)
                f.write(line + '\n')       
def get_market_by_id(markets, fmid): # Находит рынок по ID.
    """
    >>> markets = read_markets('test.csv')

    >>> market = get_market_by_id(markets, '1018965')
    >>> market['MarketName']
    '61st Street Farmers Market'

    >>> market = get_market_by_id(markets, '1012157')
    >>> market['State']
    'Montana'

    >>> market = get_market_by_id(markets, '1021689')
    >>> market['zip']
    '97321'

    >>> market = get_market_by_id(markets, '1021309')
    >>> market['street']
    '29 West Butler Pike'
    """
    for market in markets:
        if market.get('FMID', '') == fmid:
            return market
    return None
def page_split(markets, page, per_page): # Делит список рынков по страницам с заданным количеством строк на странице.
    """
    >>> markets = read_markets('test.csv')

    >>> page2 = page_split(markets, 2, 10)
    >>> len(page2)
    10

    >>> page2[3]['FMID']
    '1021442'

    >>> page5 = page_split(markets, 3, 5)
    >>> len(page5)
    5

    >>> page5[2]['city']
    'Abita Springs'
    """
    start = (page - 1) * per_page
    end = start + per_page
    result = []

    for i in range(start, end):
        if i < len(markets):
            result.append(markets[i])
    
    return result
def search_by_city_state(markets, city, state): # Поиск рынков по городу и штату.
    """
    >>> markets = read_markets('test.csv')

    >>> res = search_by_city_state(markets, 'Abingdon', 'Virginia')
    >>> len(res)
    1

    >>> res = search_by_city_state(markets, 'Gettysburg', 'Pennsylvania')
    >>> len(res)
    2

    >>> res[0]['MarketName']
    'Adams County Farmers Market'

    >>> res[1]['FMID']
    '1019351'
    """
    city = city.strip().lower()
    state = state.strip().lower()

    result = []

    if city != '' and state != '':
        for market in markets:
            if state == market.get('State', '').lower():
                if city == market.get('city', '').lower():
                    result.append(market)


    elif city != '':
        for market in markets:
                if city == market.get('city', '').lower():
                    result.append(market)

    elif state != '':
        for market in markets:
            if state == market.get('State', '').lower():
                result.append(market)

    return result
def search_by_zip(markets, zip_code, radius): # Поиск рынков вокруг указанного ZIP. Если радиус не указан, ищет точное совпадение с ZIP.
    """
     >>> markets = read_markets('test.csv')
     >>> res = search_by_zip(markets, '17325', None)
     >>> len(res)
     2
     
     >>> res = search_by_zip(markets, '34604', None)
     >>> len(res)
     1

     >>> res = search_by_zip(markets, '66749', None)
     >>> len(res)
     2

     >>> res[0]['street']
     'Jefferson'

     >>> res[1]['FMID']
     '1019832'
    """
    if radius is None:
        result = []

        for market in markets:
            if market.get('zip', '') == zip_code:
                result.append(market)
        
        return result
    
    base_market = None
    for market in markets:
        if market.get('zip', '') == zip_code:
            base_market = market
            break

    if base_market is None:
        return []

    result = []
    for market in markets:
        y = market.get('y', '')
        x = market.get('x', '')
        if x == '' or y == '':
            continue
        if find_haversine(base_market, market) <= radius:
            result.append(market)
    
    return result
def sort_markets(markets, key, is_reversed, reviews): # Сортировка ранков по заданному ключу.
    """
    >>> markets = read_markets('test.csv')

    >>> res = sort_markets(markets, 'city_state', False, None)

    >>> res[0]['MarketName']
    'Alturas Farmers Market'

    >>> res[1]['MarketName']
    "29 Palms Farmers' Market"

    >>> res = sort_markets(markets, 'city_state', True, None)
    >>> res[5]['FMID']
    '1018261'

    >>> res = sort_markets(markets, 'zip', False, None)
    >>> res[5]['FMID']
    '1019847'

    >>> res = sort_markets(markets, 'zip', True, None)
    >>> res[2]['FMID']
    '1011171'
    """
    filtered = []
    for market in markets:
        if key == 'city_state': # Отбираем только рынки с заполненным ключом
            state = market.get('State', '')
            city = market.get('city', '')
            if state != '' and city != '':
                filtered.append(market)
        elif key == 'rating':
            filtered.append(market)
        else:
            value = market.get(key, '')
            if value != '':
                filtered.append(market)

    def get_key(market):
        if key == 'city_state':
            state = market.get('State', '')
            city = market.get('city', '')
            return state + '|' + city
        elif key == 'rating':
            if reviews is not None:
                data = get_rating_reviews(reviews, market.get('FMID', ''))
                return data['average_rating']
            return 0.0
        else:
            return market.get(key, '')
    
    return sorted(filtered, key=get_key, reverse=is_reversed)
def get_city_state(markets, reviews, reviews_file): # Запрашивает город и штат.
    city = input('Введите город (0 - любой): ').strip()
    state = input('Введите штат (0 - любой): ').strip()
    
    while city == '0' and state == '0':
        print('Ошибка: введите хотя бы город или штат.')
        city = input('Введите город (0 - любой): ').strip()
        state = input('Введите штат (0 - любой): ').strip()
    
    result = search_by_city_state(markets, city, state)

    if len(result) == 0:
        print('Ничего не найдено.')
        return

    print('\nНайдено рынков:', len(result))
    print('-' * 50)
    for i in range(len(result)):
        market = result[i]
        print(i + 1, '|', market.get('MarketName', ''), '|', market.get('city', ''), '|', market.get('State', ''))
        print('-' * 50)

    while True:
        choice = input('Введите номер рынка для просмотра деталей (0 - в меню): ').strip()
        if choice == '0':
            break
        if choice.isdigit():
            choice = int(choice)
            if choice > 0 and choice <= len(result):
                market = result[choice - 1]
                show_details(market, reviews, reviews_file)
            else:
                print('Введен некорректный номер.')
        else:
            print('Неверная команда.')
def get_zip(markets, reviews, reviews_file): # Запрашивает ZIP-код и показывает результат.
    while True:
        zip_code = input('Введите Ваш ZIP-код: ').strip()
        while zip_code.isdigit() == False or len(zip_code) != 5:
            print('Ошибка: некорректный ZIP-код.')
            zip_code = input('Введите Ваш ZIP-код: ').strip()
        found = False
        for market in markets:
            if market.get('zip', '') == zip_code:
                found = True
                break
        if found == False:
            print('Извините, данного ZIP-кода нет в базе данных.')
            choice = input('Хотите ввести дургой ZIP-код?\n1. Да\n2. Нет\n').strip()
            while choice not in ['1', '2']:
                print('Некорректная команда.')
                choice = input('Хотите ввести дургой ZIP-код?\n1. Да\n2. Нет\n').strip()

            if choice == '2':
                return
            else:
                continue
        else:
            break
    
    choice = input('Хотите задать радиус области для поиска?\n1. Да\n2. Нет\n').strip()
    while choice not in ['1', '2']:
                print('Некорректная команда.')
                choice = input('Хотите задать радиус области для поиска?\n1. Да\n2. Нет\n').strip()
    
    if choice == '2':
        radius = None

    else:
        while True:
            radius = input('Введите радиус области поиска в милях: ').strip()
            dots = 0
            ok = True
            for char in radius:
                if char == '.':
                    dots += 1
                elif char.isdigit() == False:
                    ok = False
            if (ok == True and
                dots <= 1 and
                radius != '' and
                radius != '.'):
                    radius = float(radius)
                    break
            else:
                print('Некорректная команда.')

    result = search_by_zip(markets, zip_code, radius)
    if len(result) == 0:
        print('Ничего не найдено.')
        return
    
    print('Найдено рынков:', len(result))
    print('-' * 50)
    for i in range(len(result)):
        market = result[i]
        print(i + 1, '|', 
              market.get('MarketName', ''), '|', 
              market.get('city', ''), '|', 
              market.get('State', ''))
        print('-' * 50)

    while True:
        choice = input('Введите номер рынка для просмотра деталей (0 - в меню): ').strip()
        if choice == '0':
            break
        if choice.isdigit():
            choice = int(choice)
            if 0 < choice and choice <= len(result):
                market = result[choice - 1]
                show_details(market, reviews, reviews_file)
            else:
                print('Введен некорректный номер.')
        else:
            print('Неверная команда.')
def get_sort_key(markets, reviews, reviews_file): # Определяет параметр, по которму будет происходить сортировка.
    print('\nДоступные ключи сортировки:', '1. Город и штат', '2. Название рынка', '3. Город', '4. Штат', '5. ZIP-код', '6. Рейтинг', '0. Выход в меню', sep='\n')

    keys = {'1': 'city_state', 
            '2': 'MarketName', 
            '3': 'city', 
            '4': 'State', 
            '5': 'zip', 
            '6': 'rating'
    }

    choice = input('\nВыберите ключ сортировки из списка (1-6): ').strip()
    while choice not in keys and choice != '0':
        if choice.isdigit():
            print('Введен неверный номер ключа.')
            choice = input('Выберите ключ сортировки из списка (1-6): ').strip()
        else:
            print('Введена неверная команда.')
            choice = input('Выберите ключ сортировки из списка (1-6): ').strip()
    
    if choice == '0':
        return
    
    key = keys[choice]

    order = input('\nСортировать по возрастанию или по убыванию?\n1. По возрастанию\n2. По убыванию\n3. Отмена\n').strip()
    while order not in ['1', '2', '3']:
        print('Введена неверная команда.')
        order = input('\nСортировать по возрастанию или по убыванию?\n1. По возрастанию\n2. По убыванию\n3. Отмена\n').strip()

    if order == '3':
        return
    
    if order == '1':
        is_reversed = False
    else:
        is_reversed = True
    
    sorted_list = sort_markets(markets, key, is_reversed, reviews)

    if len(sorted_list) == 0:
        print('Нет данных для отображения.')
        return
    
    all_markets_view(sorted_list, reviews, reviews_file)
def pick_market(markets, action):
    page = 1
    per_page = 10

    while True:
        on_page = page_split(markets, page, per_page)
        total_pages = len(markets) // per_page
        if len(markets) % per_page != 0:
            total_pages += 1
        
        print(f'\nСтраница {page} из {total_pages}')
        print('-' * 50)
        for i in range(len(on_page)):
            index = (page - 1) * per_page + i + 1
            market = on_page[i]
            print(index, '|', market.get('MarketName', ''), '|', market.get('city', ''), '|', market.get('State', ''))
        print('-' * 50)

        cmd = input(f'1. Следующая\n2. Предыдущая\n3. {action}\n4. В меню\n').strip()
        while cmd not in ['1', '2', '3', '4']:
            print('\nНеверная команда.')
            cmd = input(f'1. Следующая\n2. Предыдущая\n3. {action}\n4. В меню\n').strip()

        if cmd == '4':
            return None
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
            idx = input('Номер рынка (0 - отмена): ').strip()
            if idx == '0':
                continue
            if idx.isdigit():
                idx = int(idx)
                if 1 <= idx <= len(markets):
                    return markets[idx - 1]
                else:
                    print('Некорректный номер.')
            else:
                print('Неверная команда.')
def delete_market(markets, reviews, reviews_file): # Удаляет рынок по FMID.
    while True:
        market = pick_market(markets, 'Выбрать для удаления')
        if market is None:
            break
        show_details(market, reviews, reviews_file)
    
        choice = input('Удалить весь рынок или только рецензии на него?\n1. Рынок и рецензии\n2. Только рецензии\n3. Отмена\n').strip()
        while choice not in ['1', '2', '3']:
            print('Неверная команда.')
            choice = input('Удалить весь рынок или только рецензии на него?\n1. Рынок (с рецензями)\n2. Только рецензии\n3. Отмена\n').strip()

        if choice == '3':
            continue
        
        fmid = market.get('FMID', '')

        new_reviews = []
        for r in reviews:
            if r.get('fmid', '') != fmid:
                new_reviews.append(r)
        reviews.clear()
        for r in new_reviews:
            reviews.append(r)
        save_reviews(reviews_file, reviews)
        
        if choice == '2':
            print('\nВсе рецензии на рынок удалены.')
            break

        elif choice == '1':
            new_markets = []
            for m in markets:
                if m.get('FMID', '') != fmid:
                    new_markets.append(m)
            markets.clear()
            for m in new_markets:
                markets.append(m)
            save_markets('test.csv', markets)
            print('\nРынок и все рецензии на него удалены.')
            break
def find_haversine(market_1, market_2): # вычисляет расстояние между точками по формуле хаверсинуса.
    R = 3959 # Радиус Земли

    x1 = float(market_1.get('x', 0))
    y1 = float(market_1.get('y', 0))
    x2 = float(market_2.get('x', 0))
    y2 = float(market_2.get('y', 0))

    x = M.radians(x2 - x1) # Долгота
    y = M.radians(y2 - y1) # Широта

    # Применяем формулу гаверсинусов :
    haversine = 2 * R * M.asin(
        ((M.sin(y / 2)) ** 2 +
         M.cos(M.radians(y1)) *
         M.cos(M.radians(y2)) *
         (M.sin(x / 2)) ** 2
        ) ** 0.5
    )

    return haversine
#================== РАБОТА С РЕЙТИНГОМ И РЕЦЕНЗИЯМИ =========================
def load_reviews(filename): # Загружает рецензии из json файла.
    """
    Загружает рецензии из JSON-файла.
    Если файла нет, возвращает пустой список.
    
    >>> reviews = load_reviews('test_reviews.json')
    >>> type(reviews)
    <class 'list'>
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reviews = json.load(f)
        return reviews
    except FileNotFoundError:
        print('Файл не найден.')
        return []
def add_review(reviews, fmid, first_name, last_name, rating, text): # Добавляет рецензию.
    """
    Добавляет рецению на конкретный рынок к общему списку рецензий.
    Возвращает обновленный список.
    Рейтинг должен быть от 1 до 5.

    >>> reviews = []

    >>> reviews = add_review(reviews, '1018261', 'Иван', 'Петров', 4, 'Все супер!')
    >>> len(reviews)
    1
    >>> reviews[0]['first_name']
    'Иван'
    >>> reviews[0]['rating']
    4

    >>> reviews = add_review(reviews, '1008961', 'Елена', 'Васильева', 5, '')
    >>> len(reviews)
    2
    >>> reviews[1]['last_name']
    'Васильева'
    >>> reviews[1]['text']
    ''
    """
    if rating < 1 or rating > 5:
        return None
    
    new_review = {
        'fmid': fmid,
        'first_name': first_name,
        'last_name': last_name,
        'rating': rating,
        'text': text
    }

    result = []
    for review in reviews: # Необходимо, потому что функция не должна менять исходный список.
        result.append(review)
    result.append(new_review)

    return result
def save_reviews(filename, reviews): # Сохраняет рецензии в json файл.
    """
    >>> reviews = [{'fmid': '1018261', 'first_name': 'Иван', 'last_name': 'Петров', 'rating': 4, 'text': 'Все супер!'}]
    >>> save_reviews('tested_save.json', reviews)
    >>> loaded = load_reviews('tested_save.json')
    >>> len(loaded)
    1
    >>> loaded[0]['rating']
    4
    """    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(reviews, f, ensure_ascii=False, indent=4)
def get_rating_reviews(reviews, fmid): # Возвращает средний рейтинг и рецензии для рынка. 
    """
    >>> reviews = [{'fmid': '1000709', 'first_name': 'Иван', 'rating': 4, 'text': ''}, {'fmid': '1003563', 'first_name': 'Анна', 'rating': 5, 'text': 'Хорошо'}, {'fmid': '1000709', 'first_name': 'Петр', 'rating': 3, 'text': 'Норм'}]
    >>> result = get_rating_reviews(reviews, '1000709')
    >>> result['average_rating']
    3.5
    >>> len(result['reviews'])
    2
    >>> result = get_rating_reviews(reviews, '1003563')
    >>> result['average_rating']
    5.0
    >>> result = get_rating_reviews(reviews, '1008961')
    >>> result['average_rating']
    0.0
    >>> len(result['reviews'])
    0
    """
    market_reviews = []
    count = 0
    total = 0

    for review in reviews:
        if review.get('fmid', '') == fmid:
            market_reviews.append(review)
            total += review.get('rating', 0)
            count += 1

    if count == 0:
        average = 0.0
    else:
        average = round(total / count, 1)

    return{
        'average_rating': average,
        'reviews': market_reviews
    }
def leave_review(market, reviews, reviews_file): # Позволяет оставить оценку и\или рецензию на рынок.
    first_name = input('Введите имя: ').strip().title()
    last_name = input('Введите фамилию: ').strip().title()
    rating = None
    
    while rating is None:
        try:
            r = int(input('Рейтинг (1-5): ').strip())
            if r < 1 or r > 5:
                print('Ошибка: рейтинг должен быть от 1 до 5.')
            else:
                rating = r
        except ValueError:
            print('Ошибка: введите число.')

    choice = input('Хотите оставить отзыв о рынке?\n1. Да\n2. Нет')
    while choice not in ['1', '2']:
        print('Неверная команда.')
        choice = input('Хотите оставить отзыв о рынке?\n1. Да\n2. Нет')
    
    if choice == '1':
        text = input('Введите отзыв: ').strip()
    else:
        text = ''
    
    new_reviews_file = add_review(reviews, market.get('FMID', ''), first_name, last_name, rating, text)
    save_reviews(reviews_file, new_reviews_file)

    reviews.clear()
    for r in new_reviews_file:
        reviews.append(r)
    
    print('=' * 50)
    print('Рецензия добавлена!')
    print('=' * 50)
#================== ВЫВОД НА ЭКРАН =========================
def main_menu(markets, reviews_file): # Главное меню.
    reviews = load_reviews(reviews_file)
    while True:
        print()
        print('=' * 50)
        print('ФЕРМЕРСКИЕ РЫНКИ')
        print('=' * 50)
        print('1. Просмотр всех рынков')
        print('2. Поиск по городу и штату')
        print('3. Поиск по ZIP')
        print('4. Сортировка рынков')
        print('5. Удалить рынок')
        print('6. Выход')
        print('=' * 50)

        choice = input('Выберите действие (1-6): ').strip()
        while choice not in ['1', '2', '3', '4', '5', '6']:
            choice = input('Неверная команда. Введите число от 1 до 6: ')

        if choice == '1':
            print('\nПРОСМОТР ВСЕХ РЫНКОВ')
            all_markets_view(markets, reviews, reviews_file)
        elif choice == '2':
            print('\nПОИСК ПО ГОРОДУ И ШТАТУ')
            get_city_state(markets, reviews, reviews_file)
        elif choice == '3':
            print('\nПОИСК ПО ZIP')
            get_zip(markets, reviews, reviews_file)
        elif choice == '4':
            print('\nСОРТИРОВКА РЫНКОВ')
            get_sort_key(markets, reviews, reviews_file)
        elif choice == '5':
            print('\nУДАЛЕНИЕ РЫНКА')
            delete_market(markets, reviews, reviews_file)
        elif choice == '6':
            print('\nДо свидания!')
            break
def all_markets_view(markets, reviews, reviews_file): # Показывает все рынки по страницам.
    while True:
        market = pick_market(markets, 'Показать детали')
        if market is None:
            break
        show_details(market, reviews, reviews_file)
def show_details(market, reviews, reviews_file): # Показывает детали рынка, рецензии и предлагает оставить отзыв.
    print('\n' + '=' * 50)
    print('Название:', market.get('MarketName', ''))
    print('FMID:', market.get('FMID', ''))
    print('Адрес:', market.get('street', ''))
    print('Город:', market.get('city', ''))
    print('Штат:', market.get('State', ''))
    print('ZIP:', market.get('zip', ''))
    print('Сезон:', market.get('Season1Date'), '|', market.get('Season1Time'))
    print('=' * 50)

    # Рецензии
    market_rating = get_rating_reviews(reviews, market.get('FMID', ''))
    print('\nКоличество отзывов:', len(market_rating['reviews']))
    print('Среднй рейтинг рынка: ', market_rating['average_rating'])
    
    if len(market_rating['reviews']) > 0:
        answer = input('Посмотреть отзывы?\n1. Да\n2. Нет\n').strip()
        while answer not in ['1', '2']:
            print('Неверная команда.')
            answer = input('Посмотреть отзывы?\n1. Да\n2. Нет\n').strip()
        if answer == '1':
            for i in range(len(market_rating['reviews'])):
                comment = market_rating['reviews'][i]
                print(f"{i + 1}. {comment.get('first_name', '')} {comment.get('last_name', '')} пишет:")
                if comment.get('text', '') != '':
                    print('    ', comment.get('text', ''))
                print(f"    Оценка: {comment.get('rating', '')} / 5")
                print()
    
    answer = input('Хотите оставть отзыв об этом рынке?\n1. Да\n2. Нет ').strip()
    while answer not in ['1', '2']:
        print('Неверная команда.')
        answer = input('Хотите оставть отзыв об этом рынке?\n1. Да\n2. Нет \n').strip()
    if answer == '1':
        leave_review(market, reviews, reviews_file)
# #================== ТЕСТИРОВАНИЕ =========================
if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
# #================== ЗАПУСК =========================
if __name__ == '__main__':
    markets = read_markets('test.csv')
    main_menu(markets, 'reviews.json')
