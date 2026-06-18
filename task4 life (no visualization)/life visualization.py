from PIL import Image as I, ImageDraw as ID
import random as R

def start(size, fill):
    field = []
    field = create_field(size, fill, field)

    ages = []
    for y in range(size):
        row = []
        for x in range(size):
            if field[y][x] == 1:
                row.append(1)
            else:
                row.append(0)
        ages.append(row)
    return field, ages

def field_filler(field):
    """
    добавляет одну живую клетку в случайное место
    
    >>> field = [[0,0,0],[0,0,0],[0,0,0]]
    >>> result = field_filler(field)
    >>> sum(sum(row) for row in result)
    1
    
    >>> field = [[1,1,1],[1,1,1],[1,1,1]]
    >>> result = field_filler(field)
    >>> sum(sum(row) for row in result)
    9
    
    >>> field = [[1,0,0],[0,0,0],[0,0,0]]
    >>> result = field_filler(field)
    >>> sum(sum(row) for row in result) >= 1
    True
    """
    has_empty = any(0 in row for row in field)
    if not has_empty:
        return field  # если все заняты, возвращаем поле без изменений

    x, y = R.randint(0, size - 1), R.randint(0, size - 1)
    if field[y][x] == 0:
        field[y][x] = 1
    else:
        field_filler(field)
    return field

def create_field(size, fill, field):
    """
    создает поле size x size с fill% живых клеток.
    
    >>> field = []
    >>> create_field(3, 0, field)
    [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    
    >>> field = []
    >>> create_field(3, 100, field)
    [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    
    >>> field = []
    >>> result = create_field(3, 50, field)
    >>> sum(sum(row) for row in result)
    4
    """
    for _ in range(size):
        row = []
        for _ in range(size):
            row.append(0)
        field.append(row)

    for _ in range(int(size ** 2 * fill / 100)):
        field = field_filler(field)
    return field

def neighbors(x, y, field):
    """
    подсчитывает количество живых соседей для клетки (x, y).
    
    >>> field = [[0,1,0], [1,1,1], [0,1,0]]
    >>> neighbors(1, 1, field)
    4
    >>> neighbors(0, 0, field)
    3
    >>> neighbors(0, 1, field)
    3
    >>> neighbors(2, 2, field)
    3
    >>> neighbors(1, 0, field)
    3
    >>> neighbors(0, 2, field)
    3
    
    >>> empty = [[0,0,0], [0,0,0], [0,0,0]]
    >>> neighbors(1, 1, empty)
    0
    
    >>> single = [[0,0,0], [0,1,0], [0,0,0]]
    >>> neighbors(1, 1, single)
    0
    
    >>> line = [[1,1,1], [0,0,0], [0,0,0]]
    >>> neighbors(1, 0, line)
    2
    >>> neighbors(0, 0, line)
    1
    """
    count = 0
    for neigh_y in range(-1, 2):
        for neigh_x in range(-1, 2):
            if neigh_y == 0 and neigh_x == 0:
                continue
            new_y = y + neigh_y
            new_x = x + neigh_x
            if 0 <= new_y < size and 0 <= new_x < size:
                count += field[new_y][new_x]
    return count

def update(field, ages):
    """
    обновляет поле на одно поколение.
    
    >>> field = [[0,1,0], [0,1,0], [0,1,0]]
    >>> ages = [[0,1,0], [0,2,0], [0,3,0]]
    >>> result = update(field, ages)
    >>> result
    [[0, 0, 0], [1, 1, 1], [0, 0, 0]]
    
    >>> field = [[1,1,0], [1,1,0], [0,0,0]]
    >>> ages = [[1,1,0], [1,1,0], [0,0,0]]
    >>> update(field, ages)
    [[1, 1, 0], [1, 1, 0], [0, 0, 0]]
    
    >>> field = [[0,0,0], [1,1,1], [0,0,0]]
    >>> ages = [[0,0,0], [1,2,1], [0,0,0]]
    >>> update(field, ages)
    [[0, 1, 0], [0, 1, 0], [0, 1, 0]]
    
    >>> field = [[0,0,0], [0,1,0], [0,0,0]]
    >>> ages = [[0,0,0], [0,1,0], [0,0,0]]
    >>> update(field, ages)
    [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    
    >>> field = [[1,1,0], [1,0,0], [0,0,0]]
    >>> ages = [[1,1,0], [1,0,0], [0,0,0]]
    >>> update(field, ages)
    [[1, 1, 0], [1, 1, 0], [0, 0, 0]]
    
    >>> field = [[1,0,0], [0,0,0], [0,0,0]]
    >>> ages = [[6,0,0], [0,0,0], [0,0,0]]
    >>> update(field, ages)
    [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    """
    new_field = []
    for y in range(size):
        row = []
        for x in range(size):
            n = neighbors(x, y, field)
            if ages[y][x] <= 5:
                if field[y][x] == 1 and (n == 2 or n == 3):
                    row.append(1)
                elif field[y][x] == 0 and n == 3:
                    row.append(1)
                else:
                    row.append(0)
            else:
                row.append(0)
        new_field.append(row)
    return new_field

