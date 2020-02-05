#-*- encoding: utf-8 -*-
import sys, string, os, copy
import datetime
import pygame

from Common import Structure
from Chess import Base
from Chess import Global
from Chess import Operate
from ai import value as ai_value

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
        self.bottomImg, rc = Global.load_image("images/bottom.bmp")
        self.headerImg, rc = Global.load_image("images/header.bmp")
        self.footerImg, rc = Global.load_image("images/footer.bmp")
        self.groundImg, rc = Global.load_image("images/ground.bmp")
        self.markImg, rc = Global.load_image("images/cur_pos.bmp", 0xffffff)
        self.moveImg, rc = Global.load_image("images/cur_move.bmp", 0xffffff)

        # 操作面板
        self.operatePanel = Operate.Panel(self.window, BOARD_TOP//2, BOARD_WIDTH + BOARD_LEFT)

        # 提示的文本
        self.tipInfo = ''

        # 保存走棋步骤
        self.stack = Structure.Stack()

    def backBorad(self, chessboard):
        """ 回退棋盘 """
        if self.stack.size() == 1:
            chessboard.resetBorad()
        elif self.stack.size() >= 2:
            # 回退一个回合/两步
            self.stack.pop()
            chessboard.board = self.stack.pop()

    def saveBorad(self, board):
        board_save = copy.deepcopy(board)
        self.stack.push(board_save)

    def resetWindow(self):
        self.stack.destroy()


class ChessBoard(object):
    ''' 象棋棋盘类
    数据:每个单元格对应的棋子
    操作:
        1.走棋
        2.重绘棋盘
    '''

    def __init__(self):
        ''' 初始化 '''

        # 走棋步骤: 0-选择棋子  1-移动棋子
        self.moveSteps = 0

        # 当前要走棋的棋子颜色,初始化为红色
        self.curStepColor = Base.COLOR_RED

        # 行位置
        self.curRow = -1

        # 列位置
        self.curCol = -1

        # 棋盘重置
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

    def formatBoard(self):
        board_fmt = [[0] * 9 for i in range(10)]

        for key in self.board.keys():
            chessman = self.board[key]
            if chessman == None:
                continue;
            kind  = Base.chessman_dict[chessman.kind]
            if chessman.color != Base.COLOR_RED:
                kind = kind.lower()
            board_fmt[key[0]][key[1]] = kind
        return board_fmt

    def resetBorad(self):
        """ 重置棋盘 """

        self.moveSteps = 0
        self.curStepColor = Base.COLOR_RED
        self.curRow = -1
        self.curCol = -1
        self.board = {
                (9, 8):Base.Chessman(Base.KIND_JU, Base.COLOR_RED,      9, 8),
                (9, 7):Base.Chessman(Base.KIND_MA, Base.COLOR_RED,      9, 7),
                (9, 6):Base.Chessman(Base.KIND_XIANG, Base.COLOR_RED,   9, 6),
                (9, 5):Base.Chessman(Base.KIND_SHI, Base.COLOR_RED,     9, 5),
                (9, 4):Base.Chessman(Base.KIND_JIANG, Base.COLOR_RED,   9, 4),
                (9, 3):Base.Chessman(Base.KIND_SHI, Base.COLOR_RED,     9, 3),
                (9, 2):Base.Chessman(Base.KIND_XIANG, Base.COLOR_RED,   9, 2),
                (9, 1):Base.Chessman(Base.KIND_MA, Base.COLOR_RED,      9, 1),
                (9, 0):Base.Chessman(Base.KIND_JU, Base.COLOR_RED,      9, 0),
                (0, 8):Base.Chessman(Base.KIND_JU, Base.COLOR_BLACK,    0, 8),
                (0, 7):Base.Chessman(Base.KIND_MA, Base.COLOR_BLACK,    0, 7),
                (0, 6):Base.Chessman(Base.KIND_XIANG, Base.COLOR_BLACK, 0, 6),
                (0, 5):Base.Chessman(Base.KIND_SHI, Base.COLOR_BLACK,   0, 5),
                (0, 4):Base.Chessman(Base.KIND_JIANG, Base.COLOR_BLACK, 0, 4),
                (0, 3):Base.Chessman(Base.KIND_SHI, Base.COLOR_BLACK,   0, 3),
                (0, 2):Base.Chessman(Base.KIND_XIANG, Base.COLOR_BLACK, 0, 2),
                (0, 1):Base.Chessman(Base.KIND_MA, Base.COLOR_BLACK,    0, 1),
                (0, 0):Base.Chessman(Base.KIND_JU, Base.COLOR_BLACK,    0, 0),
                (7, 7):Base.Chessman(Base.KIND_PAO, Base.COLOR_RED,     7, 7),
                (7, 1):Base.Chessman(Base.KIND_PAO, Base.COLOR_RED,     7, 1),
                (2, 7):Base.Chessman(Base.KIND_PAO, Base.COLOR_BLACK,   2, 7),
                (2, 1):Base.Chessman(Base.KIND_PAO, Base.COLOR_BLACK,   2, 1),
                (6, 8):Base.Chessman(Base.KIND_BING, Base.COLOR_RED,    6, 8),
                (6, 6):Base.Chessman(Base.KIND_BING, Base.COLOR_RED,    6, 6),
                (6, 4):Base.Chessman(Base.KIND_BING, Base.COLOR_RED,    6, 4),
                (6, 2):Base.Chessman(Base.KIND_BING, Base.COLOR_RED,    6, 2),
                (6, 0):Base.Chessman(Base.KIND_BING, Base.COLOR_RED,    6, 0),
                (3, 8):Base.Chessman(Base.KIND_BING, Base.COLOR_BLACK,  3, 8),
                (3, 6):Base.Chessman(Base.KIND_BING, Base.COLOR_BLACK,  3, 6),
                (3, 4):Base.Chessman(Base.KIND_BING, Base.COLOR_BLACK,  3, 4),
                (3, 2):Base.Chessman(Base.KIND_BING, Base.COLOR_BLACK,  3, 2),
                (3, 0):Base.Chessman(Base.KIND_BING, Base.COLOR_BLACK,  3, 0),
                }

    def chessmanChoose(self, win, row, col):
        ''' 选中棋子 '''

        if row >= 0 and col >= 0 and (row, col) in self.board.keys():
            if self.board[(row, col)] != None:
                self.curRow = row
                self.curCol = col
                self.moveSteps = 1

                left = self.curCol * BOARD_GAP + BOARD_LEFT
                top = self.curRow * BOARD_GAP + BOARD_TOP
                win.window.blit(win.markImg, (left, top))

    def redrawBorad(self, win):
        ''' 根据每个单元格对应的棋子重绘棋盘 '''

        win.window.fill((0,0,0))
        win.window.blit(win.bottomImg, (0, 0))
        win.window.blit(win.headerImg, (30, 20))
        win.window.blit(win.groundImg, (30, 30))
        win.window.blit(win.footerImg, (30, 550))

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
            win.window.blit(image, (left, top))
            if self.curRow == chessman.row and self.curCol == chessman.col:
                win.window.blit(win.markImg, (left, top))

        # 提示可走路径
        for pos in self.chessmanGetPoints():
            top = pos[0] * BOARD_GAP + BOARD_TOP
            left = pos[1] * BOARD_GAP + BOARD_LEFT
            win.window.blit(win.moveImg, (left, top))
        # 刷新操作面板
        win.operatePanel.refresh()

    def showTipInfo(self, win):
        ''' 在棋盘底部显示提示信息 '''

        # 把文字显示到窗口上
        text, textpos = Global.load_font(win.tipInfo)
        # textpos.centerx = win.window.get_rect().centerx
        textpos = pygame.locals.Rect(BOARD_COL, BOARD_ROW + BOARD_HEIGHT + 20, 460, 28)
        # 显示内容
        pygame.draw.rect(win.window, (255,255,255), textpos, 0)
        # 显示边框
        #  pygame.draw.rect(win.window, (105,105,105), textpos, 1)
        win.window.blit(text, textpos)

    def moveChessColorJudge(self, win,row, col):
        ''' 走棋颜色判断
        判断当前选中棋子是否和允许下的棋子颜色相同,不同不允许走棋
        '''

        if (row, col) in self.board.keys():
            chessman = self.board[(row, col)]
            if None != chessman:
                if chessman.color != self.curStepColor:
                    if Base.COLOR_BLACK == chessman.color :
                        win.tipInfo = ('It is red turn')
                    else:
                        win.tipInfo = ('It is black turn')
                    return  0
        return 1

    def chessmanGetPoints(self):
        points = []
        if (self.curRow, self.curCol) not in self.board.keys():
            return points
        chessman = self.board[(self.curRow, self.curCol)]
        if chessman == None:
            return points
        for pos in chessman.getMovePoints():
            if self.chessmanTryMove(pos[0], pos[1]) == True:
                points.append(pos)
        #  print(points)
        return points

    def chessmanTryMove(self, rowTo, colTo):
        if (self.curRow, self.curCol) not in self.board.keys():
            return False

        chessman = self.board[(self.curRow, self.curCol)]
        if chessman == None:
            return False

        chessmanTo = None
        if (rowTo, colTo) in self.board.keys():
            chessmanTo = self.board[(rowTo, colTo)]
            if chessmanTo != None and chessman.color == chessmanTo.color:
                return False

        if chessman.ChessMoveJudge(rowTo, colTo) == 0:
            # 白脸将判断
            if Base.KIND_JIANG == chessman.kind:
                if (rowTo, colTo) not in self.board.keys():
                    return False
                chessmanTo = self.board[(rowTo, colTo)]
                if None == chessmanTo:
                    return False
                if Base.KIND_JIANG != chessmanTo.kind:
                    return False
                if colTo != chessman.col:
                    return False
                for key in self.board.keys():
                    chsman = self.board[key]
                    if chsman == None:
                        continue
                    if chsman.col == colTo:
                        if ((chsman.row > chessman.row and chsman.row < rowTo) or
                            (chsman.row < chessman.row and chsman.row > rowTo)):
                                return False
            else:
                return False
        else:
            # 蹩马脚判断
            if Base.KIND_MA == chessman.kind:
                rowError = 0
                colError = 0
                if abs(chessman.row - rowTo) == 1:
                    rowError = chessman.row
                    colError = (chessman.col + colTo) / 2
                elif abs(chessman.col - colTo) == 1:
                    colError = chessman.col
                    rowError = (chessman.row + rowTo) / 2
                if (rowError, colError) in self.board.keys() and self.board[(rowError, colError)] != None:
                    return False
            # 夹心象判断
            if Base.KIND_XIANG == chessman.kind:
                rowError = (chessman.row + rowTo) / 2
                colError = (chessman.col + colTo) / 2
                if (rowError, colError) in self.board.keys() and self.board[(rowError, colError)] != None:
                    return False
            # 车拦路判断,隔山炮判断
            bIsHaveChessman = 0
            if Base.KIND_JU == chessman.kind or Base.KIND_PAO == chessman.kind:
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
                                if Base.KIND_PAO == chessman.kind:
                                    if bIsHaveChessman == 0:
                                        bIsHaveChessman = 1
                                    else:
                                        return False
                                    if (rowTo, colTo) not in self.board.keys() :
                                        return False
                                    elif None == self.board[(rowTo, colTo)]:
                                        return False
                                    else:
                                        chessmanTemp = self.board[(rowTo, colTo)]
                                        if chessmanTemp.color == chessman.color:
                                            return False
                                else:
                                    return False
            if Base.KIND_PAO == chessman.kind:
                if (rowTo, colTo) in self.board.keys() :
                    chessmanTemp = self.board[(rowTo, colTo)]
                    if bIsHaveChessman == 1 and chessmanTemp == None:
                        return False
                    if bIsHaveChessman == 0 and chessmanTemp != None:
                        return False
        return True

    def aiMoveChess(self, cur_pos, to_pos):
        ''' ai走棋, 简化了走棋的判断'''
        (curRow, curCol) = cur_pos
        (rowTo, colTo) = to_pos

        # 选中棋子
        self.curRow = curRow
        self.curCol = curCol
        self.moveSteps = 1

        # 走棋
        chessman = self.board[(self.curRow, self.curCol)]
        chessman.row = rowTo
        chessman.col = colTo
        self.board[(rowTo, colTo)] = chessman

        self.board.pop((self.curRow, self.curCol))
        self.curRow = -1
        self.curCol = -1
        self.moveSteps = 0
        # 换对方下棋
        if self.curStepColor == Base.COLOR_BLACK:
            self.curStepColor = Base.COLOR_RED
        else:
            self.curStepColor = Base.COLOR_BLACK

    def moveChess(self, win, rowTo, colTo):
        ''' 走棋判断,完成走棋,重绘棋盘 '''

        if 0 == self.moveChessColorJudge(win, rowTo, colTo) and 0 == self.moveSteps:
            # 该对方走棋
            return 0

        if 0 == self.moveSteps:
            # 选择棋子
            self.chessmanChoose(win, rowTo, colTo)
            return 0
        else:
            chessman = None
            if (self.curRow, self.curCol) in self.board.keys():
                chessman = self.board[(self.curRow, self.curCol)]
            if chessman == None:
                return 0
            chessmanTo = None
            if (rowTo, colTo) in self.board.keys():
                chessmanTo = self.board[(rowTo, colTo)]
                if chessmanTo != None and chessman.color == chessmanTo.color:
                    self.chessmanChoose(win, rowTo, colTo)
                    return 0


            # 判断是否能走棋
            if self.chessmanTryMove(rowTo, colTo) == False:
                return 0

            # 走棋
            win.saveBorad(self.board)

            # 兵过河
            if chessman.kind == Base.KIND_BING:
                if (4 == chessman.row and 5 == rowTo) or (5 == chessman.row and 4 == rowTo):
                    chessman.riverCrossed = 1
            chessman.row = rowTo
            chessman.col = colTo
            self.board[(rowTo, colTo)] = chessman

            self.board.pop((self.curRow, self.curCol))
            self.curRow = -1
            self.curCol = -1
            self.moveSteps = 0
            win.tipInfo = ('last moving chessman: %s,row:%d,col:%d' %  (chessman.printInfo(), rowTo, colTo))

            # 换对方下棋
            if self.curStepColor == Base.COLOR_BLACK:
                self.curStepColor = Base.COLOR_RED
            else:
                self.curStepColor = Base.COLOR_BLACK

            if chessmanTo != None and Base.KIND_JIANG == chessmanTo.kind:
                if Base.COLOR_BLACK == chessmanTo.color:
                    win.tipInfo = ('game over,red win!')
                else :
                    win.tipInfo = ('game over,black win!')
                self.resetBorad()

            return 1


def get_all_possible_steps(chessboard):
    points = {}
    chessboard_copy = copy.deepcopy(chessboard)

    for (row, col) in chessboard_copy.board.keys():
        chessman = chessboard_copy.board[(row, col)]
        if None != chessman:
            if chessman.color == chessboard_copy.curStepColor:
                points[(row, col)] = None

    if len(points):
        for (row, col) in points.keys():
            chessboard_copy.curRow = row
            chessboard_copy.curCol = col
            points[(row, col)] = chessboard_copy.chessmanGetPoints()
    return points


def chessboard_evaluate(chessboard):
    board_fmt = chessboard.formatBoard()
    value_all = ai_value.chessman_get_value_all(board_fmt)
    return value_all


def chessboard_ai_move(chessboard, cur_pos, to_pos):
    chessboard.aiMoveChess(cur_pos, to_pos)
