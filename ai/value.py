#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import copy
from Common import Structure

# 子粒价值表
chessman_value = {
	"C":[
		[206, 208, 207, 213, 214, 213, 207, 208, 206],
		[206, 212, 209, 216, 233, 216, 209, 212, 206],
		[206, 208, 207, 214, 216, 214, 207, 208, 206],
		[206, 213, 213, 216, 216, 216, 213, 213, 206],
		[208, 211, 211, 214, 215, 214, 211, 211, 208],

		[208, 212, 212, 214, 215, 214, 212, 212, 208],
		[204, 209, 204, 212, 214, 212, 204, 209, 204],
		[198, 208, 204, 212, 212, 212, 204, 208, 198],
		[200, 208, 206, 212, 200, 212, 206, 208, 200],
		[194, 206, 204, 212, 200, 212, 204, 206, 194]
	],

	"M":[
		[90, 90, 90, 96, 90, 96, 90, 90, 90],
		[90, 96,103, 97, 94, 97,103, 96, 90],
		[92, 98, 99,103, 99,103, 99, 98, 92],
		[93,108,100,107,100,107,100,108, 93],
		[90,100, 99,103,104,103, 99,100, 90],

		[90, 98,101,102,103,102,101, 98, 90],
		[92, 94, 98, 95, 98, 95, 98, 94, 92],
		[93, 92, 94, 95, 92, 95, 94, 92, 93],
		[85, 90, 92, 93, 78, 93, 92, 90, 85],
		[88, 85, 90, 88, 90, 88, 90, 85, 88]
	],

	"X":[
		[0, 0,20, 0, 0, 0,20, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0,23, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0,20, 0, 0, 0,20, 0, 0],

		[0, 0,20, 0, 0, 0,20, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[18,0, 0, 0,23, 0, 0, 0,18],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0,20, 0, 0, 0,20, 0, 0]
	],

	"S":[
		[0, 0, 0,20, 0,20, 0, 0, 0],
		[0, 0, 0, 0,23, 0, 0, 0, 0],
		[0, 0, 0,20, 0,20, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],

		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0,20, 0,20, 0, 0, 0],
		[0, 0, 0, 0,23, 0, 0, 0, 0],
		[0, 0, 0,20, 0,20, 0, 0, 0]
	],

	"J":[
		[0, 0, 0, 8888, 8888, 8888, 0, 0, 0],
		[0, 0, 0, 8888, 8888, 8888, 0, 0, 0],
		[0, 0, 0, 8888, 8888, 8888, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],

		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 8888, 8888, 8888, 0, 0, 0],
		[0, 0, 0, 8888, 8888, 8888, 0, 0, 0],
		[0, 0, 0, 8888, 8888, 8888, 0, 0, 0]
	],

	"P":[

		[100, 100,  96, 91,  90, 91,  96, 100, 100],
		[ 98,  98,  96, 92,  89, 92,  96,  98,  98],
		[ 97,  97,  96, 91,  92, 91,  96,  97,  97],
		[ 96,  99,  99, 98, 100, 98,  99,  99,  96],
		[ 96,  96,  96, 96, 100, 96,  96,  96,  96],

		[ 95,  96,  99, 96, 100, 96,  99,  96,  95],
		[ 96,  96,  96, 96,  96, 96,  96,  96,  96],
		[ 97,  96, 100, 99, 101, 99, 100,  96,  97],
		[ 96,  97,  98, 98,  98, 98,  98,  97,  96],
		[ 96,  96,  97, 99,  99, 99,  97,  96,  96]
	],

	"Z":[
		[ 9,  9,  9, 11, 13, 11,  9,  9,  9],
		[19, 24, 34, 42, 44, 42, 34, 24, 19],
		[19, 24, 32, 37, 37, 37, 32, 24, 19],
		[19, 23, 27, 29, 30, 29, 27, 23, 19],
		[14, 18, 20, 27, 29, 27, 20, 18, 14],

		[ 7,  0, 13,  0, 16,  0, 13,  0,  7],
		[ 7,  0,  7,  0, 15,  0,  7,  0,  7],
		[ 0,  0,  0,  0,  0,  0,  0,  0,  0],
		[ 0,  0,  0,  0,  0,  0,  0,  0,  0],
		[ 0,  0,  0,  0,  0,  0,  0,  0,  0]
	]
}


def chessman_get_value(name, row, col, isRed=True):
    if name not in chessman_value:
        return None

    if (row < 0 or row > 9) or (col < 0 or col > 8):
        return None

    if not isRed:
        row = 9 - row
        col = 8 - col

    chessman = chessman_value[name]
    return chessman[row][col]


