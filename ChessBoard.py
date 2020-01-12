#-*- encoding: utf-8 -*-

import sys, string, os
import pygame
import datetime
from pygame.locals import *
from ChessGlobal import *
from Chessman import *

import socket

class ChessBoard(object):
    '''
    象棋棋盘类，
    数据：每个单元格对应的棋子  9行9列
    操作：1、走棋 2、重绘棋盘 3、显示提示信息 4、选中棋子后棋子闪烁
    '''
    movesteps = 1  #走棋步骤：0-选择棋子  1-移动棋子
    curTime = datetime.datetime.now()
    #当前要走棋的棋子颜色，初始化为红色
    curStepColor = CHESSMAN_COLOR_RED

    #提示的文本
    tipInfo = ''
    def chessmanChoose(self, row, col):
        '''
        选中棋子后，棋子闪烁
        '''
        if row >= 0 and col >= 0 and (row, col) in self.board.keys():
            if self.board[(row, col)] != None:
                self.curRow = row
                self.curCol = col
                self.curTime = datetime.datetime.now()
                self.movesteps = 1

    def __init__(self):
        '''
        初始化，类似于C++中的构造函数
        '''
        self.curCol = 0
        self.curRow = 0

        self.ground, rc = load_image("./BMP/ground.bmp")
        self.resetBorad()


    def resetBorad(self):
        '''
        重置棋盘
        '''
        self.curRow = 0
        self.curCol = 0
        self.curStepColor = CHESSMAN_COLOR_RED
        self.movesteps = 1
        self.board = {
                (0, 0):Chessman(CHESSMAN_KIND_JU, CHESSMAN_COLOR_RED,      0, 0),
                (0, 1):Chessman(CHESSMAN_KIND_MA, CHESSMAN_COLOR_RED,      0, 1),
                (0, 2):Chessman(CHESSMAN_KIND_XIANG, CHESSMAN_COLOR_RED,   0, 2),
                (0, 3):Chessman(CHESSMAN_KIND_SHI, CHESSMAN_COLOR_RED,     0, 3),
                (0, 4):Chessman(CHESSMAN_KIND_JIANG, CHESSMAN_COLOR_RED,   0, 4),
                (0, 5):Chessman(CHESSMAN_KIND_SHI, CHESSMAN_COLOR_RED,     0, 5),
                (0, 6):Chessman(CHESSMAN_KIND_XIANG, CHESSMAN_COLOR_RED,   0, 6),
                (0, 7):Chessman(CHESSMAN_KIND_MA, CHESSMAN_COLOR_RED,      0, 7),
                (0, 8):Chessman(CHESSMAN_KIND_JU, CHESSMAN_COLOR_RED,      0, 8),
                (9, 0):Chessman(CHESSMAN_KIND_JU, CHESSMAN_COLOR_BLACK,    9, 0),
                (9, 1):Chessman(CHESSMAN_KIND_MA, CHESSMAN_COLOR_BLACK,    9, 1),
                (9, 2):Chessman(CHESSMAN_KIND_XIANG, CHESSMAN_COLOR_BLACK, 9, 2),
                (9, 3):Chessman(CHESSMAN_KIND_SHI, CHESSMAN_COLOR_BLACK,   9, 3),
                (9, 4):Chessman(CHESSMAN_KIND_JIANG, CHESSMAN_COLOR_BLACK, 9, 4),
                (9, 5):Chessman(CHESSMAN_KIND_SHI, CHESSMAN_COLOR_BLACK,   9, 5),
                (9, 6):Chessman(CHESSMAN_KIND_XIANG, CHESSMAN_COLOR_BLACK, 9, 6),
                (9, 7):Chessman(CHESSMAN_KIND_MA, CHESSMAN_COLOR_BLACK,    9, 7),
                (9, 8):Chessman(CHESSMAN_KIND_JU, CHESSMAN_COLOR_BLACK,    9, 8),
                (2, 1):Chessman(CHESSMAN_KIND_PAO, CHESSMAN_COLOR_RED,     2, 1),
                (2, 7):Chessman(CHESSMAN_KIND_PAO, CHESSMAN_COLOR_RED,     2, 7),
                (7, 1):Chessman(CHESSMAN_KIND_PAO, CHESSMAN_COLOR_BLACK,   7, 1),
                (7, 7):Chessman(CHESSMAN_KIND_PAO, CHESSMAN_COLOR_BLACK,   7, 7),
                (3, 0):Chessman(CHESSMAN_KIND_BING, CHESSMAN_COLOR_RED,    3, 0),
                (3, 2):Chessman(CHESSMAN_KIND_BING, CHESSMAN_COLOR_RED,    3, 2),
                (3, 4):Chessman(CHESSMAN_KIND_BING, CHESSMAN_COLOR_RED,    3, 4),
                (3, 6):Chessman(CHESSMAN_KIND_BING, CHESSMAN_COLOR_RED,    3, 6),
                (3, 8):Chessman(CHESSMAN_KIND_BING, CHESSMAN_COLOR_RED,    3, 8),
                (6, 0):Chessman(CHESSMAN_KIND_BING, CHESSMAN_COLOR_BLACK,  6, 0),
                (6, 2):Chessman(CHESSMAN_KIND_BING, CHESSMAN_COLOR_BLACK,  6, 2),
                (6, 4):Chessman(CHESSMAN_KIND_BING, CHESSMAN_COLOR_BLACK,  6, 4),
                (6, 6):Chessman(CHESSMAN_KIND_BING, CHESSMAN_COLOR_BLACK,  6, 6),
                (6, 8):Chessman(CHESSMAN_KIND_BING, CHESSMAN_COLOR_BLACK,  6, 8),
                }

    def redrawBorad(self, window):
        '''
        根据每个单元格对应的棋子重绘棋盘
        '''
        window.fill((0,0,0))
        window.blit(self.ground, (0, 0))
        self.window = window
        #显示所有棋子
        for key in self.board.keys():
            chessman = self.board[key]
            if chessman == None:
                continue;
            left = chessman.col * 50 + 5
            top = chessman.row * 50 + 15
            image, rc = chessman.getImage()
            if None == image:
                continue
            if self.curRow == chessman.row and self.curCol == chessman.col:
                curTime = datetime.datetime.now()
                if (curTime - self.curTime).microseconds >= 100000:
                    window.blit(image, (left, top))
                if (curTime - self.curTime).microseconds >= 500000:
                    self.curTime = curTime
            else:
                window.blit(image, (left, top))

    def showTipInfo(self, window):

        '''
        在棋盘底部显示提示信息
        '''
        # 把文字显示到window上
        text, textpos = load_font(self.tipInfo)
        #textpos.centerx = window.get_rect().centerx
        textpos = Rect(0,532, 460, 28)
        window.blit(text, textpos)


    def moveChessColorJudge(self, row, col):
        '''
        判断当前选中棋子是否和允许下的棋子颜色相同，不同不允许走棋
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
        '''
        走棋判断，完成走棋，重绘棋盘
        '''
        if 0 == self.moveChessColorJudge(rowTo, colTo) and 0 == self.movesteps:
            #该对方走棋
            return 0
        if 0 == self.movesteps:
            self.chessmanChoose(rowTo, colTo)
        elif (self.curRow, self.curCol) in self.board.keys():
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

                #别脚马判断
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

                #夹心象判断
                if CHESSMAN_KIND_XIANG == chessman.kind:
                    rowError = (chessman.row + rowTo) / 2
                    colError = (chessman.col + colTo) / 2
                    if (rowError, colError) in self.board.keys() and self.board[(rowError, colError)] != None:
                        return 0

                #车拦路判断,隔山炮判断
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
                # 兵：过河
                if chessman.kind == CHESSMAN_KIND_BING:
                    if (4 == chessman.row and 5 == rowTo) or (5 == chessman.row and 4 == rowTo):
                        chessman.riverCrossed = 1
            elif CHESSMAN_KIND_JIANG == chessman.kind:
                #将判断
                if (rowTo, colTo) not in self.board.keys():
                    return 0
                chessmanTo = self.board[(rowTo, colTo)]
                if None == chessmanTo:
                    return 0
                if CHESSMAN_KIND_JIANG != chessmanTo.kind:
                    return 0
            else:
                return 0
            #成功走棋

            self.board[(rowTo, colTo)] = chessman
            chessman.row = rowTo
            chessman.col = colTo
            self.board[(self.curRow, self.curCol)]  = None
            self.curRow = -1
            self.curCol = -1
            self.movesteps = 0
            self.tipInfo = ('last moving chessman: %s,row:%d,col:%d' %  (chessman.printInfo(), rowTo, colTo))

            #换方下棋
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
