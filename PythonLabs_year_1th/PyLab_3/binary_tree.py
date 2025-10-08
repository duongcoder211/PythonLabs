def gen_bin_tree(height, root):
    leafs = []
    leafs.append(root)
    for i in range(0, height):
        for leaf in leafs[2**i - 1 : 2 * 2**i - 1]:
            left_leaf = leaf * 2 - 2
            right_leaf = leaf + 4
            leafs.append(left_leaf)
            leafs.append(right_leaf)
            # print(leafs)
    for i in range(0, height):
        print(str(leafs[(2**i - 1) : (2 * 2**i - 1)]).center(100))
gen_bin_tree(5, 6)