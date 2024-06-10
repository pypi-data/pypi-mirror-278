def limit_number(x, left, right):
    _min = min(left, right)
    _max = max(left, right)
    if x < _min:
        return _min
    if x > _max:
        return _max
    return x
