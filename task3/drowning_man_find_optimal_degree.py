import math as M
import doctest
def get_values(): # запрашиваем значения у пользователя
    d1 = float(input('Введите кратчайшее расстояние от спасателя до кромки воды в ярдах: '))
    d2 = float(input('Введите кратчайшее расстояние от утопающего до берега в футах: '))
    h = float(input('Введите боковое смещение между спасателем и утопающим в ярдах: '))
    v_sand = float(input('Введите скорость движения спасателя по песку в милях в час: '))
    n  = float(input('Введите коэффициент замедления спасателя при движении в воде: '))
    degree = float(input('Введите направление движения спасателя по песку в градусах: '))
    return d1, d2, h, v_sand, n, degree
def trans(d1, h, v_sand, degree): # переводим значения в единую систему
    return (round(d1 * 3, 4), 
            round(h * 3, 4), 
            round(v_sand * 5280, 4), 
            round(M.radians(degree), 4))
def formulas(d1, d2, h, v_sand, n, degree): # рассичываем значения по заданным формулам       
    x = d1 * M.tan(degree)
    l1 = (x ** 2 + d1 ** 2) ** 0.5
    l2 = ((h - x) ** 2 + d2 ** 2) ** 0.5
    t = (l1 + l2 * n) / v_sand
    t = round(t * 3600, 1)
    return t
# =========== поиск оптимального угла =============
def find_optimal_angle(d1, d2, h, v_sand, n):  # способ 1: перебор
    """   
    >>> d1, d2, h, v_sand, n, degree = 8, 10, 50, 5, 2, 39.413
    >>> d1, h, v_sand, degree = trans(d1, h, v_sand, degree)
    >>> find_optimal_angle(d1, d2, h, v_sand, n)
    (80, 23.5)
    
    >>> find_optimal_angle(6, 3, 12, 5280, 0.5)
    (21, 7.8)
    
    >>> find_optimal_angle(6, 3, 12, 5280, 1)
    (51, 10.2)
    
    >>> find_optimal_angle(6, 3, 12, 5280, 2)
    (60, 12.8)
    
    >>> find_optimal_angle(3, 1, 6, 2640, 0.8)
    (44, 9.2)
    
    >>> find_optimal_angle(6, 2, 12, 5280, 0.4)
    (13, 7.1)
    """
    best_angle = 0
    min_time = float('inf')
    
    for angle in range(0, 91):
        t = formulas(d1, d2, h, v_sand, n, M.radians(angle))
        if t < min_time:
            min_time = t
            best_angle = angle
    
    return best_angle, min_time

if __name__ == "__main__":
    doctest.testmod(verbose=True) 
# # ================ основная программа ================
d1, d2, h, v_sand, n, degree = get_values()
d1, h, v_sand, degree = trans(d1, h, v_sand, degree)
t = formulas(d1, d2, h, v_sand, n, degree)
best_angle, min_time = find_optimal_angle(d1, d2, h, v_sand, n)
print(f'Спасатель достигнет утопающего через {t} сек.')
print(f'Лучшее время {min_time} сек. может быть достигнуто при угле в {best_angle} градусов.')