def chessman_get_value_all(board=None):
    # board:
    # ['c', 'm', 'x', 's', 'j', 's', 'x', 'm', 'c']
    # [0, 0, 0, 0, 0, 0, 0, 0, 0]
    # [0, 'p', 0, 0, 0, 0, 0, 'p', 0]
    # ['z', 0, 'z', 0, 'z', 0, 'z', 0, 'z']
    # [0, 0, 0, 0, 0, 0, 0, 0, 0]
    # [0, 0, 0, 0, 0, 0, 0, 0, 0]
    # ['Z', 0, 'Z', 0, 'Z', 0, 'Z', 0, 'Z']
    # [0, 'P', 0, 0, 0, 0, 0, 'P', 0]
    # [0, 0, 0, 0, 0, 0, 0, 0, 0]
    # ['C', 'M', 'X', 'S', 'J', 'S', 'X', 'M', 'C']
    red_value = 0
    black_value = 0
    kind_list = ['C', 'M', 'X', 'S', 'J', 'P', 'Z', 'c', 'm', 'x', 's', 'j', 'p', 'z']
    for row in range(10):
        for col in range(9):
            kind = board[row][col]
            if kind in kind_list:
                if kind.isupper():
                    red_value = red_value + chessman_get_value(kind, row, col, isRed=True)
                else:
                    black_value = black_value + chessman_get_value(kind.upper(), row, col, isRed=False)
    return (red_value, black_value)


def chessman_create_minimax_tree(board, depth, eval_fn,
        get_next_moves_fn, do_move_fn, is_max=True):

    chessboard_copy = copy.deepcopy(board)
    mtree = Structure.MultiTree(chessboard_copy)
    mtree_head = mtree.get_head()

    # 回合数深度
    step_deep = depth

    # 广度优先遍历 BFS
    for deep in range(step_deep*2):
        # 获取最后一层所有节点
        nodelist = mtree.get_nodelist_by_deep(deep)
        max_value_last = sys.maxsize
        min_value_last = -sys.maxsize
        for node in nodelist:
            chessboard = node.get_data()

            # 获取下一步所有可选走法
            #  {(9, 6): [(7, 4), (7, 8)],
            #   (9, 5): [(8, 4)],
            #   (9, 4): [(8, 4)],
            #   (9, 3): [(8, 4)],
            #   (9, 2): [(7, 0), (7, 4)]}
            points = get_next_moves_fn(chessboard)
            if deep % 2 == 0:
                for cur_pos in points.keys():
                    for to_pos in points[cur_pos]:
                        chessboard_copy = copy.deepcopy(node.get_data())
                        do_move_fn(None, chessboard_copy, cur_pos, to_pos)
                        child = Structure.TreeNode(chessboard_copy)
                        node.add(child)
            else:
                chessboard_child_list = []
                max_value = -sys.maxsize
                min_value = sys.maxsize
                # 是否剪枝
                is_pruning = False
                # 遍历所有子粒
                for cur_pos in points.keys():
                    # 遍历每个子粒的所有走法
                    for to_pos in points[cur_pos]:
                        chessboard_copy = copy.deepcopy(node.get_data())
                        do_move_fn(None, chessboard_copy, cur_pos, to_pos)

                        # 评价所有子粒价值=(red_value, black_value)
                        value_all = eval_fn(chessboard_copy)
                        value_tmp = value_all[0] - value_all[1]
                        if is_max == True:
                            if value_tmp > max_value_last:
                                is_pruning = True
                                chessboard_child_list = []
                                break
                            if value_tmp >= max_value:
                                if value_tmp == max_value:
                                    chessboard_child_list.append(chessboard_copy)
                                else:
                                    chessboard_child_list = [chessboard_copy]
                                max_value = value_tmp
                        else:
                            if value_tmp < min_value_last:
                                is_pruning = True
                                chessboard_child_list = []
                                break
                            if value_tmp <= min_value:
                                if value_tmp == min_value:
                                    chessboard_child_list.append(chessboard_copy)
                                else:
                                    chessboard_child_list = [chessboard_copy]
                                min_value = value_tmp
                    if is_pruning:
                        break
                for chessboard_child in chessboard_child_list:
                    child = Structure.TreeNode(chessboard_child)
                    node.add(child)
                    max_value_last = max_value
                    min_value_last = min_value
        is_max = (not is_max)
    return mtree


def chessman_get_minimax_moves(mtree, eval_fn, is_max=True):
    nodelist = []
    mtree_height = mtree.get_height()
    bottom_nodelist = mtree.get_nodelist_by_deep(mtree_height)

    max_value = -sys.maxsize
    min_value = sys.maxsize
    for node in bottom_nodelist:
        chessboard = node.get_data()

        value_all = eval_fn(chessboard)
        value_tmp = value_all[0] - value_all[1]
        if is_max == True:
            if value_tmp >= max_value:
                if value_tmp == max_value:
                    nodelist.append(node)
                else:
                    nodelist = [node]
                    max_value = value_tmp
        else:
            if value_tmp <= min_value:
                if value_tmp == min_value:
                    nodelist.append(node)
                else:
                    nodelist = [node]
                    min_value =value_tmp

    return nodelist


def test_main():
    print("start...")
    row = 0
    col = 0
    print("Z(%d, %d) = %d" % (row, col, chessman_get_value("Z", row, col, True)))
    row = 1
    col = 0
    print("Z(%d, %d) = %d" % (row, col, chessman_get_value("Z", row, col, True)))
    row = 5
    col = 0
    print("Z(%d, %d) = %d" % (row, col, chessman_get_value("Z", row, col, True)))


if __name__ == "__main__":
    test_main()