def set_age(ages, field):
    """
    обновляет возраст клеток.

    >>> ages = [[1,2,0], [3,4,0], [0,0,0]]
    >>> field = [[1,0,0], [1,1,0], [0,0,0]]
    >>> set_age(ages, field)
    [[2, 0, 0], [4, 5, 0], [0, 0, 0]]
    
    >>> ages = [[5,0,0], [0,5,0], [0,0,0]]
    >>> field = [[1,0,0], [0,1,0], [0,0,0]]
    >>> set_age(ages, field)
    [[6, 0, 0], [0, 6, 0], [0, 0, 0]]
    
    >>> ages = [[6,0,0], [0,0,0], [0,0,0]]
    >>> field = [[1,0,0], [0,0,0], [0,0,0]]
    >>> set_age(ages, field)
    [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    
    >>> ages = [[1,2,3], [4,5,6], [7,8,9]]
    >>> field = [[0,0,0], [0,0,0], [0,0,0]]
    >>> set_age(ages, field)
    [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    
    >>> ages = [[1,2,3], [4,5,0], [0,0,0]]
    >>> field = [[1,0,1], [0,1,0], [0,0,0]]
    >>> set_age(ages, field)
    [[2, 0, 4], [0, 6, 0], [0, 0, 0]]
    """
    new_ages = []
    for y in range(size):
        row = []
        for x in range(size):
            if field[y][x] == 1:
                if ages[y][x] <= 5:
                    row.append(ages[y][x] + 1)
                else:
                    row.append(0)
            else:
                row.append(0)

        new_ages.append(row)
    return new_ages

# ================== ВИЗУАЛИЗАЦИЯ =========================

def draw_field(colors, size, ages, img_size, pixel_size):

    img = I.new('RGB', (img_size, img_size))
    brush = ID.Draw(img)

    for y in range(size):
        for x in range(size):
            if ages[y][x] != 0 and ages[y][x] != 6:

                color_index = ages[y][x]
                color = colors[color_index - 1]

                x1, x2 = x * pixel_size, (x + 1) * pixel_size
                y1, y2 = y * pixel_size, (y + 1) * pixel_size

                brush.rectangle([x1, y1, x2, y2], fill = color)
            else:
                continue
    return img

#====================== ТЕСТИРОВАНИЕ ======================

# if __name__ == "__main__":
#     size = 3
#     import doctest
#     doctest.testmod(verbose=True)

# ================== ОСНОВНАЯ ПРОГРАММА ===================

f = open(r"start.txt")
f = f.read().split('\n')
size = int(f[0][f[0].find(':') + 2:])  # размер поля
fill = int(f[1][f[1].find(':') + 2:])  # процент живых клеток в начале
gens = int(f[2][f[2].find(':') + 2:])  # количество поколений

colors = [
    (255, 255, 255),  # 0 - белый
    (200, 200, 200),  # 1 - светло-серый
    (150, 150, 150),  # 2 - средний серый
    (100, 100, 100),  # 3 - темно-серый
    (60, 60, 60)]     # 4 - почти черный

pixel_size = 20               # размер кисти
img_size = pixel_size * size  # размер холста

field, ages = start(size, fill)

gif_frames = []
for i in range(gens):
    field = update(field, ages)
    ages = set_age(ages, field)
    img = draw_field(colors, size, ages, img_size, pixel_size)
    gif_frames.append(img)

    # img.save(f'life_{i + 1}.png')

gif_frames[0].save('life.gif',
                   save_all = True,
                   append_images = gif_frames[1:],
                   duration = 500) 
print('GIF создан успешно!')

