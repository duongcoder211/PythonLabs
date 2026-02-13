from collections import defaultdict
from left_branch import left_branch
from right_branch import right_branch
from functools import lru_cache

@lru_cache
def gen_bin_tree_optimized_recursive(height = 5, root = 6) -> list:
    """
    Ввод значений корни и высоты для cоздания бинарного дерева
    ,по которому мы ищем бинарного дерева в виде словаря 
    
    __вызов функции gen_bin_tree с параметрами: __
      - высоты (height)
      - корень (root)
    __вывод результатов на экран__
    :return:
    """
    # Установка условии закончения рекурции
    if(height == 0):
        # Создание новый пустой словарь
        tree = defaultdict()
        # Добавление пустого списка
        tree[str(root)] = []
        # Приведение типа данных collections.defaultdict в словарь и возвращение последней ветки дерева
        return list(tree)
    
    # Обновление новых корней
    l_b = left_branch(root)
    r_b = right_branch(root)

    # Создание новый пустой словарь
    bin_tree = defaultdict()
    # Присвоение текущего корни с списком 2 новых ветки
    bin_tree[str(root)] = [gen_bin_tree_optimized_recursive(height-1, l_b), gen_bin_tree_optimized_recursive(height-1, r_b)]
    # Приведение типа данных collections.defaultdict в словарь и возвращение бинарного дерева
    return dict(bin_tree)
