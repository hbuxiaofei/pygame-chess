#-*- encoding: utf-8 -*-
import sys, string, os, copy
import datetime
import pygame
from pygame.locals import *

from ChessGlobal import *
from Chessman import *
import Button
import Structure


# 棋盘最大行
BOARD_MAX_ROW = 9
# 棋盘最大列
BOARD_MAX_COL = 8
# 棋盘格子间隔
BOARD_GAP = 50
# 棋盘左间距
BOARD_LEFT = 5
# 棋盘上间距
BOARD_TOP = 15


class ChessBoard(object):
    ''' 象棋棋盘类
    数据:每个单元格对应的棋子
    操作:
        1.走棋
        2.重绘棋盘
        3.显示提示信息
    '''

    def __init__(self, win):
        ''' 初始化 '''

        # 窗口
        self.window = win

        # 走棋步骤: 0-选择棋子  1-移动棋子
        self.moveSteps = 0

        # 当前要走棋的棋子颜色,初始化为红色
        self.curStepColor = CHESSMAN_COLOR_RED

        # 行位置
        self.curRow = -1

        # 列位置
        self.curCol = -1

        # 提示的文本
        self.tipInfo = ''

        # 保存步骤栈
        self.stack = Structure.Stack()

        self.groundImg, rc = load_image("./BMP/ground.bmp")
        self.markImg, rc = load_image("./BMP/curPos.bmp", 0xffffff)
        self.resetBorad()

    def reverseBoard(self):
        """ 反转棋盘 """

        board_tmp = copy.deepcopy(self.board)
        self.board.clear()
        for key in board_tmp.keys():
            chessman = board_tmp[key]
            if chessman == None:
                continue;
            row =  BOARD_MAX_ROW - key[0]
            col = BOARD_MAX_COL - key[1]
            chessman.row = row
            chessman.col = col
            self.board[(row, col)] = chessman
        self.curRow = BOARD_MAX_ROW - self.curRow
        self.curCol = BOARD_MAX_COL - self.curCol

    def resetBorad(self):
        """ 重置棋盘 """

        self.moveSteps = 0
        self.curStepColor = CHESSMAN_COLOR_RED
        self.curRow = -1
        self.curCol = -1
        self.stack.destroy()
        self.board = {
                (9, 8):Chessman(CHESSMAN_KIND_JU, CHESSMAN_COLOR_RED,      9, 8),
                (9, 7):Chessman(CHESSMAN_KIND_MA, CHESSMAN_COLOR_RED,      9, 7),
                (9, 6):Chessman(CHESSMAN_KIND_XIANG, CHESSMAN_COLOR_RED,   9, 6),
                (9, 5):Chessman(CHESSMAN_KIND_SHI, CHESSMAN_COLOR_RED,     9, 5),
                (9, 4):Chessman(CHESSMAN_KIND_JIANG, CHESSMAN_COLOR_RED,   9, 4),
                (9, 3):Chessman(CHESSMAN_KIND_SHI, CHESSMAN_COLOR_RED,     9, 3),
                (9, 2):Chessman(CHESSMAN_KIND_XIANG, CHESSMAN_COLOR_RED,   9, 2),
                (9, 1):Chessman(CHESSMAN_KIND_MA, CHESSMAN_COLOR_RED,      9, 1),
                (9, 0):Chessman(CHESSMAN_KIND_JU, CHESSMAN_COLOR_RED,      9, 0),
                (0, 8):Chessman(CHESSMAN_KIND_JU, CHESSMAN_COLOR_BLACK,    0, 8),
                (0, 7):Chessman(CHESSMAN_KIND_MA, CHESSMAN_COLOR_BLACK,    0, 7),
                (0, 6):Chessman(CHESSMAN_KIND_XIANG, CHESSMAN_COLOR_BLACK, 0, 6),
                (0, 5):Chessman(CHESSMAN_KIND_SHI, CHESSMAN_COLOR_BLACK,   0, 5),
                (0, 4):Chessman(CHESSMAN_KIND_JIANG, CHESSMAN_COLOR_BLACK, 0, 4),
                (0, 3):Chessman(CHESSMAN_KIND_SHI, CHESSMAN_COLOR_BLACK,   0, 3),
                (0, 2):Chessman(CHESSMAN_KIND_XIANG, CHESSMAN_COLOR_BLACK, 0, 2),
                (0, 1):Chessman(CHESSMAN_KIND_MA, CHESSMAN_COLOR_BLACK,    0, 1),
                (0, 0):Chessman(CHESSMAN_KIND_JU, CHESSMAN_COLOR_BLACK,    0, 0),
                (7, 7):Chessman(CHESSMAN_KIND_PAO, CHESSMAN_COLOR_RED,     7, 7),
                (7, 1):Chessman(CHESSMAN_KIND_PAO, CHESSMAN_COLOR_RED,     7, 1),
                (2, 7):Chessman(CHESSMAN_KIND_PAO, CHESSMAN_COLOR_BLACK,   2, 7),
                (2, 1):Chessman(CHESSMAN_KIND_PAO, CHESSMAN_COLOR_BLACK,   2, 1),
                (6, 8):Chessman(CHESSMAN_KIND_BING, CHESSMAN_COLOR_RED,    6, 8),
                (6, 6):Chessman(CHESSMAN_KIND_BING, CHESSMAN_COLOR_RED,    6, 6),
                (6, 4):Chessman(CHESSMAN_KIND_BING, CHESSMAN_COLOR_RED,    6, 4),
                (6, 2):Chessman(CHESSMAN_KIND_BING, CHESSMAN_COLOR_RED,    6, 2),
                (6, 0):Chessman(CHESSMAN_KIND_BING, CHESSMAN_COLOR_RED,    6, 0),
                (3, 8):Chessman(CHESSMAN_KIND_BING, CHESSMAN_COLOR_BLACK,  3, 8),
                (3, 6):Chessman(CHESSMAN_KIND_BING, CHESSMAN_COLOR_BLACK,  3, 6),
                (3, 4):Chessman(CHESSMAN_KIND_BING, CHESSMAN_COLOR_BLACK,  3, 4),
                (3, 2):Chessman(CHESSMAN_KIND_BING, CHESSMAN_COLOR_BLACK,  3, 2),
                (3, 0):Chessman(CHESSMAN_KIND_BING, CHESSMAN_COLOR_BLACK,  3, 0),
                }

    def backBorad(self):
        """ 回退棋盘 """
        if self.stack.size() == 1:
            self.resetBorad()
        elif self.stack.size() >= 2:
            self.board.clear()
            # 回退两步
            self.stack.pop()
            self.board = self.stack.pop()

    def chessmanChoose(self, row, col):
        ''' 选中棋子 '''

        if row >= 0 and col >= 0 and (row, col) in self.board.keys():
            if self.board[(row, col)] != None:
                self.curRow = row
                self.curCol = col
                self.moveSteps = 1

                left = self.curCol * BOARD_GAP + BOARD_LEFT
                top = self.curRow * BOARD_GAP + BOARD_TOP
                self.window.blit(self.markImg, (left, top))

    def redrawBorad(self):
        ''' 根据每个单元格对应的棋子重绘棋盘 '''

        self.window.fill((0,0,0))
        self.window.blit(self.groundImg, (0, 0))

        # 显示所有棋子
        for key in self.board.keys():
            chessman = self.board[key]
            if chessman == None:
                continue;
            left = chessman.col * BOARD_GAP + BOARD_LEFT
            top = chessman.row * BOARD_GAP + BOARD_TOP
            image, rc = chessman.getImage()
            if None == image:
                continue
            self.window.blit(image, (left, top))
            if self.curRow == chessman.row and self.curCol == chessman.col:
                self.window.blit(self.markImg, (left, top))

        Button.refresh()

    def showTipInfo(self):
        ''' 在棋盘底部显示提示信息 '''

        # 把文字显示到窗口上
        text, textpos = load_font(self.tipInfo)
        # textpos.centerx = self.window.get_rect().centerx
        textpos = Rect(0, 532, 460, 28)
        self.window.blit(text, textpos)

    def moveChessColorJudge(self, row, col):
        ''' 走棋颜色判断
        判断当前选中棋子是否和允许下的棋子颜色相同,不同不允许走棋
        '''

        if (row, col) in self.board.keys():
            chessman = self.board[(row, col)]
            if None != chessman:
                if chessman.color != self.curStepColor:
                    if CHESSMAN_COLOR_BLACK == chessman.color :
                        self.tipInfo = ('It is red turn')
                    else:
                        self.tipInfo = ('It is black turn')
                    return  0
        return 1

    def moveChess(self, rowTo, colTo):
        ''' 走棋判断,完成走棋,重绘棋盘 '''

        if 0 == self.moveChessColorJudge(rowTo, colTo) and 0 == self.moveSteps:
            # 该对方走棋
            return 0

        if 0 == self.moveSteps:
            # 选择棋子
            self.chessmanChoose(rowTo, colTo)
            return 0
        elif (self.curRow, self.curCol) in self.board.keys():
            # 移动棋子
            chessman = self.board[(self.curRow, self.curCol)]
            chessmanTo = None
            if (rowTo, colTo) in self.board.keys():
                chessmanTo = self.board[(rowTo, colTo)]
                if chessmanTo != None and chessman.color == chessmanTo.color:
                    chessmanTo.printInfo()
                    self.chessmanChoose(rowTo, colTo)
                    return 0
            if chessman == None:
                return 0
            if chessman.ChessMoveJudge(rowTo, colTo) == 1:
                chessman.printInfo()
                print('rowFrom:%d, ColFrom:%d' % (self.curRow, self.curCol))
                print('rowTo:%d,colTo:%d' % (rowTo, colTo))

                # 蹩马脚判断
                if CHESSMAN_KIND_MA == chessman.kind:
                    rowError = 0
                    colError = 0
                    if abs(chessman.row - rowTo) == 1:
                        rowError = chessman.row
                        colError = (chessman.col + colTo) / 2
                    elif abs(chessman.col - colTo) == 1:
                        colError = chessman.col
                        rowError = (chessman.row + rowTo) / 2
                    if (rowError, colError) in self.board.keys() and self.board[(rowError, colError)] != None:
                        return 0

                # 夹心象判断
                if CHESSMAN_KIND_XIANG == chessman.kind:
                    rowError = (chessman.row + rowTo) / 2
                    colError = (chessman.col + colTo) / 2
                    if (rowError, colError) in self.board.keys() and self.board[(rowError, colError)] != None:
                        return 0

                # 车拦路判断,隔山炮判断
                bIsHaveChessman = 0
                if CHESSMAN_KIND_JU == chessman.kind or CHESSMAN_KIND_PAO == chessman.kind:
                    rowLoopMin = 0
                    rowLoopMax = 0
                    colLoopMin = 0
                    colLoopMax = 0
                    if chessman.row == rowTo:
                        rowLoopMin = rowTo
                        rowLoopMax = rowTo + 1
                        if chessman.col > colTo:
                            colLoopMin = colTo+1
                            colLoopMax = chessman.col
                        elif chessman.col < colTo:
                            colLoopMin = chessman.col + 1
                            colLoopMax = colTo
                    if chessman.col == colTo:
                        colLoopMin = colTo
                        colLoopMax = colTo + 1
                        if chessman.row > rowTo:
                            rowLoopMin = rowTo + 1
                            rowLoopMax = chessman.row
                        elif chessman.row < rowTo:
                            rowLoopMin = chessman.row + 1
                            rowLoopMax = rowTo
                    for row in range(rowLoopMin, rowLoopMax):
                        for col in range(colLoopMin, colLoopMax):
                            if (row, col) in self.board.keys():
                                if None != self.board[(row, col)]:
                                    bIsHaveChessman = 1
                                    if CHESSMAN_KIND_PAO == chessman.kind:
                                        if (rowTo, colTo) not in self.board.keys() :
                                            return  0
                                        elif None == self.board[(rowTo, colTo)]:
                                            return 0
                                        else:
                                            chessmanTemp = self.board[(rowTo, colTo)]
                                            if chessmanTemp.color == chessman.color:
                                                return 0
                                    else:
                                        return 0
                if CHESSMAN_KIND_PAO == chessman.kind:
                    if (rowTo, colTo) in self.board.keys() :
                        chessmanTemp = self.board[(rowTo, colTo)]
                        if None == chessmanTemp and  1 == bIsHaveChessman:
                            return 0
                        if None != chessmanTemp and 0 == bIsHaveChessman:
                            return 0
                # 兵:过河
                if chessman.kind == CHESSMAN_KIND_BING:
                    if (4 == chessman.row and 5 == rowTo) or (5 == chessman.row and 4 == rowTo):
                        chessman.riverCrossed = 1
            else:
                if CHESSMAN_KIND_JIANG == chessman.kind:
                    # 白脸将判断
                    if (rowTo, colTo) not in self.board.keys():
                        return 0
                    chessmanTo = self.board[(rowTo, colTo)]
                    if None == chessmanTo:
                        return 0
                    if CHESSMAN_KIND_JIANG != chessmanTo.kind:
                        return 0
                else:
                    return 0

            # 成功走棋
            board_save = copy.deepcopy(self.board)
            self.stack.push(board_save)

            self.board[(rowTo, colTo)] = chessman
            chessman.row = rowTo
            chessman.col = colTo
            self.board[(self.curRow, self.curCol)]  = None
            self.curRow = -1
            self.curCol = -1
            self.moveSteps = 0
            self.tipInfo = ('last moving chessman: %s,row:%d,col:%d' %  (chessman.printInfo(), rowTo, colTo))

            # 换对方下棋
            if self.curStepColor == CHESSMAN_COLOR_BLACK:
                self.curStepColor = CHESSMAN_COLOR_RED
            else:
                self.curStepColor = CHESSMAN_COLOR_BLACK

            if chessmanTo != None and CHESSMAN_KIND_JIANG == chessmanTo.kind:
                if CHESSMAN_COLOR_BLACK == chessmanTo.color:
                    self.tipInfo = ('game over,red win!')
                else :
                    self.tipInfo = ('game over,black win!')
                self.resetBorad()

            return 1
