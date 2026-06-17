import doctest as D
import math as M

def read_all(f_name):
    """
    >>> test = read_all('zip_codes_states.csv')
    >>> test[2][0]
    '00601'
    >>> test[6][3]
    'Aguadilla'
    >>> test[10][2]
    -66.698262
    >>> test[15][4]
    'PR'
    >>> test[692][0]
    '02210'
    >>> test[698][0]
    '02222'
    >>> test[700][0]
    '02239'
    >>> test[706][-1]
    'Suffolk'
    """   
    header = []
    zip_data = []
    row = 0

    file = open(f_name, 'r')
    content = file.read().split('\n')
    file.close()

    for line in content:
        if line == '':
            continue
        
        skip = False
        a = line.strip().replace('"', '').split(',')
        row += 1
        
        if row == 1:
            for item in a:
                header.append(item)
        else:
            if len(a) != len(header):
                continue
            
            data = []
            
            for i in range(len(a)):
                if a[i] == '':
                    skip = True
                    break
                elif header[i] == 'latitude' or header[i] == 'longitude':
                    item = float(a[i])
                else:
                    item = a[i]
                data.append(item)
            
            if skip is False:
                zip_data.append(data)
    return zip_data
def command_input():
    command = input("Command ('loc', 'zip', 'dist', 'end') => ")
    while command.lower() not in ['loc', 'zip', 'dist', 'end']:
        print('Invalid command, ignoring')
        command = input("Command ('loc', 'zip', 'dist', 'end') => ")
    print(command)
    return command.lower()
def coordinates(side):
    """
    >>> coordinates(42.673701)
    (42, 40, 25.32)

    >>> coordinates(-74.54525)
    (74, 32, 42.9)

    >>> coordinates(42.343986)
    (42, 20, 38.35)

    >>> coordinates(-73.56733)
    (73, 34, 2.39)
    """
    if side < 0:
        side *= -1
    s1 = int(side // 1)
    s2 = int((side - s1) * 60)
    s3 = round(((side - s1) * 60 - s2) * 60, 4)
    return s1, s2, round(s3, 2)
def loc_go(zip_data):
    zip_code = input('Enter a ZIP Code to lookup => ')
    while len(zip_code) != 5 or zip_code.isdigit() == False:
        print('Invalid command, ignoring')
        zip_code = input('Enter a ZIP Code to lookup => ')
    for item in zip_data:
        if item[0] == zip_code:
            n = item[1]
            w = item[2]
            n1, n2, n3 = coordinates(n)
            w1, w2, w3 = coordinates(w)
            print(zip_code)
            print(f'ZIP Code {zip_code} is in {item[3]}, {item[4]}, {item[5]} county, coordinates: (0{n1}°{n2}\'{n3}"N,0{w1}°{w2}\'{w3}"W)')
            break
    else:
        print('Invalid command, ignoring')
def zip_go(zip_data):

    """
    не понимаю, как написаь тесты, поскольку функция требует ручного ввода

    # >>> test_data = [
    # ...     ['12179', 42.673701, -74.54525, 'Troy', 'NY', 'Rensselaer'],
    # ...     ['12180', 42.728465, -73.69161, 'Troy', 'NY', 'Rensselaer']
    # ... ]
    # >>> zip_go(test_data)
    # Enter a city name to lookup => troy
    # troy
    # Enter the state name to lookup => ny
    # ny
    # The following ZIP Code(s) found for Troy, NY: 12179, 12180

    # >>> test_data = [
    # ...     ['00606', 18.172947, -66.944111, 'Maricao', 'PR', 'Maricao'],
    # ...     ['00610', 18.288685, -67.139696, 'Anasco', 'PR', 'Anasco'],
    # ...     ['00611', 18.279531, -66.80217, 'Angeles', 'PR', 'Utuado'],
    # ...     ['00612', 18.450674, -66.698262, 'Arecibo', 'PR', 'Arecibo'],
    # ...     ['00613', 18.458093, -66.732732, 'Arecibo', 'PR', 'Arecibo'],
    # ...     ['00614', 18.429675, -66.674506, 'Arecibo', 'PR', 'Arecibo'],
    # ...     ['00616', 18.444792, -66.640678, 'Bajadero', 'PR', 'Arecibo'],
    # ...     ['00617', 18.447092, -66.544255, 'Barceloneta', 'PR', 'Barceloneta']
    # ... ]
    # >>> zip_go(test_data)
    # Enter a city name to lookup => AreСibo
    # AreСibo
    # Enter the state name to lookup => pR
    # pR
    # The following ZIP Code(s) found for Arecibo, PR: 00612, 00613, 00614, 00616
    """

    city = input('Enter a city name to lookup => ')
    while not city.isalpha():
        print('Invalid command, ignoring')
        city = input('Enter a city name to lookup => ')
    print(city)
    
    state = input('Enter the state name to lookup => ')
    while not state.isalpha():
        print('Invalid command, ignoring')
        state = input('Enter a state name to lookup => ')
    print(state)

    city, state = city.title(), state.upper()

    codes = []
    for item in zip_data:
        if item[3] == city and item[4] == state:
            codes.append(item[0])
    
    if len(codes) == 0:
        print('Invalid command, ignoring')
    else:
        print(f'The following ZIP Code(s) found for {city}, {state}: {", ".join(codes)}')
def dist_go(zip_data):
    c1 = input('Enter the first ZIP Code => ')
    while c1.isdigit() == False or len(c1) != 5:
        print('Invalid command, ignoring')
        c1 = input('Enter the first ZIP Code => ')
    
    c2 = input('Enter the second ZIP Code => ')
    while c2.isdigit() == False or len(c2) != 5:
        print('Invalid command, ignoring')
        c2 = input('Enter the second ZIP Code => ')

    
    for item1 in zip_data:
        if item1[0] == c1:
            break
    else:
        print('Invalid command, ignoring')
        return
    
    for item2 in zip_data:
        if item2[0] == c2:
            break
    else:
        print('Invalid command, ignoring')
        return
    
    lat1, lon1 = item1[1], item1[2]
    lat2, lon2 = item2[1], item2[2]

    distance = haversine(lat1, lon1, lat2, lon2) * 0.621371  # переводим в мили

    print(f'The distance between {c1} and {c2} is {round(distance, 2)} miles')
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1 = M.radians(lat1)
    lon1 = M.radians(lon1)
    lat2 = M.radians(lat2)
    lon2 = M.radians(lon2)    

    d_lon = lon2 - lon1
    d_lat = lat2 - lat1

    a = M.sin(d_lat / 2) ** 2 + M.cos(lat1) * M.cos(lat2) * (M.sin(d_lon / 2) ** 2)
    c = 2 * M.asin(a ** 0.5)

    return c * R

# if __name__ == "__main__":
#     D.testmod(verbose=True)

zip_data = read_all('zip_codes_states.csv')
while True:
    command = command_input()
    if command == 'loc':
        loc_go(zip_data)
    elif command == 'zip':
        zip_go(zip_data)
    elif command == 'dist':
        dist_go(zip_data)
    elif command == 'end':
        print('Done')
        break