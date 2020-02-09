#-*- encoding: utf-8 -*-
import sys, string, os, time
import pygame
from pygame.locals import *

from widget.window import ChessWindow
from widget.window import BOARD_TOP, BOARD_LEFT, BOARD_GAP


def main():
    # 初始化
    pygame.init()

    # 设置窗口标题
    pygame.display.set_caption('Chinese Chess')

    pygame.event.set_blocked([MOUSEMOTION])
    pygame.event.set_allowed([QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP])

    # 窗口
    chesswindow = ChessWindow()

    # 操作面板按钮初始化
    args = {"window": chesswindow}
    chesswindow.oper_panel.button_init(args)

    chesswindow.redraw_borad()

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
            row = (yPos - BOARD_TOP) // BOARD_GAP
            col = (xPos - BOARD_LEFT) // BOARD_GAP
            mouse = pygame.mouse.get_pressed()
            if (row >= 0 and row <= 9) and (col >= 0 and col <= 8): # 鼠标点击在棋盘内
                if not mouse[0]:
                    print("press: (%d, %d)" %(row, col))
                    chesswindow.move_chessman(row, col)
            else:
                chesswindow.oper_panel.button_process((xPos, yPos), mouse)
        else:
            print("press othre key: %s" % event.type)

        chesswindow.redraw_borad()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
