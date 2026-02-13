from guess_number import guess_number

def main():
    """
    Ввод значений с клавиатуры для формирования
    списка, по которому мы ищем искомое число и
    искомого числа
    (опционально) предложить пользователю сформировать
    список вручную с клавиатуры

    __вызов функции guess-number с параметрами: __
      - искомое число (target)
      - список, по-которому идем
      - тип поиска (последовательный, бинарный)

    __вывод результатов на экран__
    :return:
    """

    target = int(input('Введите target: '))
    start_range = int(input('Введите начало диап: '))
    end_range = int(input('Введите конец диап: '))
    d = list(range(start_range, end_range + 1))

    res = guess_number(target, d, type='bin')
    print(">>> Result:", f'{res}')


if __name__ == '__main__':
    main()