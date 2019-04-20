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
    
    Example: pic.py path=c:\\folder\\someName.jpg ni ibp=10:5 c2g=name
    
    Full list of arguments:
    path= - (path=c:\\f\\n.jpg) - !!!must be 1st argument!!!, set path
    ni    - view width, height and count layers
    c2g   - (c2g=name) - converting picture to gray color, set new name for gray picture
    h     - view help message
    ibp   - (ibp=1:1) - view info in set pixel x:y
    htg   - (histogr) - make histogram picture
    mo    - (morf_op) - morfologic operations
    bp    - (bin_pic) - binary picture
    sgt   - (segment) - segmentation picture
    ''')
    sys.exit()


def infoByPixel(pic, point):  # view info in adress of picture
    z = point.split(':')
    data = np.array(pic)
    if len(z) == 2:
        if z[0].isdigit() and z[1].isdigit():
            xmax = pic.shape[0]
            ymax = pic.shape[1]
            x = int(z[0])
            y = int(z[1])
            print(data[x][y]) if 0 < x < xmax and 0 < y < ymax else print('out of value')
        else:
            print('wrong value in ibp')
    else:
        print('wrong value in ibp')


def color2gray(pic, name, path):  # Try convert color picture to gray color
    conv2gray = skimage.color.rgb2gray(pic)
    dirPath = os.path.dirname(path)
    save = os.path.join(dirPath, name + path[-4:])
    skimage.io.imsave(save, conv2gray, check_contrastbool=False)


def check_path(paath):  # Now we checking correct path, correct extension and existence file
    p = paath[-4:]
    file_ok = os.path.exists(paath)
    return True if (p == '.jpg' or p == '.bmp' or p == '.png') and file_ok == True else helpinfo()


def viewinfo(needinfo):  # Read info picture, size and layers
    x = needinfo.shape
    n_layer = x[2] if len(x) > 2 else 1
    print('Hight = {} pxls\nWidth = {} pxls\nLayers = {}'.format(*x))


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
        data_pic = skimage.io.imread(fullpath)
        for countarg in range(2, c):
            if list[countarg] == 'ni':
                viewinfo(data_pic)
                continue
            elif list[countarg][:4] == 'c2g=':
                color2gray(data_pic, list[countarg][4:], fullpath)
                continue
            elif list[countarg] == 'h':
                helpinfo()
                break
            elif list[countarg][:4] == 'ibp=':
                infoByPixel(data_pic, list[countarg][4:])
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

    # ckecking for correct count arguments if not enough go read help
    helpinfo() if count_argum <= 2 else parser_arguments(list_argum, count_argum)
