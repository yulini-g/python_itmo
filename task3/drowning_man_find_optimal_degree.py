import math as M
import doctest

def get_values():
    d1 = float(input('Введите кратчайшее расстояние от спасателя до кромки воды в ярдах: '))
    d2 = float(input('Введите кратчайшее расстояние от утопающего до берега в футах: '))
    h = float(input('Введите боковое смещение между спасателем и утопающим в ярдах: '))
    v_sand = float(input('Введите скорость движения спасателя по песку в милях в час: '))
    n = float(input('Введите коэффициент замедления спасателя при движении в воде: '))
    return d1, d2, h, v_sand, n

def trans(d1, h, v_sand):
    return (round(d1 * 3, 4), 
            round(h * 3, 4), 
            round(v_sand * 5280, 4))

def formulas(d1, d2, h, v_sand, n, degree):
    x = d1 * M.tan(degree)
    l1 = (x ** 2 + d1 ** 2) ** 0.5
    l2 = ((h - x) ** 2 + d2 ** 2) ** 0.5
    t = (l1 + l2 * n) / v_sand
    t = round(t * 3600, 1)
    return t

def find_optimal_angle(d1, d2, h, v_sand, n):
    """   
    >>> d1, d2, h, v_sand, n = 8, 10, 50, 5, 2
    >>> d1, h, v_sand = trans(d1, h, v_sand)
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

def analytical_find_optimal_angle(d1, d2, h, n, v_sand):
    """
    Аналитический метод (приближенный)
    tan(θ) = h / (d1 + n * d2)
    
    >>> d1, d2, h, v_sand, n = 8, 10, 50, 5, 2
    >>> d1, h, v_sand = trans(d1, h, v_sand)
    >>> analytical_find_optimal_angle(d1, d2, h, n, v_sand)
    (73.652, 30.4)
    
    >>> analytical_find_optimal_angle(6, 3, 12, 0.5, 2640)
    (63.435, 17.2)
    
    >>> analytical_find_optimal_angle(6, 3, 12, 1, 5280)
    (50.194, 20.4)
    
    >>> analytical_find_optimal_angle(6, 3, 12, 2, 10560)
    (36.253, 13.8)
    
    >>> analytical_find_optimal_angle(3, 1, 6, 0.8, 2640)
    (51.34, 9.9)
    
    >>> analytical_find_optimal_angle(6, 2, 12, 0.4, 5280)
    (68.199, 8.0)
    """
    angle_rad = M.atan(h / (d1 + n * d2))
    degree = round(M.degrees(angle_rad), 3)
    t = formulas(d1, d2, h, v_sand, n, M.radians(degree))
    return round(degree), t

# ================ основная программа ================
if __name__ == "__main__":
      doctest.testmod(verbose=True) 

d1, d2, h, v_sand, n = get_values()
d1, h, v_sand = trans(d1, h, v_sand)
print(find_optimal_angle(d1, d2, h, v_sand, n))
print(analytical_find_optimal_angle(d1, d2, h, n, v_sand))