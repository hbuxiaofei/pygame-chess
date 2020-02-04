# -*- coding: utf-8 -*-
import sys
import pygame
import copy
import random

from Chess import Board
from Chess import Base
from Chess import Structure
from ai import value as ai_value

button_list = []

# 按钮弹起颜色
BUTTON_UP_COLOR = (238,232,170)
# 按钮按下颜色
BUTTON_DOWN_COLOR = (255,255,224)
# 按钮边框颜色
BUTTON_RIM_COLOR = (255,255,255)

# 按钮字符颜色
BUTTON_TEXT_COLOR = (54,54,54)


class GuiButton(object):
    """ 按钮类
    """

    def __init__(self, win, text, x, y, w, h, cb=None, arg=None):
        self._win = win
        self._text = text
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._cb = cb
        self._arg = arg
        self._color = BUTTON_UP_COLOR
        self._color_rim = BUTTON_RIM_COLOR

    def refresh(self):
        # 填充色
        pygame.draw.rect(self._win, self._color, (self._x,self._y,self._w,self._h), 0)
        # 边框色
        pygame.draw.rect(self._win, self._color_rim, (self._x,self._y,self._w,self._h), 1)
        font = pygame.font.SysFont(None, 20)
        textSurf = font.render(self._text, True, BUTTON_TEXT_COLOR)
        textRect = textSurf.get_rect()
        textRect.center = ((self._x+(self._w/2)), (self._y+(self._h/2)))
        self._win.blit(textSurf, textRect)

    def process(self, pos, mouse):
        if self._x + self._w > pos[0] > self._x and self._y + self._h > pos[1] > self._y:
            if not mouse[0]:
                # 按钮弹起填充色
                self._color = BUTTON_UP_COLOR
                if self._cb != None:
                    self._cb(self._arg)
            else:
                # 按钮按下填充色
                self._color = BUTTON_DOWN_COLOR


class GuiButtonBox(object):
    def __init__(self, win, row, col):
        self._win = win
        self._row = row
        self._col = col
        self._button_list = get_button_list()

    def init(self, args):
        self._button_list.clear()

        # 翻转棋盘按钮 BOARD_COL, BOARD_ROW + BOARD_HEIGHT
        btn = GuiButton(self._win, "Reverse",
                self._col, self._row,
                101, 28, cb_reverse_board, args)
        self._button_list.append(btn)

        # 重置棋盘按钮
        btn = GuiButton(self._win, "Reset",
                self._col + 117, self._row,
                101, 28, cb_reset_board, args)
        self._button_list.append(btn)

        # 回退按钮
        btn = GuiButton(self._win, "Back",
                self._col, self._row + 40,
                101, 28, cb_back_board, args)
        self._button_list.append(btn)

        # 提示按钮
        btn = GuiButton(self._win, "Prompt",
                self._col + 117, self._row + 40,
                101, 28, cb_back_prompt, args)
        self._button_list.append(btn)

    def refresh(self):
        for button in self._button_list:
            button.refresh()


    def process(self, pos, mouse):
        for button in self._button_list:
            button.process(pos, mouse)


def get_button_list():
    global button_list
    return button_list

def cb_reverse_board(args=None):
    if args != None and "board" in args:
        args["board"].reverseBoard()


def cb_reset_board(args=None):
    if args != None and "board" in args and "window" in args:
        args["window"].resetWindow()
        args["board"].resetBorad()


def cb_back_board(args=None):
    if args != None and "board" in args and "window" in args:
        chessboard = args["board"]
        args["window"].backBorad(chessboard)

def cb_back_prompt(args=None):
    if args != None and "board" in args and "window" in args:
        board = args["board"]
        window = args["window"]

        # 保存当前局面为根节点
        chessboard_copy = copy.deepcopy(board)
        mtree = Structure.MultiTree(chessboard_copy)
        mtree_head = mtree.get_head()

        # 保存步长深度所有走法
        step_deep = 1
        for deep in range(step_deep):
            nodelist = mtree.get_nodelist_by_deep(deep)
            for node in nodelist:
                chessboard = node.get_data()
                points = Board.get_all_possible_steps(chessboard)
                for cur_pos in points.keys():
                    for to_pos in points[cur_pos]:
                        chessboard_copy = copy.deepcopy(node.get_data())
                        chessboard_copy.aiChessmanChoose(cur_pos[0], cur_pos[1])
                        chessboard_copy.aiMoveChess(to_pos[0], to_pos[1])
                        child = Structure.TreeNode(chessboard_copy)
                        node.add(child)

        # maxmin计算深度
        calc_deep = 6
        for deep in range(calc_deep):
            nodelist = mtree.get_nodelist_by_deep(deep+step_deep)
            for node in nodelist:
                chessboard = node.get_data()
                curColor = chessboard.curStepColor
                points = Board.get_all_possible_steps(chessboard)

                chessboard_child_list = []
                max_value = -sys.maxsize
                min_value = sys.maxsize
                max_value_last = -sys.maxsize
                min_value_last = sys.maxsize
                # 遍历所有子粒
                for cur_pos in points.keys():
                    # 遍历每个子粒的所有走法
                    for to_pos in points[cur_pos]:
                        chessboard_copy = copy.deepcopy(node.get_data())
                        chessboard_copy.aiChessmanChoose(cur_pos[0], cur_pos[1])
                        chessboard_copy.aiMoveChess(to_pos[0], to_pos[1])

                        board_fmt = chessboard_copy.formatBoard()
                        value_all = ai_value.chessman_get_value_all(board_fmt)

                        value_tmp = value_all[0] - value_all[1]
                        if curColor == Base.COLOR_RED:
                            if value_tmp >= max_value:
                                if value_tmp == max_value:
                                    chessboard_child_list.append(chessboard_copy)
                                else:
                                    chessboard_child_list = [chessboard_copy]
                                max_value = value_tmp
                        else:
                            if value_tmp <= min_value:
                                if value_tmp == min_value:
                                    chessboard_child_list.append(chessboard_copy)
                                else:
                                    chessboard_child_list = [chessboard_copy]
                                min_value =value_tmp

                for chessboard_child in chessboard_child_list:
                    child = Structure.TreeNode(chessboard_child)
                    node.add(child)
                max_value_last = max_value
                min_value_last = min_value

        nodelist = []
        bottom_nodelist = mtree.get_nodelist_by_deep(calc_deep+step_deep)
        head_color = mtree_head.get_data().curStepColor
        for node in bottom_nodelist:
            chessboard = node.get_data()
            board_fmt = chessboard.formatBoard()
            value_all = ai_value.chessman_get_value_all(board_fmt)
            value_tmp = value_all[0] - value_all[1]
            if head_color == Base.COLOR_RED:
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

        ##################
        print(">>> avilable steps:")
        for node in nodelist:
            for index in range(calc_deep+step_deep-1):
                node = node.get_parent()
            chessboard = node.get_data()
            board_fmt = chessboard.formatBoard()
            print(">>>step:")
            for i in range(10):
                print(board_fmt[i])
        ##################

        # 随机选择一种走法
        node = random.choice(nodelist)
        for index in range(calc_deep+step_deep-1):
            node = node.get_parent()

        # 走棋
        window.saveBorad(board.board)
        board.board = chessboard.board
        if board.curStepColor == Base.COLOR_RED:
            board.curStepColor = Base.COLOR_BLACK
        else:
            board.curStepColor = Base.COLOR_RED
        board.moveSteps = 0
        board.curRow = -1
        board.curCol = -1
