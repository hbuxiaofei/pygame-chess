#-*- encoding: utf-8 -*-
import sys, string, os
import pygame

from pygame.locals import *


def widget_load_image(name, colorfilter=0xffffff):
    ''' 加载图片 '''

    try:
        image = pygame.image.load(name)
    except pygame.error:
        print("Cannot load image: %s" % name)
        return None
    image = image.convert()
    if colorfilter is not None:
        if colorfilter is -1:
            colorfilter = image.get_at((0,0))
        image.set_colorkey(colorfilter, RLEACCEL)
    return image, image.get_rect()


def widget_load_chessman_image():
    chessman_dict = {
            "w_A":None,
            "w_B":None,
            "w_C":None,
            "w_K":None,
            "w_N":None,
            "w_P":None,
            "w_R":None,
            "b_a":None,
            "b_b":None,
            "b_c":None,
            "b_k":None,
            "b_n":None,
            "b_p":None,
            "b_r":None,
            }
    for key in chessman_dict:
        img, rc = widget_load_image("images/%s.bmp" % key, 0xffffff)
        chessman_dict[key] = img
    return chessman_dict


def widget_load_font(txt):
    ''' 加载文字 '''

    # 创建一个字体对象
    # font = pygame.font.Font(u"simsun.ttc", 20)
    font = pygame.font.SysFont(name=None, bold=False, size=25)

    # 生成文字
    text = font.render(txt, True, (255, 0, 0))

    # 取得文字区域大小
    textpos = text.get_rect()

    return text, textpos
