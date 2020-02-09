# -*- coding: utf-8 -*-
import sys
import pygame
import copy
import random


# 按钮弹起颜色
BUTTON_UP_COLOR = (238,232,170)
# 按钮按下颜色
BUTTON_DOWN_COLOR = (255,255,224)
# 按钮边框颜色
BUTTON_RIM_COLOR = (255,255,255)

# 按钮字符颜色
BUTTON_TEXT_COLOR = (54,54,54)


def _cb_reverse_board(args=None):
    if args != None and "window" in args:
        print("cb_reverse_board button")


def _cb_reset_board(args=None):
    if args != None and "window" in args:
        print("cb_reset_board button")


def _cb_back_board(args=None):
    if args != None and "window" in args:
        print("cb_back_board button")


def _cb_board_prompt(args=None):
    if args != None and "window" in args:
        window = args["window"]
        print("cb_board_prompt button")


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
        self._button_list = []

    def init(self, args):
        self._button_list.clear()

        # 翻转棋盘按钮 BOARD_COL, BOARD_ROW + BOARD_HEIGHT
        btn = GuiButton(self._win, "Reverse",
                self._col, self._row + 40,
                101, 28, _cb_reverse_board, args)
        self._button_list.append(btn)

        # 重置棋盘按钮
        btn = GuiButton(self._win, "Reset",
                self._col, self._row,
                101, 28, _cb_reset_board, args)
        self._button_list.append(btn)

        # 回退按钮
        btn = GuiButton(self._win, "Back",
                self._col + 117, self._row,
                101, 28, _cb_back_board, args)
        self._button_list.append(btn)

        # 提示按钮
        btn = GuiButton(self._win, "Prompt",
                self._col + 117, self._row + 40,
                101, 28, _cb_board_prompt, args)
        self._button_list.append(btn)

    def refresh(self):
        for button in self._button_list:
            button.refresh()

    def process(self, pos, mouse):
        for button in self._button_list:
            button.process(pos, mouse)
