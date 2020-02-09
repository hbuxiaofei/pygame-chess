#-*- encoding: utf-8 -*-
import sys, string, os, copy
import datetime
import pygame

from widget.base import *
from widget.operate import OperatePanel
from chess.chess import Chess
from chess.chessboard import int2fen_char
from chess.chessboard import ChessboardMove

# 窗口宽度
WINDOW_WIDTH = 780
# 窗口高度
WINDOW_HEIGHT = 640

# 棋盘宽度
BOARD_WIDTH = 460
# 棋盘高度
BOARD_HEIGHT = 532

# 棋盘坐标
BOARD_COL = 30
BOARD_ROW = 30

# 棋盘左间距
BOARD_LEFT = 5 + BOARD_COL
# 棋盘上间距
BOARD_TOP = 15 + BOARD_ROW

# 棋盘最大行
BOARD_MAX_ROW = 9
# 棋盘最大列
BOARD_MAX_COL = 8
# 棋盘格子间隔
BOARD_GAP = 50


class ChessWindow(object):
    def __init__(self):
        ''' 初始化 '''
        # 窗口
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self._bottom_img, rc = widget_load_image("images/bottom.bmp")
        self._header_img, rc = widget_load_image("images/header.bmp")
        self._footer_img, rc = widget_load_image("images/footer.bmp")
        self._ground_img, rc = widget_load_image("images/ground.bmp")
        self._mark_img, rc = widget_load_image("images/cur_mark.bmp", 0xffffff)
        self._can_move_img, rc = widget_load_image("images/cur_move.bmp", 0xffffff)
        self._chessman_img = widget_load_chessman_image()

        # 初始化界面
        self.window.fill((0,0,0))
        self.window.blit(self._bottom_img, (0, 0))
        self.window.blit(self._header_img, (30, 20))
        self.window.blit(self._footer_img, (30, 550))

        # 操作面板
        self.oper_panel = OperatePanel(self.window, BOARD_TOP//2, BOARD_WIDTH + BOARD_LEFT)

        # 选中棋子位置
        self.choose_pos = None

        # 可以移动的位置
        self.choose_can_move_pos = []

        # 象棋
        fen = "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w"
        self._chs = Chess(fen)

    def _refresh_chessman(self):
        ''' 刷新所有棋子 '''

        board_2d = self._chs.get_2d_board()
        for i in range(len(board_2d)):
            for j in range(len(board_2d[i])):
                pc = board_2d[i][j]
                pc_char = int2fen_char(pc)
                if isinstance(pc_char, str):
                    left = j * BOARD_GAP + BOARD_LEFT
                    top = i * BOARD_GAP + BOARD_TOP
                    if pc_char.isupper():
                        pc_char = "w_" + pc_char
                    else:
                        pc_char = "b_" + pc_char
                    # 显示每个棋子图片
                    self.window.blit(self._chessman_img[pc_char], (left, top))

    def redraw_borad(self):
        ''' 根据每个单元格对应的棋子重绘棋盘 '''

        # 显示背景
        self.window.blit(self._ground_img, (30, 30))

        # 显示所有棋子
        self._refresh_chessman()

        # 标记选中的棋子
        if self.choose_pos != None:
            left = self.choose_pos[1] * BOARD_GAP + BOARD_LEFT
            top = self.choose_pos[0] * BOARD_GAP + BOARD_TOP
            self.window.blit(self._mark_img, (left, top))

        # 可走的位置
        if self.choose_can_move_pos != None:
            for pos in self.choose_can_move_pos:
                left = pos[1] * BOARD_GAP + BOARD_LEFT
                top = pos[0] * BOARD_GAP + BOARD_TOP
                self.window.blit(self._can_move_img, (left, top))

        # 刷新操作面板
        self.oper_panel.refresh()

    def choose_chessman(self, row, col):
        ''' 选择棋子 '''

        board_2d = self._chs.get_2d_board()
        if board_2d[row][col] != 0:
            side = self._chs.get_side()
            pos = (row+3) * 16 + (col+3)
            pc = self._chs.get_board()[pos]
            if self._chs.is_match_side_pc(side, pc):
                self.choose_pos = (row, col)
                self.choose_can_move_pos = []
                for k in self._chs.get_can_move_list(pos):
                    self.choose_can_move_pos.append((k//16-3, k%16-3))

    def move_chessman(self, row, col):
        ''' 移动棋子 '''

        if (row >= 0 and row < 10) and (col >= 0 and col < 9):
            pos = (row+3) * 16 + (col+3)
            board = self._chs.get_board()
            if self.choose_pos != None:
                m = ChessboardMove()
                m.from_pos = (self.choose_pos[0]+3) * 16 + (self.choose_pos[1]+3)
                m.to_pos = pos
                if self._chs.check_move(m):
                    # 移动
                    self._chs.make_move(m)
                    self.choose_pos = None
                    self.choose_can_move_pos = []
                else:
                    self.choose_chessman(row, col)
            else:
                self.choose_chessman(row, col)
