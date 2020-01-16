#-*- encoding: utf-8 -*-
import sys, string, os, time
import pygame
from pygame.locals import *
from ChessBoard import *
import Button


def main():
    # 初始化
    pygame.init()
    # 设置窗口大小 图片大小是460*532
    window = pygame.display.set_mode((460, 532 + 28 + 50))
    # 设置窗口标题
    pygame.display.set_caption('Chinese Chess')

    pygame.event.set_blocked([MOUSEMOTION])
    pygame.event.set_allowed([QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP])

    # 象棋棋盘类
    chessbord = ChessBoard(window)
    Button.init(window, chessbord)

    chessbord.redrawBorad()

    curRow = BOARD_MAX_ROW
    curCol = BOARD_MAX_COL
    mainloop = True

    # 事件循环
    while mainloop:
        # 更新显示
        pygame.display.update()
        for event in pygame.event.get():
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
                    curRow = (yPos - BOARD_TOP) // BOARD_GAP
                    curCol = (xPos - BOARD_LEFT) // BOARD_GAP
                    moveResult = chessbord.moveChess(curRow, curCol)
                Button.process((xPos, yPos), mouse)
            else:
                print("press othre key: %s" % event.type)
                break

        chessbord.redrawBorad()
        chessbord.showTipInfo()
        # 更新显示
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
