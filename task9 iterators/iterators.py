class Fibo:
    """
    Итератор чисел Фибоначчи.

    >>> f = Fibo()
    >>> next(f)
    0
    >>> next(f)
    1
    >>> next(f)
    1
    >>> next(f)
    2
    >>> next(f)
    3
    >>> next(f)
    5
    """
    
    def __init__(self):
        self.a = 0
        self.b = 1
    
    def __iter__(self):
        return self
    
    def __next__(self):
        result = self.a
        self.a, self.b = self.b, self.a + self.b
        return result
    
def integers():
    """
    Генератор неотрицательных целых чисел.

    >>> g = integers()
    >>> next(g)
    0
    >>> next(g)
    1
    >>> next(g)
    2
    >>> next(g)
    3
    >>> next(g)
    4
    """
    
    n = 0
    while True:
        yield n
        n += 1


def primes():
    """
    Генератор простых чисел.

    >>> p = primes()
    >>> next(p)
    2
    >>> next(p)
    3
    >>> next(p)
    5
    >>> next(p)
    7
    >>> next(p)
    11
    """
    
    n = 2
    while True:
        for i in range(2, n):
            if n % i == 0:
                break
        else:
            yield n
        n += 1
        
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)

        