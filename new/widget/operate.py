# -*- coding: utf-8 -*-
import pygame

from widget.base import widget_load_image
from widget.button import GuiButtonBox


class OperatePanel(object):
    ''' 操作面板 '''
    def __init__(self, win, row, col):
        self._win = win
        self._row = row
        self._col = col

        self._button_box = GuiButtonBox(win, row + 431, col + 20)

        self._panel_image, rc = widget_load_image("images/operate.bmp")

    def refresh(self):
        self._win.blit(self._panel_image, (self._col, self._row))
        self._button_box.refresh()


    def button_init(self, board):
        self._button_box.init(board)

    def button_process(self, pos, mouse):
        self._button_box.process(pos, mouse)
