# -*- coding: utf-8 -*-
import sys
import pygame
import copy

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

        board_fmt = args["board"].formatBoard()
        value_all = ai_value.chessman_get_value_all(board_fmt)

        for i in range(10):
            print(board_fmt[i])

        print(value_all)

        path = []
        board_copy = copy.deepcopy(board)
        mtree = Structure.MultiTree(board_copy)
        node = mtree.get_head()

        calc_deep = 2
        for deep in range(calc_deep):
            nodelist = mtree.get_nodelist_by_deep(deep)
            for node in nodelist:
                chessboard = node.get_data()
                points = Board.get_all_possible_steps(chessboard)
                for cur_pos in points.keys():
                    for to_pos in points[cur_pos]:
                        board_copy = copy.deepcopy(node.get_data())
                        board_copy.chessmanChoose(window, cur_pos[0], cur_pos[1])
                        board_copy.moveChess(window, to_pos[0], to_pos[1])
                        child = Structure.TreeNode(board_copy)
                        #  if cur_pos == (9, 8):
                        node.add(child)

        nodelist = mtree.get_nodelist_by_deep(calc_deep)
        max_value = -sys.maxsize
        min_value = sys.maxsize
        maxmin = {"max":[max_value], "min":[min_value]}
        for node in nodelist:
            chessboard = node.get_data()
            board_fmt = chessboard.formatBoard()
            value_all = ai_value.chessman_get_value_all(board_fmt)
            value_tmp = value_all[0] - value_all[1]
            if value_tmp >= max_value:
                if value_tmp == max_value:
                    maxmin["max"].append(node.get_path())
                else:
                    maxmin["max"] = [value_tmp, node.get_path()]
                max_value = value_tmp
            if value_tmp <= min_value:
                if value_tmp == min_value:
                    maxmin["min"].append(node.get_path())
                else:
                    maxmin["min"] = [value_tmp, node.get_path()]
                min_value =value_tmp


        def travel_func(node):
            chessboard = node.get_data()
            board_fmt = chessboard.formatBoard()
            value_all = ai_value.chessman_get_value_all(board_fmt)
            print("deep:", node.get_deep(), "path:", node.get_path(), "value:", value_all)
            for i in range(10):
                print(board_fmt[i])
            print("")
        #  mtree.travel(func=travel_func)

        print(maxmin)
        path = []
        if board.curStepColor == Base.COLOR_RED:
            path = maxmin["max"][1]
        else:
            path = maxmin["min"][1]

        ##################
        node = mtree.search(path)
        chessboard = node.get_data()
        board_fmt = chessboard.formatBoard()
        print("step--->:", node.get_path())
        for i in range(10):
            print(board_fmt[i])

        node = node.get_parent()
        chessboard = node.get_data()
        board_fmt = chessboard.formatBoard()
        print("step--->:", node.get_path())
        for i in range(10):
            print(board_fmt[i])

        node = node.get_parent()
        chessboard = node.get_data()
        board_fmt = chessboard.formatBoard()
        print("step--->:", node.get_path())
        for i in range(10):
            print(board_fmt[i])
        ##################

        node = mtree.search([path[0]])
        chessboard = node.get_data()
        board_fmt = chessboard.formatBoard()
        print("\n\n")
        for i in range(10):
            print(board_fmt[i])

        #  board.chessmanChoose(window, chessboard.curRow, chessboard.curCol)
        if board.curStepColor == Base.COLOR_RED:
            board.curStepColor = Base.COLOR_BLACK
        else:
            board.curStepColor = Base.COLOR_RED
        board.board = chessboard.board
        board.moveSteps = 0

        number = 0
        def travel_print(node):
            nonlocal number
            number = number + 1
            print(">>>> number:", number)
        #  mtree.travel(func=travel_print)
