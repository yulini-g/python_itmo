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
    """
    >>> trans(8, 50, 5, 39.413)
    (24, 150, 26400, 0.6879)
    
    >>> trans(2, 4, 1, 45)
    (6, 12, 5280, 0.7854)
    
    >>> trans(1.5, 2.3, 0.5, 90)
    (4.5, 6.9, 2640.0, 1.5708)
    
    >>> trans(0, 0, 0, 180)
    (0, 0, 0, 3.1416)
    """
    return (round(d1 * 3, 4), 
            round(h * 3, 4), 
            round(v_sand * 5280, 4), 
            round(M.radians(degree), 4))

def formulas(d1, d2, h, v_sand, n, degree): # рассичываем значения по заданным формулам       
    """
    >>> formulas(24, 10, 150, 26400, 2, 0.6879)
    39.9
    
    >>> formulas(6, 3, 12, 5280, 0.5, 0.7854)
    8.1
    
    >>> formulas(0, 3, 12, 5280, 0.5, 0.0)
    4.2
    
    >>> formulas(6, 0, 12, 5280, 1.0, 0.7854)
    9.9
    
    >>> formulas(3, 1, 6, 2640, 0.8, 0.5236)
    9.5
    
    >>> formulas(6, 2, 12, 5280, 0.4, 1.0472)
    8.9
    """
    x = d1 * M.tan(degree)
    l1 = (x ** 2 + d1 ** 2) ** 0.5
    l2 = ((h - x) ** 2 + d2 ** 2) ** 0.5
    t = (l1 + l2 * n) / v_sand
    t = round(t * 3600, 1)
    return t

if __name__ == "__main__":
    doctest.testmod(verbose=True)
    print('\n' + '*' * 10)

d1, d2, h, v_sand, n, degree = get_values()
d1, h, v_sand, degree = trans(d1, h, v_sand, degree)
t = formulas(d1, d2, h, v_sand, n, degree)
print('\nОтвет:', t)