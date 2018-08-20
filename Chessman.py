#-*- encoding: utf-8 -*-

from ChessGlobal import *
import os

class Chessman:
    '''
    棋子基类
    数据成员：棋子类型（车，马。。），棋子颜色（黑，红）,棋子当前行列
    操作：1、仅靠位置判断是否能走棋,不考虑其它棋子的影响   
            2、获得棋子图片对象
    '''

    def getImage(self):
        '''
        根据棋子类型和棋子颜色获得棋子图片对象
        '''
        kind = ""
        if CHESSMAN_KIND_JU == self.kind:
            kind = 'ju'
        if CHESSMAN_KIND_PAO == self.kind:
            kind = 'pao'
        elif CHESSMAN_KIND_MA == self.kind:
            kind = 'ma'
        elif CHESSMAN_KIND_XIANG == self.kind:
            kind = 'xiang'
        elif CHESSMAN_KIND_SHI == self.kind:
            kind = 'shi'
        elif CHESSMAN_KIND_JIANG == self.kind:
            kind = 'jiang'
        elif CHESSMAN_KIND_BING == self.kind:
            kind = 'bing'
        
        color = 'r'
        if CHESSMAN_COLOR_BLACK == self.color:
            color = 'b'

        #print __file__
        curpath = os.path.dirname(__file__)
        #print curpath
        curpath = curpath.replace('ChsChess.exe', '')
        filename = './BMP/' + color + '_' + kind + '.bmp'
        writeErrorLog(filename)
        return load_image(filename)
    
    def __init__(self, kind, color, row, col):
        self.kind  = kind
        self.color = color
        self.row = row
        self.col = col
        self.riverCrossed = 0  #过河判断，用于兵
    
    def printInfo(self):
        arrKind = ('ju', 'ma', 'xiang', 'shi', 'jiang', 'pao', 'bing', 'None')
        arrColor = ('red ', 'black ')
        info = arrColor[self.color] + arrKind[self.kind]
        print info
        return info
    
    def ChessMoveJudge(self, rowTo, colTo):
        '''
        根据棋子类型、当前位置和目标位置判断能否走棋
        '''
        isSuc = 1
        if CHESSMAN_KIND_JU == self.kind or CHESSMAN_KIND_PAO == self.kind:
            isSuc = (self.row == rowTo) or (self.col == colTo)
        elif CHESSMAN_KIND_MA == self.kind:
            rowGap = abs(self.row - rowTo)
            colGap = abs(self.col - colTo)
            isSuc = rowGap > 0 and colGap > 0 and rowGap+colGap == 3
        elif CHESSMAN_KIND_XIANG == self.kind:
            if abs(rowTo-self.row) != 2 or abs(colTo - self.col) != 2:
                isSuc = 0
            if 4 == self.row  and rowTo > 4:
                isSuc = 0
            if 5 == self.row and rowTo < 5:
                isSuc = 0
            
        elif CHESSMAN_KIND_SHI == self.kind:
            if abs(rowTo-self.row) != 1 or abs(colTo - self.col) != 1:
                isSuc = 0
            if colTo < 3 or colTo > 5:
                isSuc = 0
            if self.row < 3 and rowTo >= 3:
                isSuc = 0
            if self.row > 6 and rowTo <6:
                isSuc = 0
        elif CHESSMAN_KIND_JIANG == self.kind:
            if abs(rowTo-self.row) + abs(colTo - self.col) != 1:
                isSuc = 0
            if colTo < 3 or colTo > 5:
                isSuc = 0
            if self.row < 3 and rowTo >= 3:
                isSuc = 0
            if self.row > 6  and rowTo <=6:
                isSuc = 0            
        elif CHESSMAN_KIND_BING == self.kind:
            if abs(rowTo-self.row) + abs(colTo - self.col) != 1:
                isSuc = 0
            if 0 == self.riverCrossed and colTo != self.col:
                isSuc = 0
            if 1 == self.riverCrossed and ((self.row < 5 and self.row < rowTo ) or (self.row > 5 and self.row > rowTo)):
                isSuc = 0
        return isSuc
        
if __name__ == "__main__":

    
    #测试用例
    #ju = Chessman(CHESSMAN_KIND_JU, CHESSMAN_COLOR_RED, 0, 0)
    #print ju.ChessMoveJudge(1, 1)
    #print ju.ChessMoveJudge(1, 0)
    
    
    ma = Chessman(CHESSMAN_KIND_MA, CHESSMAN_COLOR_RED, 2, 2)
    ma.printInfo()
    
    print ma.ChessMoveJudge(1, 2) == 0
    print ma.ChessMoveJudge(4, 1) == 1
    print ma.ChessMoveJudge(4, 2) == 0
    print ma.ChessMoveJudge(4, 3) == 1 
    
    xiang = Chessman(CHESSMAN_KIND_XIANG, CHESSMAN_COLOR_RED, 0, 2)
    
    print xiang.ChessMoveJudge(2, 4) == 1
    print xiang.ChessMoveJudge(2, 0) == 1
    print xiang.ChessMoveJudge(2, 1) == 0
    print xiang.ChessMoveJudge(2, 2) == 0
    
    shi = Chessman(CHESSMAN_KIND_SHI, CHESSMAN_COLOR_RED, 0, 3)
    
    print shi.ChessMoveJudge(1, 4) == 1
    print shi.ChessMoveJudge(1, 5) == 0
    print shi.ChessMoveJudge(2, 0) == 0
    print shi.ChessMoveJudge(3, 1) == 0
    
    jiang = Chessman(CHESSMAN_KIND_JIANG, CHESSMAN_COLOR_RED, 0, 4)
    
    print jiang.ChessMoveJudge(0, 5) == 1
    print jiang.ChessMoveJudge(0, 3) == 1
    print jiang.ChessMoveJudge(1, 4) == 1
    print jiang.ChessMoveJudge(1, 5) == 0
    
    bing = Chessman(CHESSMAN_KIND_BING, CHESSMAN_COLOR_RED, 3, 2)
    
    
