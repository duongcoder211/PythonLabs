from functools import lru_cache

@lru_cache
def gen_bin_tree_optimized_iterative(height=5, root=6, left_branch=lambda l_r: (l_r*2)-2, right_branch=lambda r_r: r_r+4):
    """
        __ Создание бинарного дерева в виде списки

        __ Вход в функцию получает 4 аргумента
            height: число обозначает высоту дерева, считается с 0, по умочанию = 5
            root: число обозначает корень дерева, по умочанию = 6
            left_branch, right_branch : функции возвращают значения следущих корень соответствия названию

        __ Возвращение бинарного дерева (tree), которое имеет вид [{"6":[10,10]}, {"10":[18,14]}, {"10":[18,14]}, ...]

    """
    # Создание пустого списка для хранения значений корней и добавление первого корня в список
    roots = []
    roots.append(root)

    # Добавление всех остальных значений корней в список, Список иммеет вид [6,10,10,14,18,14,18,...]
    for i in range (height):
        for rt in roots[2**i - 1:]:
            roots.append(left_branch(rt))
            roots.append(right_branch(rt))

    # Доступ к каждому корню и присвоенение их значений
    tree = list(map(lambda index_root: {str(index_root[1]): [left_branch(index_root[1]), right_branch(index_root[1])] if (index_root[0] < len(roots) - 2**height) else []}, enumerate(roots)))

    # Возвращение бинарного дерева (tree)
    return tree

# if __name__ == "__main__":
#     # Вызов функции и печать на экране
#     print(gen_bin_tree_iterative())

