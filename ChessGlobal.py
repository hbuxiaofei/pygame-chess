#-*- encoding: utf-8 -*-

import sys, string, os
import pygame
from pygame.locals import *


#象棋游戏相关的全局定义变量
CHESSMAN_COLOR_RED    = 0
CHESSMAN_COLOR_BLACK  = 1

CHESSMAN_KIND_NONE     = -1  # 表示棋盘该位置没有棋子
CHESSMAN_KIND_JU       = 0
CHESSMAN_KIND_MA       = 1
CHESSMAN_KIND_XIANG    = 2
CHESSMAN_KIND_SHI      = 3
CHESSMAN_KIND_JIANG    = 4
CHESSMAN_KIND_PAO      = 5
CHESSMAN_KIND_BING     = 6


# 加载图片
def load_image(name, colorfilter=0xffffff):
    try:
        image = pygame.image.load(name)
    except (pygame.error, message):
        print("Cannot load image: %s" % name)
        raise (SystemExit, message)
        return None
    image = image.convert()
    if colorfilter is not None:
        if colorfilter is -1:
            colorfilter = image.get_at((0,0))
        image.set_colorkey(colorfilter, RLEACCEL)
    return image, image.get_rect()


# 加载文字
def load_font(txt):
    # 创建一个字体对象
    #  font = pygame.font.Font(u"simsun.ttc", 20)
    font = pygame.font.SysFont(None, 25)
    # 生成文字
    text = font.render(txt, 1, (255, 0, 0))
    # 取得文字区域大小
    textpos = text.get_rect()

    return text, textpos

