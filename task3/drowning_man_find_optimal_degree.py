import math as M
import doctest

def get_values():
    d1 = float(input('Введите кратчайшее расстояние между спасателем и кромкой воды, d1 (ярды) => '))
    print(int(d1))
    d2 = float(input('Введите кратчайшее расстояние от утопающего до берега, d2 (футы) => '))
    print(int(d2))
    h = float(input('Введите боковое смещение между спасателем и утопающим, h (ярды) => '))
    print(int(h))
    v_sand = float(input('Введите скорость движения спасателя по песку, v_sand (мили в час) => '))
    print(int(v_sand))
    n = float(input('Введите коэффициент замедления спасателя при движении в воде, n => '))
    print(int(n))
    return d1, d2, h, v_sand, n

def trans(d1, h, v_sand):
    return (round(d1 * 3, 4), 
            round(h * 3, 4), 
            round(v_sand * 5280, 4))

def formulas(d1, d2, h, v_sand, n, angle_rad):
    x = d1 * M.tan(angle_rad)
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
    (57.995, 18.1)
    
    >>> analytical_find_optimal_angle(6, 3, 12, 1, 5280)
    (53.13, 10.2)
    
    >>> analytical_find_optimal_angle(6, 3, 12, 2, 5280)
    (45.0, 14.9)
    
    >>> analytical_find_optimal_angle(3, 1, 6, 0.8, 2640)
    (57.653, 9.4)
    
    >>> analytical_find_optimal_angle(6, 2, 12, 0.4, 5280)
    (60.461, 9.0)
    """
    angle_rad = M.atan(h / (d1 + n * d2))
    degree = round(M.degrees(angle_rad), 3)
    t = formulas(d1, d2, h, v_sand, n, angle_rad)
    return round(degree, 3), round(t, 1)

# ================ основная программа ================
if __name__ == "__main__":
      doctest.testmod(verbose=True) 

d1, d2, h, v_sand, n = get_values()
d1, h, v_sand = trans(d1, h, v_sand)
op_d, op_t = find_optimal_angle(d1, d2, h, v_sand, n)
an_d, an_t = analytical_find_optimal_angle(d1, d2, h, n, v_sand)
print(f"\nРезультаты:")
print(f"  Перебор:       угол = {round(op_d)}°, время = {op_t} сек")
print(f"  Аналитический: угол = {round(an_d)}°, время = {an_t} сек")
print(f"\nРасхождение:")
print(f"  Угол:  {round(abs(op_d - an_d), 2)}°")
print(f"  Время: {round(abs(op_t - an_t), 2)} сек")
