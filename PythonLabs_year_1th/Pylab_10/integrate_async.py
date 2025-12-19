# итерация 2
# оптимизация с помощью потоков

# итерация 3
# оптимизация с помощью процессов


import concurrent.futures as ftres
from functools import partial
import math

from integrate_1 import integrate_1

def integrate_async(f, a, b, *, n_jobs=2, n_iter=1000):
    """
      - аннотировать аргументы
      - реализовать аналогичную функцию для вычисления с процессами (ProcessPoolExecutor)
      - оценить время работы программ с потоками и процессами и зафиксировать значения (2, 4, 6, 8(?))
    """

    executor = ftres.ThreadPoolExecutor(max_workers=n_jobs) # создаваемый пул тредов будет размера n_jobs

    spawn = partial(executor.submit, integrate_1, f, n_iter = n_iter // n_jobs)   # partial позволяет "закрепить"
                                                                                  # несколько аргументов
                                                                                  # для удобства вызова функции ,
                                                                                  # см. пример ниже
    step = (b - a) / n_jobs
    for i in range(n_jobs):

      print(f"Работник {i}, границы: {a + i * step}, {a + (i + 1) * step}")


    fs = [spawn(a + i * step, a + (i + 1) * step) for i in range(n_jobs)]    # создаем потоки с помощью генератора
                                                                            # списков; partial позволил нам

    return sum(list(f.result() for f in ftres.as_completed(fs)))                # as.completed() берет на вход список
                                                                                # фьючерсов и как только какой-то
                                                                                # завершился, возвращает результат
                                                                                # f.result(), далее, мы эти результаты
                                                                                # складываем

# print(integrate_async(math.sin, 0, math.pi))