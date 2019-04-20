import re
import os
import numpy as np
import cv2
import skimage
import sys
import argparse


def helpinfo():
    print('''
    How to usage!
    
    Example: pic.py path=c:\\folder\\someName.jpg ni ibp c2g
    
    Full list of arguments:
    path= - !!!must be 1st argument!!!, set path
    ni - (needinfo) - view width, height and count layers ni=newname
    c2g - (color2gray) - converting picture to gray color
    h - (help) - view help message
    ibp - (infoByPixel) - view info in set pixel
    htg - (histogr) - make histogram picture
    mo - (morf_op) - morfologic operations
    bp - (bin_pic) - binary picture
    sgt - (segment) - segmentation picture''')
    sys.exit()


def infoByPixel(pic, point):  # view info in adress of picture
    pass


def color2gray(pic, name):  # Try convert color picture to gray color
    orig_pic = skimage.io.imread(pic)
    conv2gray = skimage.color.rgb2gray(orig_pic)
    dirPath = os.path.dirname(pic)
    save = os.path.join(dirPath, name + pic[-4:])
    skimage.io.imsave(save, conv2gray, check_contrastbool=False)


def check_path(paath):  # Now we checking correct path, correct extension and existence file
    p = paath[-4:]
    file_ok = os.path.exists(paath)
    if (p == '.jpg' or p == '.bmp' or p == '.png') and file_ok == True:
        return True
    else:
        helpinfo()


def viewinfo(needinfo):  # Read info picture, size and layers
    x = skimage.io.imread(needinfo).shape
    n_layer = x[2] if len(x) > 2 else 1
    print('Hight = ' + str(x[0]) + ' pxls\nWidth = ' + str(x[1]) + ' pxls\nLayers = ' + str(n_layer))


def histogr():
    pass


def morf_op():
    pass


def bin_pic():
    pass


def segmentat():
    pass


def parser_arguments(list, c):  # checking path and after than if ok use argument
    fullpath = list[1][5:]
    if list[1][:5] == 'path=' and check_path(fullpath) == True:
        for countarg in range(2, c):
            if list[countarg] == 'ni':
                viewinfo(fullpath)
                continue
            elif list[countarg][:4] == 'c2g=':
                color2gray(fullpath, list[countarg][4:])
                continue
            elif list[countarg] == 'h':
                helpinfo()
            elif list[countarg][:4] == 'ibp=':
                infoByPixel(fullpath, list[countarg][4:])
                continue
            elif list[countarg] == 'htg':
                histogr()
                continue
            elif list[countarg] == 'mo':
                morf_op()
                continue
            elif list[countarg] == 'bp':
                bin_pic()
                continue
            elif list[countarg] == 'sgt':
                segmentat()
                continue
            else:
                helpinfo()
    else:
        helpinfo()


if __name__ == '__main__':
    count_argum = len(sys.argv)
    list_argum = sys.argv

    # if too small count of arguments > read help
    if count_argum <= 2:
        helpinfo()
    # else reading all arguments and checking important of them
    else:
        parser_arguments(list_argum, count_argum)
