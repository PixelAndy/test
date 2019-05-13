from matplotlib import pyplot as plt
import os
from os.path import dirname, splitext, join, exists
import numpy as np
from skimage import io, segmentation
from skimage.util import img_as_ubyte
from skimage.future import graph
from skimage.exposure import equalize_hist
from skimage.color import rgb2gray, label2rgb
from skimage.morphology import erosion, disk
from skimage.filters import try_all_threshold
import sys


def helpinfo(error):
    print('''
    How to usage!
    
    Example: pic.py path=c:\\folder\\someName.jpg info ibp=10:5 c2g=name
    
    Full list of arguments:
    path= - (path=c:\\f\\n.jpg) - !!!must be 1st argument!!!, set path
    info  - view width, height and count layers
    c2g=  - (c2g=name) - converting picture to gray color, set new name for gray picture
    help  - view help message
    ibp=  - (ibp=1:1) - view info in set pixel x:y
    hstg  - (histogr) - make histogram picture
    mopt  - (morf_op) - morfologic operations
    bpic  - (bin_pic) - binary picture
    segt  - (segment) - segmentation picture
    
    Problem: {}
    '''.format(error))
    sys.exit()


def infoByPixel(pic, points):  # view info in adress of picture
    adrs = points.split(':')
    data = np.array(pic)
    if len(adrs) == 2 and adrs[0].isdigit() and adrs[1].isdigit():
        xmax = pic.shape[0]
        ymax = pic.shape[1]
        x = int(adrs[0])
        y = int(adrs[1])
        print(data[x][y]) if 0 < x < xmax and 0 < y < ymax else helpinfo('out of value in ibp')
    else:
        helpinfo('wrong value in ibp')


def color2gray(pic, name, path):  # Try convert color picture to gray color
    conv2gray = rgb2gray(pic)
    dirPath = dirname(path)
    ext = splitext(path)[1]
    save = join(dirPath, name + ext)
    io.imsave(save, conv2gray, check_contrastbool=False)


def check_path(path):  # Now we checking correct path, correct extension and existence file
    ext = splitext(path)[1]
    file_ok = exists(path)
    return True if (ext == '.jpg' or ext == '.bmp' or ext == '.png') and file_ok == True else helpinfo(
        'File not found or wrong extension')


def viewinfo(needinfo):  # Read info picture, size and layers
    x = needinfo.shape
    if len(x) > 2:
        print('Hight = {} pxls\nWidth = {} pxls\nLayers = {}'.format(*x))
    else:
        print('Hight = {} pxls\nWidth = {} pxls\nLayers = 1'.format(*x))


def histogr(pictr):
    if len(pictr.shape) > 2:
        pictr = rgb2gray(pictr)
    eqw_pic = equalize_hist(pictr)
    plt.imshow(eqw_pic, cmap="gray")
    plt.show()


def morf_op(pic):
    pic_gray = rgb2gray(pic)
    pic_u = img_as_ubyte(pic_gray)
    selem = disk(10)
    eroded = erosion(pic_u, selem)
    plt.imshow(eroded, cmap='gray')
    plt.show()


def bin_pic(pic):
    pic_gray = rgb2gray(pic)
    fig, ax = try_all_threshold(pic_gray, figsize=(5, 10), verbose=False)
    plt.show()


def segmentat(pic):
    labels1 = segmentation.slic(pic, compactness=30, n_segments=400)
    out1 = label2rgb(labels1, pic, kind='avg')
    g = graph.rag_mean_color(pic, labels1)
    plt.imshow(out1)
   # labels2 = graph.cut_threshold(labels1, g, 29)
   # out2 = label2rgb(labels2, pic, kind='avg')
   # plt.imshow(out2)
    plt.show()

def parser_arguments(all_arguments):  # checking path and after than if ok use argument
    fullpath = all_arguments[1][5:]
    if all_arguments[1][:5] == 'path=' and (len(fullpath)) > 7 and check_path(fullpath):
        data_pic = io.imread(fullpath)
        max_iteration = len(all_arguments)
        for count_arg in range(2, max_iteration):
            if all_arguments[count_arg] == 'info':
                viewinfo(data_pic)
                continue
            elif all_arguments[count_arg][:4] == 'c2g=':
                color2gray(data_pic, all_arguments[count_arg][4:], fullpath)
                continue
            elif all_arguments[count_arg][:4] == 'ibp=':
                infoByPixel(data_pic, all_arguments[count_arg][4:])
                continue
            elif all_arguments[count_arg] == 'hstg':
                histogr(data_pic)
                continue
            elif all_arguments[count_arg] == 'mopt':
                morf_op(data_pic)
                continue
            elif all_arguments[count_arg] == 'bpic':
                bin_pic(data_pic)
                continue
            elif all_arguments[count_arg] == 'segt':
                segmentat(data_pic)
                continue
            elif all_arguments[count_arg] == 'help':
                helpinfo('no problem')
            else:
                helpinfo('wrong argument')
    else:
        helpinfo('wrong path, argument or file not found')


if __name__ == '__main__':
    list_argum = sys.argv
    # ckecking for correct count arguments if not enough go read help
    helpinfo('need more arguments') if len(list_argum) <= 2 else parser_arguments(list_argum)
