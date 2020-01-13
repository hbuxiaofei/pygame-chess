#-*- encoding: utf-8 -*-
import sys, string, os, time
import pygame
from pygame.locals import *
from ChessBoard import *


def main():
    # 初始化
    pygame.init()
    # 设置窗口大小 图片大小是460*532
    window = pygame.display.set_mode((460, 532 + 28))
    # 设置窗口标题
    pygame.display.set_caption('Chinese Chess')

    pygame.event.set_blocked([MOUSEMOTION])
    pygame.event.set_allowed([QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP])

    # 象棋棋盘类
    chessbord = ChessBoard()

    chessbord.redrawBorad(window)

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

                keyname = pygame.key.get_pressed()
                if keyname[pygame.K_RETURN]:
                    moveResult = chessbord.moveChess(curRow, curCol)
                elif keyname[pygame.K_LEFT]:
                    curCol -= 1
                    if curCol < 0:
                        curCol = 0
                elif keyname[pygame.K_RIGHT]:
                    curCol += 1
                    if curCol > BOARD_MAX_COL:
                        curCol = BOARD_MAX_COL
                elif keyname[pygame.K_UP]:
                    curRow -= 1
                    if curRow < 0:
                        curRow = 0
                elif keyname[pygame.K_DOWN]:
                    curRow += 1
                    if curRow > BOARD_MAX_ROW:
                        curRow = BOARD_MAX_ROW
            else:
                print("press othre key: %s" % event.type)

            leftMouseButton = pygame.mouse.get_pressed()[0]
            if leftMouseButton:
                (xPos, yPos) = pygame.mouse.get_pos()
                curRow = (yPos - BOARD_TOP) // BOARD_GAP
                curCol = (xPos - BOARD_LEFT) // BOARD_GAP
                moveResult = chessbord.moveChess(curRow, curCol)

            chessbord.redrawBorad(window)
            chessbord.showTipInfo(window)

            left = curCol * BOARD_GAP + BOARD_LEFT
            top = curRow * BOARD_GAP + BOARD_TOP
            window.blit(chessbord.markImg, (left, top))

            # 更新显示
            pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
