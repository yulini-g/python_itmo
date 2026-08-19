class RatNum:
    @staticmethod 
    def gcd(a, b):
        """
        Возвращает наибольший общий делитель двух целых чисел.
        
        @requires: a и b - целые числа
        @modifies: None
        @effects: Вычисляет НОД через алгоритм Евклида
        @throws: None
        @returns: int - положительный НОД
        
        >>> RatNum.gcd(12, 18)
        6
        >>> RatNum.gcd(24, 36)
        12
        >>> RatNum.gcd(17, 19)
        1
        >>> RatNum.gcd(0, 5)
        5
        >>> RatNum.gcd(5, 0)
        5
        >>> RatNum.gcd(-12, 18)
        6
        >>> RatNum.gcd(12, -18)
        6
        """
        
        a, b = abs(a), abs(b)
        while b:
            a, b = b, a % b
        return a
    
    def __eq__(self, other):
        """
        Проверяет равенство двух RatNum.
        NaN равен только NaN.
        
        @requires: other - любой объект
        @modifies: None
        @effects: Сравнивает числители и знаменатели
        @throws: None
        @returns: bool - True если равны, иначе False
        
        >>> RatNum(1, 2) == RatNum(2, 4)
        True
        >>> RatNum(1, 2) == RatNum(1, 3)
        False
        >>> RatNum(1, 2) == RatNum(-1, -2)
        True
        >>> RatNum(1, 0) == RatNum(0, 0)
        True
        >>> RatNum(1, 0) == RatNum(1, 2)
        False
        >>> RatNum(5, 1) == 5
        False
        >>> RatNum(0, 1) == RatNum(0, 5)
        True
        """
        if isinstance(other, RatNum):
            return self._num == other._num and self._den == other._den
        else:
            return False
    
    def __hash__(self):
        """
        Возвращает хеш-значение для использования в множествах и словарях.
        Равные объекты должны иметь равные хеши.
        
        @requires: None
        @modifies: None
        @effects: Вычисляет хеш от кортежа (_num, _den) или от 'NaN'
        @throws: None
        @returns: int - хеш-значение
        
        >>> hash(RatNum(1, 2)) == hash(RatNum(2, 4))
        True
        >>> hash(RatNum(1, 2)) == hash(RatNum(1, 3))
        False
        >>> hash(RatNum(1, 0)) == hash(RatNum(0, 0))
        True
        >>> hash(RatNum(1, 2)) == hash(RatNum(-1, -2))
        True
        >>> hash(RatNum(1, 0)) == hash(RatNum(1, 2))
        False
        >>> len({RatNum(1, 2), RatNum(2, 4), RatNum(1, 3)})
        2
        >>> RatNum(1, 0) in {RatNum(0, 0), RatNum(1, 2)}
        True
        """
        if self._is_nan:
            return hash('NaN')
        return hash((self._num, self._den))
    
    def __init__(self, num, den):
        """
        Создает новое рациональное число num/den.
        
        Representation fields:
            _num (int): числитель
            _den (int): знаменатель (всегда положительный, кроме NaN)
            _is_nan (bool): True если число - NaN
        
        Representation invariant:
            1. _den > 0 для всех чисел, кроме NaN
            2. Для NaN: _num == 0 и _den == 0
            3. Дробь всегда сокращена (gcd(_num, _den) == 1)
            4. _num и _den - целые числа
        
        Abstraction function:
            AF(num, den) = num/den, если den != 0
            AF(0, 0) = NaN
        
        @requires: num и den - целые числа (int)
        @modifies: Создает новый объект
        @effects: Инициализирует поля объекта
        @throws: ValueError если num или den не являются int
        @returns: None
        
        >>> str(RatNum(1, 2))
        '1/2'
        >>> str(RatNum(6, 8))
        '3/4'
        >>> str(RatNum(1, -2))
        '-1/2'
        >>> str(RatNum(-1, -2))
        '1/2'
        >>> str(RatNum(5, 1))
        '5'
        >>> str(RatNum(1, 0))
        'NaN'
        >>> str(RatNum(0, 0))
        'NaN'
        """
        
        if isinstance(num, int) and isinstance(den, int):
            if den == 0:
                self._num = 0
                self._den = 0
                self._is_nan = True
                return
            else:
                self._is_nan = False
            if den < 0:
                num, den = -num, -den
                    
            g = RatNum.gcd(num, den)
            
            self._num = num // g
            self._den = den // g
        else:
            raise ValueError('Ошибка: оба числа должны быть целыми!')
    
    def is_nan(self):
        """
        Возвращает True, если число - NaN.
        
        @requires: None
        @modifies: None
        @effects: Проверяет флаг _is_nan
        @throws: None
        @returns: bool - True если NaN, иначе False
        
        >>> RatNum(1, 2).is_nan()
        False
        >>> RatNum(0, 1).is_nan()
        False
        >>> RatNum(-3, 4).is_nan()
        False
        >>> RatNum(5, 1).is_nan()
        False
        >>> RatNum(1, 0).is_nan()
        True
        >>> RatNum(0, 0).is_nan()
        True
        >>> RatNum(-1, 0).is_nan()
        True
        """
        return self._is_nan
     
    def is_positive(self):
        """
        Возвращает True, если число положительное.
        NaN считается положительным (по условию).
        
        @requires: None
        @modifies: None
        @effects: Проверяет числитель на > 0
        @throws: None
        @returns: bool - True если положительное или NaN
        
        >>> RatNum(1, 2).is_positive()
        True
        >>> RatNum(-3, 4).is_positive()
        False
        >>> RatNum(0, 1).is_positive()
        False
        >>> RatNum(5, 1).is_positive()
        True
        >>> RatNum(1, -2).is_positive()
        False
        >>> RatNum(-1, -2).is_positive()
        True
        >>> RatNum(1, 0).is_positive()
        True
        """
        if self._is_nan:
            return True
        return self._num > 0
        
    def is_negative(self):
        """
        Возвращает True, если число отрицательное.
        NaN не считается отрицательным (по условию).
        
        @requires: None
        @modifies: None
        @effects: Проверяет числитель на < 0
        @throws: None
        @returns: bool - True если отрицательное
        
        >>> RatNum(1, 2).is_negative()
        False
        >>> RatNum(-3, 4).is_negative()
        True
        >>> RatNum(0, 1).is_negative()
        False
        >>> RatNum(5, 1).is_negative()
        False
        >>> RatNum(1, -2).is_negative()
        True
        >>> RatNum(-1, -2).is_negative()
        False
        >>> RatNum(1, 0).is_negative()
        False
        """
        if self._is_nan:
            return False
        return self._num < 0
    
    def float_value(self):
        """
        Возвращает значение дроби как float.
        
        @requires: None
        @modifies: None
        @effects: Вычисляет значение num/den как float
        @throws: None
        @returns: float - значение дроби, или float('nan') для NaN
        
        >>> RatNum(1, 2).float_value()
        0.5
        >>> RatNum(3, 4).float_value()
        0.75
        >>> RatNum(5, 1).float_value()
        5.0
        >>> RatNum(-1, 2).float_value()
        -0.5
        >>> RatNum(1, -2).float_value()
        -0.5
        >>> RatNum(0, 1).float_value()
        0.0
        >>> RatNum(1, 0).float_value()
        nan
        """
        if self.is_nan():
            return float('nan')
        return self._num / self._den
    
    def int_value(self):
        """
        Возвращает целую часть дроби (округление вниз).
        
        @requires: None
        @modifies: None
        @effects: Вычисляет целую часть от num/den
        @throws: None
        @returns: int - целая часть, или 0 для NaN
        
        >>> RatNum(5, 2).int_value()
        2
        >>> RatNum(3, 4).int_value()
        0
        >>> RatNum(7, 3).int_value()
        2
        >>> RatNum(-5, 2).int_value()
        -3
        >>> RatNum(-3, 4).int_value()
        -1
        >>> RatNum(0, 1).int_value()
        0
        >>> RatNum(1, 0).int_value()
        0
        """
        if self.is_nan():
            return 0
        return self._num // self._den
    
    def __str__(self):
        """
        Возвращает строковое представление RatNum.
        
        @requires: None
        @modifies: None
        @effects: Форматирует строку для вывода
        @throws: None
        @returns: str - "NaN", "5" или "3/4"
        
        >>> str(RatNum(1, 2))
        '1/2'
        >>> str(RatNum(6, 8))
        '3/4'
        >>> str(RatNum(5, 1))
        '5'
        >>> str(RatNum(1, 0))
        'NaN'
        >>> str(RatNum(-3, 4))
        '-3/4'
        >>> str(RatNum(0, 1))
        '0'
        >>> str(RatNum(1, -2))
        '-1/2'
        """
        if self.is_nan():
            return 'NaN'
        if self._den == 1:
            return str(self._num)
        return f'{self._num}/{self._den}'
    
    def __add__(self, other):
        """
        Возвращает сумму двух RatNum.
        
        @requires: other - экземпляр RatNum
        @modifies: None
        @effects: Вычисляет (self + other) по формуле a/b + c/d = (ad + bc)/bd
        @throws: None
        @returns: RatNum - результат сложения, или NaN если любой операнд NaN
        
        >>> str(RatNum(1, 2) + RatNum(1, 3))
        '5/6'
        >>> str(RatNum(1, 4) + RatNum(1, 4))
        '1/2'
        >>> str(RatNum(1, 2) + RatNum(-1, 2))
        '0'
        >>> str(RatNum(3, 4) + RatNum(1, 4))
        '1'
        >>> str(RatNum(1, 2) + RatNum(1, 0))
        'NaN'
        >>> str(RatNum(1, 0) + RatNum(0, 0))
        'NaN'
        >>> str(RatNum(1, 3) + RatNum(2, 3))
        '1'
        """
        if self.is_nan() or other.is_nan():
            return RatNum(0, 0)
        
        num_1, num_2 = self._num * other._den, other._num * self._den
        return RatNum(num_1 + num_2, self._den * other._den)
    
    def __sub__(self, other):
        """
        Возвращает разность двух RatNum.
        
        @requires: other - экземпляр RatNum
        @modifies: None
        @effects: Вычисляет (self - other) по формуле a/b - c/d = (ad - bc)/bd
        @throws: None
        @returns: RatNum - результат вычитания, или NaN если любой операнд NaN
        
        >>> str(RatNum(1, 2) - RatNum(1, 3))
        '1/6'
        >>> str(RatNum(1, 2) - RatNum(-1, 2))
        '1'
        >>> str(RatNum(3, 4) - RatNum(1, 4))
        '1/2'
        >>> str(RatNum(1, 2) - RatNum(1, 0))
        'NaN'
        >>> str(RatNum(1, 0) - RatNum(1, 2))
        'NaN'
        >>> str(RatNum(1, 0) - RatNum(0, 0))
        'NaN'
        >>> str(RatNum(5, 1) - RatNum(3, 1))
        '2'
        """
        if self.is_nan() or other.is_nan():
            return RatNum(0, 0) 
        
        num_1, num_2 = self._num * other._den, other._num * self._den
        return RatNum(num_1 - num_2, self._den * other._den)
    
    def __neg__(self):
        """
        Возвращает аддитивную инверсию (self * -1).
        
        @requires: None
        @modifies: None
        @effects: Меняет знак числителя
        @throws: None
        @returns: RatNum - новый объект с противоположным знаком
        
        >>> str(-RatNum(1, 2))
        '-1/2'
        >>> str(-RatNum(-3, 4))
        '3/4'
        >>> str(-RatNum(5, 1))
        '-5'
        >>> str(-RatNum(0, 1))
        '0'
        >>> str(-RatNum(1, -2))
        '1/2'
        >>> str(-RatNum(-1, -2))
        '-1/2'
        >>> str(-RatNum(1, 0))
        'NaN'
        """
        if self.is_nan():
            return self
        return RatNum(-self._num, self._den)   
    
    def __mul__(self, other):
        """
        Возвращает произведение двух RatNum.
        
        @requires: other - экземпляр RatNum
        @modifies: None
        @effects: Вычисляет (self * other) по формуле (a/b) * (c/d) = ac/bd
        @throws: None
        @returns: RatNum - результат умножения, или NaN если любой операнд NaN
        
        >>> str(RatNum(1, 2) * RatNum(2, 3))
        '1/3'
        >>> str(RatNum(1, 2) * RatNum(-1, 2))
        '-1/4'
        >>> str(RatNum(0, 1) * RatNum(5, 1))
        '0'
        >>> str(RatNum(3, 4) * RatNum(4, 3))
        '1'
        >>> str(RatNum(1, 2) * RatNum(1, 0))
        'NaN'
        >>> str(RatNum(1, 0) * RatNum(0, 0))
        'NaN'
        >>> str(RatNum(-2, 3) * RatNum(3, 4))
        '-1/2'
        """
        if self.is_nan() or other.is_nan():
            return RatNum(0, 0)  
        return RatNum(self._num * other._num, self._den * other._den)
    
    def __truediv__(self, other):
        """
        Возвращает частное двух RatNum.
        
        @requires: other - экземпляр RatNum
        @modifies: None
        @effects: Вычисляет (self / other) по формуле (a/b) / (c/d) = ad/bc
        @throws: None
        @returns: RatNum - результат деления, или NaN если:
                - любой операнд NaN
                - other == 0 (деление на ноль)
        
        >>> print(RatNum(1, 2) / RatNum(2, 3))
        3/4
        >>> print(RatNum(1, 2) / RatNum(-1, 2))
        -1
        >>> print(RatNum(0, 1) / RatNum(5, 1))
        0
        >>> print(RatNum(3, 4) / RatNum(3, 4))
        1
        >>> print(RatNum(1, 2) / RatNum(0, 1))
        NaN
        >>> print(RatNum(1, 0) / RatNum(1, 2))
        NaN
        >>> print(RatNum(1, 2) / RatNum(1, 0))
        NaN
        """
        if self.is_nan() or other.is_nan() or other._num == 0:
            return RatNum(0, 0)
        return RatNum(self._num * other._den, other._num * self._den)
    
    def compare_to(self, other):
        """
        Сравнивает два RatNum.
        NaN считается больше любого числа.
        
        @requires: other - экземпляр RatNum
        @modifies: None
        @effects: Сравнивает два рациональных числа
        @throws: None
        @returns: int - 1 если self > other, 0 если равны, -1 если self < other
        
        >>> RatNum(1, 2).compare_to(RatNum(1, 3))
        1
        >>> RatNum(1, 3).compare_to(RatNum(1, 2))
        -1
        >>> RatNum(1, 2).compare_to(RatNum(2, 4))
        0
        >>> RatNum(1, 0).compare_to(RatNum(1, 2))
        1
        >>> RatNum(1, 2).compare_to(RatNum(1, 0))
        -1
        >>> RatNum(1, 0).compare_to(RatNum(0, 0))
        0
        >>> RatNum(-3, 4).compare_to(RatNum(1, 2))
        -1
        """
        if self.is_nan() and other.is_nan():
            return 0
        if self.is_nan():
            return 1
        if other.is_nan():
            return -1
        
        if self._num * other._den > other._num * self._den:
            return 1
        elif self._num * other._den < other._num * self._den:
            return -1
        else:
            return 0

