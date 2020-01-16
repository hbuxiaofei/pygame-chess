# -*- coding: utf-8 -*-
import pygame


button_list = []

# 按钮弹起颜色
BUTTON_UP_COLOR = (0,255,0)
# 按钮按下颜色
BUTTON_DOWN_COLOR = (0,200,0)
# 按钮边框颜色
BUTTON_RIM_COLOR = (0,0,255)

# 按钮字符颜色
BUTTON_TEXT_COLOR = (200,0,0)


class GuiButton(object):
    """ 按钮类
    """

    def __init__(self, win, board, text, x, y, w, h, cb=None, arg=None):
        self._win = win
        self._board = board
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


def get_button_list():
    global button_list
    return button_list


def refresh():
    for button in get_button_list():
        button.refresh()


def process(pos, mouse):
    for button in get_button_list():
        button.process(pos, mouse)


def init(win, board):
    btn_list = get_button_list()
    btn_list.clear()

    # 翻转棋盘
    btn = GuiButton(win, board, "Reverse", 0, 560, 80, 28, cb_reverse_board, board)

    btn_list.append(btn)


def cb_reverse_board(board=None):
    if board != None:
        board.reverseBoard()
