# Функция, которую будем тестировать
def guess_number(target : int, lst, type = "seq") -> list[int | None]:
    # Сортировать список
    lst = sorted(lst)
    # Декларция переменной расчет количества выполнения цикла
    round : int
    if type == "seq":
        round = 0
        # Найти target с помощью цикла for (алгоритма медленного перебора (инкремента))
        for i in lst:
            round += 1
            if i == target:
                # Сообщение о количестве выполнения цикла и методе поиска
                # print("Number", target, "was found in the list after", round, "round" if round == 1 else "rounds", "by method", type)
                return [i, target]
        # Возвращать None в случае не найти target
        return None
            
    if type == "bin":
        round = 0
        isLoop = True
        # Найти target с помощью цикла while (алгоритма бинарного)
        while(isLoop):
            round += 1
            # Найти средний индекс списка
            mid_index = int(len(lst) / 2)
            if target == lst[mid_index]:
                # Сообщение о количестве выполнения цикла и методе поиска
                # print("Number", target, "was found in the list after", round, "round" if round == 1 else "rounds", "by", type, "method")
                return [lst[mid_index], target]
            # Cтрезать список после каждого раза выполнения цикла для уменьшения области поиска
            elif target < lst[mid_index]:
                lst = lst[:mid_index]
            elif target > lst[mid_index]:
                lst = lst[mid_index + 1:]

            # Перестать цикл while в случае не найти target в данном списке
            if mid_index == 0: 
                isLoop = False
                # Сообщение о количества выполнения цикла и методе поиска
                # print("Number", target, "not found in the list after", round, "round" if round == 1 else "rounds", "by", type, "method")
                # Возвращать None в случае не найти target
                return None

# res = guess_number(7, [7,7,7,7,7,7,77,7,7,7,7,7,7,9,9,9,9,8,9,9,9,9,9], "bin")
# print(">>> Result:", res)






