#-*- encoding: utf-8 -*-
import sys, string, os
import pygame

from pygame.locals import *


def load_image(name, colorfilter=0xffffff):
    ''' 加载图片 '''

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


def load_font(txt):
    ''' 加载文字 '''

    # 创建一个字体对象
    # font = pygame.font.Font(u"simsun.ttc", 20)
    font = pygame.font.SysFont(name=None, bold=False, size=25)

    # 生成文字
    text = font.render(txt, True, (255, 0, 0))

    # 取得文字区域大小
    textpos = text.get_rect()

    return text, textpos
