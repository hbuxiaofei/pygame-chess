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
BOARD_MAX_ROW = 10
# 棋盘最大列
BOARD_MAX_COL = 9
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
        self._chs = None

        # 棋盘是否反转
        self._is_reverse = 0

        self.reset()

    def reset(self):
        # 选中棋子位置
        self.choose_pos = None

        # 可以移动的位置
        self.choose_can_move_pos = []

        # 象棋
        fen = "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w - - 0 1"
        self._chs = Chess(fen)

    def get_chess(self):
        return self._chs

    def convert_pos_2d(self, pos):
        row = pos//16 - 3
        col = pos%16 - 3
        if (self._is_reverse):
            row = BOARD_MAX_ROW - row -1
            col = BOARD_MAX_COL - col -1
        return (row, col)

    def convert_2d_pos(self, d2):
        (row, col) = d2
        if (self._is_reverse):
            row = BOARD_MAX_ROW - row - 1
            col = BOARD_MAX_COL - col - 1
        pos = (row+3)*16 + (col+3)
        return pos

    def reverse_board(self):
        self._is_reverse = 1 - self._is_reverse

        # 选中棋子位置反转
        if self.choose_pos != None:
            row = BOARD_MAX_ROW - self.choose_pos[0] - 1
            col = BOARD_MAX_COL - self.choose_pos[1] - 1
            self.choose_pos = (row, col)

        # 可以移动的位置反转
        if self.choose_can_move_pos != None:
            pos_list = []
            for pos in self.choose_can_move_pos:
                row = BOARD_MAX_ROW - pos[0] - 1
                col = BOARD_MAX_COL - pos[1] - 1
                pos_list.append((row, col))
            self.choose_can_move_pos = pos_list

    def get_2d_board(self):
        array_2d = [[0] * (BOARD_MAX_COL) for i in range(BOARD_MAX_ROW)]
        for index in range(16, len(self._chs.piece)):
            k = self._chs.piece[index]
            if k:
                i = k // 16 - 3
                j = k % 16 - 3
                if (self._is_reverse):
                    i = BOARD_MAX_ROW - i - 1
                    j = BOARD_MAX_COL - j - 1
                array_2d[i][j] = index
        return array_2d

    def _refresh_chessman(self):
        ''' 刷新所有棋子 '''

        board_2d = self.get_2d_board()
        for i in range(len(board_2d)):
            for j in range(len(board_2d[i])):
                pc = board_2d[i][j]
                pc_char = int2fen_char(pc)
                if isinstance(pc_char, str):
                    row = i
                    col = j
                    left = col * BOARD_GAP + BOARD_LEFT
                    top = row * BOARD_GAP + BOARD_TOP
                    if pc_char.isupper():
                        pc_char = "w_" + pc_char
                    else:
                        pc_char = "b_" + pc_char
                    # 显示每个棋子图片
                    self.window.blit(self._chessman_img[pc_char], (left, top))

    def _refresh_last_move(self):
        if len(self._chs.movestack) > 0:
            stack_head = self._chs.movestack[-1]
            last_move = []

            (pos_row, pos_col) = self.convert_pos_2d(stack_head.from_pos)
            last_move.append((pos_row, pos_col))
            (pos_row, pos_col) = self.convert_pos_2d(stack_head.to_pos)
            last_move.append((pos_row, pos_col))

            for pos in last_move:
                left = pos[1] * BOARD_GAP + BOARD_LEFT
                top = pos[0] * BOARD_GAP + BOARD_TOP
                self.window.blit(self._mark_img, (left, top))

    def redraw_borad(self):
        ''' 根据每个单元格对应的棋子重绘棋盘 '''

        # 显示背景
        self.window.blit(self._ground_img, (30, 30))

        # 显示所有棋子
        self._refresh_chessman()

        # 显示上一步走法
        self._refresh_last_move()

        # 标记选中的棋子
        if self.choose_pos != None:
            row = self.choose_pos[0]
            col = self.choose_pos[1]
            left = col * BOARD_GAP + BOARD_LEFT
            top = row * BOARD_GAP + BOARD_TOP
            self.window.blit(self._mark_img, (left, top))

        # 可走的位置
        if self.choose_can_move_pos != None:
            for pos in self.choose_can_move_pos:
                row = pos[0]
                col = pos[1]
                left = col * BOARD_GAP + BOARD_LEFT
                top = row * BOARD_GAP + BOARD_TOP
                self.window.blit(self._can_move_img, (left, top))

        # 刷新操作面板
        self.oper_panel.refresh()

    def _choose_chessman(self, row, col):
        ''' 选择棋子 '''

        board_2d = self.get_2d_board()
        if board_2d[row][col] != 0:
            side = self._chs.get_side()
            pos = self.convert_2d_pos((row, col))
            pc = self._chs.get_board()[pos]
            if self._chs.is_match_side_pc(side, pc):
                self.choose_pos = (row, col)
                self.choose_can_move_pos = []
                for k in self._chs.get_can_move_list(pos):
                    self.choose_can_move_pos.append(self.convert_pos_2d(k))

    def move_chessman(self, row, col):
        ''' 移动棋子 '''

        if (row >= 0 and row < 10) and (col >= 0 and col < 9):
            pos = self.convert_2d_pos((row, col))
            board = self._chs.get_board()
            if self.choose_pos != None:
                m = ChessboardMove()
                m.from_pos = self.convert_2d_pos(self.choose_pos)
                m.to_pos = pos
                if self._chs.check_move(m):
                    # 移动
                    self._chs.make_move(m)
                    self.choose_pos = None
                    self.choose_can_move_pos = []
                else:
                    self._choose_chessman(row, col)
            else:
                self._choose_chessman(row, col)