class RatPoly:
    def __init__(self, coeffs):
        if not isinstance(coeffs, list):
            raise TypeError('Ошибка: передан не список!')
        
        rat_coeffs = []
        for c in coeffs:
            if isinstance(c, RatNum):
                rat_coeffs.append(c)
            elif isinstance(c, int):
                rat_coeffs.append(RatNum(c, 1))
            else:
                raise TypeError(f'Ошибка: {c} не является числом или RatNum!')
            
        self._is_nan = False
        for c in rat_coeffs:
            if c.is_nan():
                self._is_nan = True
                
        while len(rat_coeffs) > 1 and rat_coeffs[-1] == RatNum(0, 1):
            rat_coeffs.pop()
            
        if not rat_coeffs:
            rat_coeffs = [RatNum(0, 1)]
            
        self._coeffs = rat_coeffs
        
    def degree(self):
        """
        Возвращает степень полинома.
        
        @requires: None
        @modifies: None
        @effects: Вычисляет степень
        @throws: None
        @returns: int - степень полинома (0 для нулевого полинома)
        
        >>> RatPoly([1, 2, 3]).degree()
        2
        >>> RatPoly([5]).degree()
        0
        >>> RatPoly([0]).degree()
        0
        >>> RatPoly([0, 0, 0]).degree()
        0
        """
        return len(self._coeffs) - 1
    
    def is_nan(self):
        """
        Возвращает True, если полином содержит NaN.
        
        @requires: None
        @modifies: None
        @effects: Проверяет флаг _is_nan
        @throws: None
        @returns: bool - True если есть NaN коэффициент
        
        >>> RatPoly([1, 2]).is_nan()
        False
        >>> RatPoly([RatNum(1, 0), 2]).is_nan()
        True
        """
        return self._is_nan
    
    def __str__(self):
        """
        Возвращает строковое представление полинома.
        
        @requires: None
        @modifies: None
        @effects: Форматирует полином в строку
        @throws: None
        @returns: str - "0", "5", "2x + 1" или "3x^2 + 2x + 1"
        
        >>> str(RatPoly([1, 2, 3]))
        '3x^2 + 2x + 1'
        >>> str(RatPoly([5]))
        '5'
        >>> str(RatPoly([0]))
        '0'
        >>> str(RatPoly([0, 0, 0]))
        '0'
        >>> str(RatPoly([RatNum(1, 2), RatNum(3, 4)]))
        '3/4x + 1/2'
        """
        if self.is_nan():
            return 'NaN'
        
        base = []
        for i, coeff in enumerate(self._coeffs):
            if coeff  == RatNum(0, 1):
                continue
            
            if i == 0:
                base.append(str(coeff))
            elif i == 1:
                if coeff == RatNum(1, 1):
                    base.append('x')
                elif coeff == RatNum(-1, 1):
                    base.append('-x')
                else:
                    base.append(f'{coeff}x')
            else:
                if coeff == RatNum(1,1):
                    base.append(f'x^{i}')   
                elif coeff == RatNum(-1, 1):
                    base.append(f'-x^{i}')
                else:
                    base.append(f'{coeff}x^{i}')
                    
        if not base:
            return '0'
        
        base.reverse()
        
        result = base[0]
        for b in base[1:]:
            if b[0] == '-':
                result += f' - {b[1:]}'
            else:
                result += f' + {b}'
                
        return result
    
    def get_coeff(self, degree):
        """
        Возвращает коэффициент при x^degree.
        
        @requires: degree - неотрицательное целое число
        @modifies: None
        @effects: Находит коэффициент по индексу
        @throws: None
        @returns: RatNum - коэффициент, или 0 если степень больше степени полинома
        
        >>> str(RatPoly([1, 2, 3]).get_coeff(2))
        '3'
        >>> str(RatPoly([1, 2, 3]).get_coeff(5))
        '0'
        >>> str(RatPoly([1, 2, 3]).get_coeff(0))
        '1'
        """
        if degree < 0:
            raise ValueError('Ошибка: степень не может быть отрицательной!')
        
        if degree >= len(self._coeffs):
            return RatNum(0, 1)
        
        return self._coeffs[degree]
    
    def scale_coeff(self, scalar):
        """
        Умножает все коэффициенты на scalar.
        
        @requires: scalar - RatNum или число
        @modifies: None (создает новый объект)
        @effects: Умножает все коэффициенты на scalar
        @throws: None
        @returns: RatPoly - новый полином
        
        >>> str(RatPoly([1, 2]).scale_coeff(2))
        '4x + 2'
        >>> str(RatPoly([1, 2]).scale_coeff(RatNum(1, 2)))
        'x + 1/2'
        >>> str(RatPoly([1, 2, 3]).scale_coeff(2))
        '6x^2 + 4x + 2'
        >>> str(RatPoly([1, 2, 3]).scale_coeff(RatNum(1, 2)))
        '3/2x^2 + x + 1/2'
        >>> str(RatPoly([0]).scale_coeff(5))
        '0'
        >>> str(RatPoly([RatNum(1, 0)]).scale_coeff(2))
        'NaN'
        """
        if not isinstance(scalar, int) and not isinstance(scalar, RatNum):
            raise TypeError('Ошибка: недопустимое значение!')
        
        if isinstance(scalar, int):
            scalar = RatNum(scalar, 1)
        
        new_coeffs = []
        for c in self._coeffs:
            new_coeffs.append(c * scalar)
            
        return RatPoly(new_coeffs)
    
    def __neg__(self):
        """
        Возвращает аддитивную инверсию полинома.
        
        @requires: None
        @modifies: None
        @effects: Меняет знак всех коэффициентов
        @throws: None
        @returns: RatPoly - новый полином с противоположными знаками
        
        >>> str(-RatPoly([1, 2, 3]))
        '-3x^2 - 2x - 1'
        >>> str(-RatPoly([5]))
        '-5'
        >>> str(-RatPoly([0]))
        '0'
        """
        if self.is_nan():
            return self
        
        new = []
        for c in self._coeffs:
            new.append(-c)
            
        return RatPoly(new)
    
    def __add__(self, other):
        """
        Возвращает сумму двух полиномов.
        
        @requires: other - экземпляр RatPoly
        @modifies: None
        @effects: Складывает соответствующие коэффициенты
        @throws: TypeError если other не RatPoly
        @returns: RatPoly - результат сложения
        
        >>> str(RatPoly([1, 2]) + RatPoly([3, 4]))
        '6x + 4'
        >>> str(RatPoly([1, 2, 3]) + RatPoly([1, 2]))
        '3x^2 + 4x + 2'
        >>> str(RatPoly([5]) + RatPoly([3]))
        '8'
        """
        if not isinstance(other, RatPoly):
            raise TypeError('Ошибка: other должен быть RatPoly!')
        
        if self.is_nan() or other.is_nan():
            return RatPoly([RatNum(0, 0)])
        
        result = []
        max_len = max(len(self._coeffs), len(other._coeffs))
        
        for i in range(max_len):
            a = self.get_coeff(i)
            b = other.get_coeff(i)
            result.append(a + b)
            
        return RatPoly(result)
    
    def __sub__(self, other):
        """
        Возвращает разность двух полиномов.
        
        @requires: other - экземпляр RatPoly
        @modifies: None
        @effects: Вычитает соответствующие коэффициенты
        @throws: TypeError если other не RatPoly
        @returns: RatPoly - результат вычитания
        
        >>> str(RatPoly([1, 2]) - RatPoly([3, 4]))
        '-2x - 2'
        >>> str(RatPoly([1, 2, 3]) - RatPoly([1, 2]))
        '3x^2'
        >>> str(RatPoly([1, 3, 3]) - RatPoly([1, 2]))
        '3x^2 + x'
        >>> str(RatPoly([1, 2, 3, 4]) - RatPoly([1, 2]))
        '4x^3 + 3x^2'
        >>> str(RatPoly([1, 2, 3]) - RatPoly([1, 5]))
        '3x^2 - 3x'
        >>> str(RatPoly([1, 2, 3]) - RatPoly([1, 2, 3]))
        '0'
        >>> str(RatPoly([1, 2]) - RatPoly([1, 2, 3]))
        '-3x^2'
        """
        if not isinstance(other, RatPoly):
            raise TypeError('Ошибка: other должен быть RatPoly!')
        
        if self.is_nan() or other.is_nan():
            return RatPoly([RatNum(0, 0)])
        
        return self + (-other)
    
    def __mul__(self, other):
        """
        Возвращает произведение двух полиномов.
        
        @requires: other - экземпляр RatPoly
        @modifies: None
        @effects: Умножает полиномы
        @throws: TypeError если other не RatPoly
        @returns: RatPoly - результат умножения
        
        >>> str(RatPoly([1, 2]) * RatPoly([3, 4]))
        '8x^2 + 10x + 3'
        >>> str(RatPoly([1, 1]) * RatPoly([1, -1]))
        '-x^2 + 1'
        """
        if not isinstance(other, RatPoly):
            raise TypeError('Ошибка: other должен быть RatPoly!')
        
        if self.is_nan() or other.is_nan():
            return RatPoly([RatNum(0, 0)])
                
        result_len = len(self._coeffs) + len(other._coeffs) - 1
        result = [RatNum(0, 1) for _ in range(result_len)]
        
        for i, a in enumerate(self._coeffs):
            for j, b in enumerate(other._coeffs):
                result[i + j] = (a * b) + result[i + j]
                
        return RatPoly(result)
    
    def __truediv__(self, other):
        """
        Возвращает частное двух полиномов.
        
        @requires: other - экземпляр RatPoly
        @modifies: None
        @effects: Делит полиномы
        @throws: TypeError если other не RatPoly
        @returns: RatPoly - результат деления
        
        >>> str(RatPoly([1, 2, 1]) / RatPoly([1, 1]))
        'x + 1'
        """
        if not isinstance(other, RatPoly):
            raise TypeError('Ошибка: other должен быть RatPoly!')
        
        if (self.is_nan() or 
            other.is_nan() or
            (other.degree() == 0 and
             other.get_coeff(0) == RatNum(0, 1))):
            return RatPoly([RatNum(0, 0)])
        
        if self.degree() < other.degree():
            return RatPoly([RatNum(0, 1)])
        
        base = [RatNum(0, 1)] * (self.degree() - other.degree() + 1)
        remain = self._coeffs.copy()
        
        for i in range(len(base) - 1, -1, -1):
            coeff = remain[i + other.degree()] / other._coeffs[-1]
            base[i] = coeff
            
            for j in range(other.degree() + 1):
                remain[i + j] = remain[i + j] - (coeff * other._coeffs[j])
                
        return RatPoly(base)
    
    def eval(self, dot):
        """
        Вычисляет значение полинома в точке dot.
        
        @requires: dot - RatNum или int
        @modifies: None
        @effects: Подставляет dot в полином по схеме Горнера
        @throws: TypeError если dot не RatNum или int
        @returns: RatNum - значение полинома в точке
        
        >>> RatPoly([1, 2, 3]).eval(2) == RatNum(17, 1)
        True
        >>> RatPoly([1, 2, 3]).eval(RatNum(1, 2)) == RatNum(11, 4)
        True
        >>> RatPoly([5]).eval(10) == RatNum(5, 1)
        True
        >>> RatPoly([0]).eval(5) == RatNum(0, 1)
        True
        >>> RatPoly([RatNum(1, 0)]).eval(2) == RatNum(0, 0)
        True
        """
        if not isinstance(dot, RatNum) and not isinstance(dot, int):
            raise TypeError('Ошибка: dot должен быть RatNum или int!')
        
        if isinstance(dot, int):
            dot = RatNum(dot, 1)
            
        if self.is_nan():
            return RatNum(0, 0)
        
        result = RatNum(0, 1)
        for coeff in reversed(self._coeffs):
            result = result * dot + coeff
            
        return result
    
    def differentiate(self):
        """
        Возвращает производную полинома.
        
        @requires: None
        @modifies: None
        @effects: Вычисляет производную по правилу (a*x^n)' = a*n*x^(n-1)
        @throws: None
        @returns: RatPoly - производная
        
        >>> str(RatPoly([1, 2, 3]).differentiate())
        '6x + 2'
        >>> str(RatPoly([5]).differentiate())
        '0'
        >>> str(RatPoly([1, 2, 3, 4]).differentiate())
        '12x^2 + 6x + 2'
        >>> str(RatPoly([RatNum(1, 2), RatNum(3, 4)]).differentiate())
        '3/4'
        """
        if self.is_nan():
            return self
        
        if self.degree() == 0:
            return RatPoly([RatNum(0, 1)])
        
        result = []
        for i in range(1, len(self._coeffs)):
            new = self._coeffs[i] * RatNum(i, 1)
            result.append(new)
            
        return RatPoly(result)
    
    def anti_differentiate(self):
        """
        Возвращает неопределенный интеграл полинома (без константы).
        
        @requires: None
        @modifies: None
        @effects: Интегрирует по правилу ∫a*x^n dx = a/(n+1)*x^(n+1)
        @throws: None
        @returns: RatPoly - интеграл (константа = 0)
        
        >>> str(RatPoly([1, 2, 3]).anti_differentiate())
        'x^3 + x^2 + x'
        >>> str(RatPoly([5]).anti_differentiate())
        '5x'
        >>> str(RatPoly([RatNum(1, 2), RatNum(3, 4)]).anti_differentiate())
        '3/8x^2 + 1/2x'
        """
        if self.is_nan():
            return self
        
        new_coeffs = [RatNum(0, 1)]
        for i in range(len(self._coeffs)):
            new_coeffs.append(self._coeffs[i] / RatNum(i + 1, 1))
        
        return RatPoly(new_coeffs)
    
    def integrate(self, a, b):
        """
        Возвращает определенный интеграл от a до b.
        
        @requires: a, b - RatNum или int
        @modifies: None
        @effects: Вычисляет ∫[a,b] P(x) dx = F(b) - F(a)
        @throws: TypeError если a или b не RatNum или int
        @returns: RatNum - значение интеграла
        
        >>> RatPoly([1, 2]).integrate(0, 1) == RatNum(2, 1)
        True
        >>> RatPoly([1, 2, 3]).integrate(0, 1) == RatNum(3, 1)
        True
        >>> RatPoly([5]).integrate(1, 3) == RatNum(10, 1)
        True
        """
        if isinstance(a, int):
            a = RatNum(a, 1)
        if isinstance(b, int):
            b = RatNum(b, 1)
        
        if not isinstance(a, RatNum) or not isinstance(b, RatNum):
            raise TypeError('a и b должны быть RatNum или int')
        
        if self.is_nan():
            return RatNum(0, 0)
        
        antiderivative = self.anti_differentiate()
        return antiderivative.eval(b) - antiderivative.eval(a)
    
    def value_of(self, x):
        """
        Аналог eval() - вычисляет значение полинома в точке x.
        
        @requires: x - RatNum или int
        @modifies: None
        @effects: Подставляет x в полином
        @throws: TypeError если x не RatNum или int
        @returns: RatNum - значение полинома в точке
        
        >>> RatPoly([1, 2, 3]).value_of(2) == RatNum(17, 1)
        True
        """
        return self.eval(x)
    
    def __eq__(self, other):
        """
        Проверяет равенство двух полиномов.
        
        @requires: other - любой объект
        @modifies: None
        @effects: Сравнивает коэффициенты
        @throws: None
        @returns: bool - True если равны
        
        >>> RatPoly([1, 2, 3]) == RatPoly([1, 2, 3])
        True
        >>> RatPoly([1, 2, 3]) == RatPoly([1, 2])
        False
        >>> RatPoly([1, 2, 3]) == RatPoly([1, 2, 3, 0])
        True
        >>> RatPoly([0]) == RatPoly([])
        True
        """
        if not isinstance(other, RatPoly):
            return False
        
        if self.is_nan() or other.is_nan():
            return self.is_nan() == other.is_nan()

        coeffs1 = self._coeffs.copy()
        coeffs2 = other._coeffs.copy()
        
        while len(coeffs1) > 1 and coeffs1[-1] == RatNum(0, 1):
            coeffs1.pop()
        while len(coeffs2) > 1 and coeffs2[-1] == RatNum(0, 1):
            coeffs2.pop()
        
        return coeffs1 == coeffs2
    
    def __hash__(self):
        """
        Возвращает хеш-значение полинома.
        
        @requires: None
        @modifies: None
        @effects: Вычисляет хеш от кортежа коэффициентов
        @throws: None
        @returns: int - хеш-значение
        
        >>> hash(RatPoly([1, 2])) == hash(RatPoly([1, 2]))
        True
        >>> hash(RatPoly([1, 2])) == hash(RatPoly([1, 2, 0]))
        True
        """
        if self.is_nan():
            return hash('NaN')
        
        coeffs = self._coeffs.copy()
        while len(coeffs) > 1 and coeffs[-1] == RatNum(0, 1):
            coeffs.pop()
        
        return hash(tuple(coeffs))

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
