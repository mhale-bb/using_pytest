import numbers

def add(x, y):
    result = x + y
    if not isinstance(result, numbers.Number):
        raise TypeError('tried to add non-numbers')

    return result

def multiply(x, y):
    return x * y
