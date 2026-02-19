# def f(a,b,c = 20):
#     print(a, b, c)
# def f1(a,b,*,c = 20):
#     print(a, b, c)

# f(1,2)
# f1(1,2)
# f(1,2,3)
# f1(1,2,c=3)
# f1(1,2,3,4)

# import timeit

# f = open("result.txt", mode="w")
# def fib(n = 1000):
#         a,b = 0,1
#         while b < n:
#             # print(b, end=" ", file=f)
#             a, b = b, a+b

# def opt_fib(n = 1000):
#         a,b = 0,1
#         while b < n:
#             a, b = b, a+b
#             return a

# print(min(timeit.repeat(fib, number=1000, repeat=5)))
# print(min(timeit.repeat(opt_fib, number=1000, repeat=5)))

# a = 5
# def a():
#     return 10
# print(a)
# print(a())

# dict = {
#     "/currency/get" : 123
# }

# print("/currency/get" in dict)
# print(dict["/currency/get"])

# print(list(dict.keys())[0])

# text_concatenation=(
#     "hello "
#     "toi "
#     "ten "
#     "la "
#     "duong."
# )

# print(text_concatenation)

# result_data = list(zip(['id', 'cur', 'date', 'value'], ["1", "2", "3"], ["a", "b", "c"]))
# print(result_data)


import multiprocessing
import time
import math

def calculate_factorial(n):
    result = math.factorial(n)
    print(f"Factorial of {n} calculated")
    return result

def calculate_all_factorials(numbers):
    with multiprocessing.Pool() as pool:
        results = pool.map(calculate_factorial, numbers)
    return results

# Sử dụng
numbers = [10000, 10001, 10002, 10003, 10004]
start_time = time.time()
results = calculate_all_factorials(numbers)
print(f"Thời gian thực thi: {time.time() - start_time} giây")