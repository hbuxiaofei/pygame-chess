# -*- coding: utf-8 -*-
import pygame

from Chess import Board
from Chess import Global
from Chess import Button


class Panel(object):

    def __init__(self, win, row, col):
        self._win = win
        self._row = row
        self._col = col

        self._button_box = Button.GuiButtonBox(win, row + 431, col + 20)

        self._info_image, rc = Global.load_image("images/operate.bmp")

    def refresh(self):
        self._win.blit(self._info_image, (self._col, self._row))
        self._button_box.refresh()


    def button_init(self, board):
        self._button_box.init(board)

    def button_process(self, pos, mouse):
        self._button_box.process(pos, mouse)
