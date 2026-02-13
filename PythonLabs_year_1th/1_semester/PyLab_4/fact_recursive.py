def fact_recursive(n):
    """Возвращает факториала числа n путем рекурция"""
    return n*fact_recursive(n-1) if n else 1