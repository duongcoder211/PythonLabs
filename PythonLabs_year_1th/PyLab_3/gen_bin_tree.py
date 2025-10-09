from collections import defaultdict
from left_branch import left_branch
from right_branch import right_branch

def gen_bin_tree(height, root) -> list:
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
    bin_tree[str(root)] = [gen_bin_tree(height-1, l_b), gen_bin_tree(height-1, r_b)]
    # Приведение типа данных collections.defaultdict в словарь и возвращение бинарного дерева
    return dict(bin_tree)