# -*- coding: utf-8 -*-
import sys
import pygame
import copy
import random

from Common import Structure
from Chess import Board
from Chess import Base
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
                self._col, self._row + 40,
                101, 28, cb_reverse_board, args)
        self._button_list.append(btn)

        # 重置棋盘按钮
        btn = GuiButton(self._win, "Reset",
                self._col, self._row,
                101, 28, cb_reset_board, args)
        self._button_list.append(btn)

        # 回退按钮
        btn = GuiButton(self._win, "Back",
                self._col + 117, self._row,
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

        # 暂停走棋
        if board.is_stop():
            return

        # 回合数, 总步数 = 回合数 * 2
        depth = 5

        # 创建minimax树
        mtree = ai_value.chessman_create_minimax_tree(board, depth,
                Board.chessboard_evaluate,
                Board.get_all_possible_steps,
                Board.chessboard_ai_move,
                is_max=(board.curStepColor == Base.COLOR_RED))

        # 取得所有最佳招法列表
        nodelist = ai_value.chessman_get_minimax_moves(mtree,
                Board.chessboard_evaluate,
                is_max=(board.curStepColor == Base.COLOR_RED))

        # 随机选择一种走法
        node_last = random.choice(nodelist)
        move_path = node_last.get_elder()
        node_first = move_path[1]
        chessboard = node_first.get_data()

        # 走棋
        pos_change = Board.chessboard_get_step_by_board(board.board, chessboard.board)
        Board.chessboard_ai_move(window, board, pos_change[0], pos_change[1])
