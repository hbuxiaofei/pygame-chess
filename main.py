#-*- encoding: utf-8 -*-
import sys, string, os, time
import pygame
from pygame.locals import *
from ChessBoard import *

def main():
    #初始化
    pygame.init()
    # 设置窗口大小 图片大小是460*532 ，
    window = pygame.display.set_mode((460, 560))
    # 设置窗口标题
    if len(sys.argv) > 1:
        pygame.display.set_caption('Chinese Chess black')
    else:
        pygame.display.set_caption('Chinese Chess red')

    chessbord = ChessBoard()
    chessbord.redrawBorad(window)


    top = 15
    left = 4
    gap = 50

    curRow = 0
    curCol = 0

    #当前光标位置
    curPos, rc = load_image("./BMP/curPos.bmp", 0xffffff)
    window.blit(curPos, (left, top))

    bInit = 1

    pygame.event.set_blocked([MOUSEMOTION])
    pygame.event.set_allowed([QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP])
    mainloop = True

    # 事件循环
    while mainloop:
        # 更新显示
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #如果关闭窗口就退出
                mainloop = False
                print("press pygame.QUIT: %s" % pygame.QUIT)
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:# 如果按下Esc键也退出
                    print("press pygame.K_ESCAPE: %s" % pygame.K_ESCAPE)
                    mainloop = False
                    break

                keyname = pygame.key.get_pressed()
                if keyname[pygame.K_RETURN]:
                    moveResult = chessbord.moveChess(curRow, curCol)
                    print("press pygame.K_RETURN, moveResult:%s" % moveResult)

                if keyname[pygame.K_LEFT]:
                    curCol -= 1
                    left -= gap
                    if left <= 4:
                        left = 4
                        curCol = 0
                if keyname[pygame.K_RIGHT]:
                    left += gap
                    curCol += 1
                    if left >= 400:
                        left = 400
                        curCol = 8

                if keyname[pygame.K_UP]:
                    top -= gap
                    curRow -= 1
                    if top <= 15:
                        top = 15
                        curRow = 0

                if keyname[pygame.K_DOWN]:
                    top += gap
                    curRow += 1
                    if top >= 465:
                        top = 465
                        curRow = 9
            else:
                print("press othre key: %s" % event.type)

            chessbord.redrawBorad(window)
            chessbord.showTipInfo(window)
            window.blit(curPos,(left,top))
            # 更新显示
            pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()


