def fact_iterative(n):
    """Возвращает факториала числа n путем повторения"""
    factorial = 1
    for i in range(1,n+1):
        factorial*=i
    return factorial