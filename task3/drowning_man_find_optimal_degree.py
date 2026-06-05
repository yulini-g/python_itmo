import math as M
def get_values(): # запрашиваем значения у пользователя
    d1 = input('Введите кратчайшее расстояние от спасателя до кромки воды в ярдах: ')
    d2 = input('Введите кратчайшее расстояние от утопающего до берега в футах: ')
    h = input('Введите боковое смещение между спасателем и утопающим в ярдах: ')
    v_sand = input('Введите скорость движения спасателя по песку в милях в час: ')
    n  = input('Введите коэффициент замедления спасателя при движении в воде: ')
    degree = input('Введите направление движения спасателя по песку в градусах: ')
    return d1, d2, h, v_sand, n, degree
def formulas(d1, d2, h, v_sand, n, degree): # рассичываем значения по заданным формулам
    # переводим в единую СИ:
    d1 = float(d1) * 3
    d2 = float(d2)
    h = float(h) * 3
    v_sand = float(v_sand) * 5280
    n = float(n)
    degree = float(degree)
        
    x = d1 * M.tan(M.radians(degree))
    l1 = (x ** 2 + d1 ** 2) ** 0.5
    l2 = ((h - x) ** 2 + d2 ** 2) ** 0.5
    t = (l1 + l2 * n) / v_sand
    t = round(t * 3600, 1)
    return t
# =========== поиск оптимального угла =============
def find_degree(d1, d2, h, v_sand, n):  # способ 1: перебор
    degree = 0.0

    best_degree = 0.0
    min_time = 99999999999999.9
    
    while degree <= 90.0:
        t = formulas(d1, d2, h, v_sand, n, degree)
        if t < min_time:
            min_time = t
            best_degree = degree
        degree += 0.1
        degree = round(degree, 1)  
    
    return min_time, round(best_degree)
# ================ модульные тесты ================
def tests():
    excepted = 39.9
    result = formulas(8, 10, 50, 5, 2, 39.413)
    min_time, best_degree = find_degree(8, 10, 50, 5, 2)
    print('Тест 1:')
    if excepted == result:
        print('Пройден успешно.')
    else:
        print('Провален.')
    print('Ожидаемый результат:', excepted)
    print('Полученный результат:', result)
    print(f'Лучшее время {min_time} сек. может быть достигнуто при угле в {best_degree} градусов.')
    print()
    # --------------------------------------------------
    excepted = 1717.3
    result = formulas(5, 20, 10, 1, 2, 89)
    min_time, best_degree = find_degree(5, 20, 10, 1, 2)
    print('Тест 2:')
    if excepted == result:
        print('Пройден успешно.')
    else:
        print('Провален.')
    print('Ожидаемый результат:', excepted)
    print('Полученный результат:', result)
    print(f'Лучшее время {min_time} сек. может быть достигнуто при угле в {best_degree} градусов.')
    print()
    # ---------------------------------------------------
    excepted = 30.7
    result = formulas(10, 40, 0, 2, 1.5, 0)
    min_time, best_degree = find_degree(10, 40, 0, 2, 1.5)
    print('Тест 3:')
    if excepted == result:
        print('Пройден успешно.')
    else:
        print('Провален.')
    print('Ожидаемый результат:', excepted)
    print('Полученный результат:', result)
    print(f'Лучшее время {min_time} сек. может быть достигнуто при угле в {best_degree} градусов.')
    print()
tests()
# ================ основная программа ================
d1, d2, h, v_sand, n, degree = get_values()
t = formulas(d1, d2, h, v_sand, n, degree)
min_time, best_degree = find_degree(d1, d2, h, v_sand, n)
print(f'Спасатель достигнет утопающего через {t} сек.')
print(f'Лучшее время {min_time} сек. может быть достигнуто при угле в {best_degree} градусов.')
