#-*- encoding: utf-8 -*-
import sys, string, os, time
import pygame
from pygame.locals import *

from Chess import Board
from Chess import Operate


def main():
    # 初始化
    pygame.init()
    # 设置窗口大小 图片大小是460*532
    #  window = pygame.display.set_mode((460, 532 + 28 + 50))
    #  window = pygame.display.set_mode((Board.WINDOW_WIDTH, Board.WINDOW_HEIGHT))
    # 设置窗口标题
    pygame.display.set_caption('Chinese Chess')

    pygame.event.set_blocked([MOUSEMOTION])
    pygame.event.set_allowed([QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP])

    # 窗口
    chesswindow = Board.ChessWindow()

    # 象棋棋盘类
    chessbord = Board.ChessBoard()

    # 操作面板按钮初始化
    args = {"window": chesswindow, "board": chessbord}
    chesswindow.operatePanel.button_init(args)

    chessbord.redrawBorad(chesswindow)

    mainloop = True

    # 事件循环
    while mainloop:
        # 更新显示
        pygame.display.update()
        moveResult = 0

        # 等待并从队列中获取一个事件
        event = pygame.event.wait()

        if event.type == pygame.QUIT: # 如果关闭窗口,退出
            print("press pygame.QUIT")
            mainloop = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: # 如果按下Esc键,退出
                print("press pygame.K_ESCAPE")
                mainloop = False
                break
        elif event.type ==  pygame.MOUSEBUTTONDOWN or event.type ==  pygame.MOUSEBUTTONUP:
            (xPos, yPos) = pygame.mouse.get_pos()
            mouse = pygame.mouse.get_pressed()
            if not mouse[0]:
                row = (yPos - Board.BOARD_TOP) // Board.BOARD_GAP
                col = (xPos - Board.BOARD_LEFT) // Board.BOARD_GAP
                if (row >= 0  and row <= 9) and (col >= 0 and col <= 8): # 鼠标点击在棋盘内
                    moveResult = chessbord.moveChess(chesswindow, row, col)
            chesswindow.operatePanel.button_process((xPos, yPos), mouse)
        else:
            print("press othre key: %s" % event.type)

        chessbord.redrawBorad(chesswindow)
        chessbord.showTipInfo(chesswindow)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
