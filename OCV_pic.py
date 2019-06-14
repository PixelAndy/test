from matplotlib import pyplot as plt
from os.path import dirname, splitext, join
import numpy as np
import argparse
import sys
from cv2 import imread, imwrite, COLOR_BGR2GRAY, cvtColor, equalizeHist
from cv2 import erode, dilate, MORPH_OPEN, MORPH_CLOSE, MORPH_TOPHAT
from cv2 import MORPH_BLACKHAT, MORPH_GRADIENT, morphologyEx, ADAPTIVE_THRESH_MEAN_C
from cv2 import threshold, THRESH_BINARY, THRESH_BINARY_INV, THRESH_TRUNC, THRESH_OTSU
from cv2 import THRESH_TOZERO, THRESH_TOZERO_INV, ADAPTIVE_THRESH_GAUSSIAN_C
from cv2 import adaptiveThreshold, COLOR_BGR2HSV, bitwise_and, ximgproc, bitwise_not
import cv2


def Main():
    parser = argparse.ArgumentParser(description='Read all arguments')
    parser.add_argument('path', type=str,
                        help='Path to picture')
    parser.add_argument('-i', '--info', action='store_true',
                        help='View width, height and count layers')
    parser.add_argument('-c', '--c2g', nargs='?', const='no_name',
                        help='Converting color to gray scale, need Name, example: -c some_name')
    parser.add_argument('-ib', '--ibp', nargs='?', const='1x1',
                        help='View info in set pixel, example: -ib 1x1')
    parser.add_argument('-hs', '--hstg', action='store_true',
                        help='Make histogramm')
    parser.add_argument('-m', '--mopt', action='store_true',
                        help='Make morfologic operation')
    parser.add_argument('-b', '--bpic', action='store_true',
                        help='Make binary picture')
    parser.add_argument('-s', '--segt', action='store_true',
                        help='Make segmentation picture')
    args = parser.parse_args()
    file = check_path(args.path)
    path_to_file = args.path
    do_something = False
    what_to_do = {
        'info': viewinfo,
        'hstg': histogr,
        'mopt': morf_op,
        'bpic': bin_pic,
        'segt': segmentat,
    }
    kwargs = {
        'pic': file,
        'path': path_to_file,
        'points': args.ibp,
        'name': args.c2g,
    }
    in_dict = args.__dict__
    for key in in_dict:
        if in_dict[key] == True:
            what_to_do[key](**kwargs)
            do_something = True

    if args.c2g != None:
        color2gray(**kwargs)
        do_something = True
    if args.ibp != None:
        infoByPixel(**kwargs)
        do_something = True
    if do_something != True:
        helpinfo('Need some arguments')


def helpinfo(error, **kwargs):
    print('''
    How to usage!

    Example: ocv_pic.py c:\\folder\\someName.jpg -i --ibp 10x5 --c2g name

    Full list of arguments:
    -i        - view width, height and count layers
    -c name   - converting picture to gray color, set new name for gray picture
    -ib 15x25 - view info in set pixel x:y
    -hs       - make histogram picture
    -m        - morfologic operations
    -b        - binary picture
    -s        - segmentation picture

    Problem: {}
    '''.format(error))
    sys.exit()


def infoByPixel(pic, points, **kwargs):  # view info in adress of picture
    adrs = points.split('x')
    data = np.array(pic)
    if len(adrs) == 2 and adrs[0].isdigit() and adrs[1].isdigit():
        xmax = pic.shape[0]
        ymax = pic.shape[1]
        x = int(adrs[0])
        y = int(adrs[1])
        print(data[x][y]) if 0 < x < xmax and 0 < y < ymax else helpinfo('out of value in ibp')
    else:
        helpinfo('wrong value in ibp')


def color2gray(pic, name, path, **kwargs):  # Try convert color picture to gray color
    if len(pic.shape) == 2:
        print('picture already gray')
        return
    conv2gray = cvtColor(pic, COLOR_BGR2GRAY)
    dirPath = dirname(path)
    ext = splitext(path)[1]
    save = join(dirPath, name + ext)
    imwrite(save, conv2gray)


def viewinfo(pic, **kwargs):  # Read info picture, size and layers
    x = pic.shape
    if len(x) > 2:
        print('Hight = {} pxls\nWidth = {} pxls\nLayers = {}'.format(*x))
    else:
        print('Hight = {} pxls\nWidth = {} pxls\nLayers = 1'.format(*x))


def histogr(pic, **kwargs):
    if len(pic.shape) > 2:
        pic = cvtColor(pic, COLOR_BGR2GRAY)
    eqw_pic = equalizeHist(pic)
    plt.imshow(eqw_pic, cmap="gray")
    plt.show()


def morf_op(pic, **kwargs):
    if len(pic.shape) > 2:
        pic = cvtColor(pic, COLOR_BGR2GRAY)
    fig, ax = plt.subplots(2, 4, figsize=(7, 8))
    ax = ax.ravel()
    kernel = np.ones((5, 5), np.uint8)
    img = [pic]
    img.append(erode(pic, kernel, iterations=1))
    img.append(dilate(pic, kernel, iterations=1))
    mor = [MORPH_OPEN, MORPH_CLOSE, MORPH_TOPHAT, MORPH_BLACKHAT, MORPH_GRADIENT]
    for m in mor:
        img.append(morphologyEx(pic, m, kernel))
    titles = ['original', 'erosion', 'dilation', 'opening', 'closing', 'white tophat', 'black tophat', 'gradient']
    c = 0
    for image in img:
        ax[c].imshow(image, cmap='gray')
        ax[c].set_title(titles[c])
        ax[c].axis('off')
        c += 1
    plt.show()


def bin_pic(pic, **kwargs):
    if len(pic.shape) > 2:
        pic = cvtColor(pic, COLOR_BGR2GRAY)
    fig, ax = plt.subplots(2, 4, figsize=(7, 8))
    ax = ax.ravel()
    img = [pic]
    thresh = [THRESH_TOZERO, THRESH_TOZERO_INV, THRESH_BINARY, THRESH_BINARY_INV, THRESH_TRUNC]
    for i in thresh:
        ret, img_ = threshold(pic, 127, 255, i)
        img.append(img_)
    s_title = ['original', 'to zero', 'to zero inv', 'binary', 'binary inv',
               'trunc', 'adaptive mean', 'adaptive gaussian']
    img.append(adaptiveThreshold(pic, 255, ADAPTIVE_THRESH_MEAN_C, THRESH_BINARY, 11, 2))
    img.append(adaptiveThreshold(pic, 255, ADAPTIVE_THRESH_GAUSSIAN_C, THRESH_BINARY, 11, 2))
    b = 0
    for image in img:
        ax[b].imshow(image, cmap='gray')
        ax[b].set_title(s_title[b])
        ax[b].axis('off')
        b += 1
    plt.show()


def segmentat(pic, **kwargs):
    orig_pic = cvtColor(pic, cv2.COLOR_BGR2RGB)
    converted_img = cvtColor(pic, COLOR_BGR2HSV)
    result = [orig_pic]
    region_size = 50
    ruler = 20
    num_superpixels = 400
    num_iterations = 5
    prior = 2
    num_levels = 4
    num_hist_bins = 5
    height, width, channels = converted_img.shape
    SL = [0, ximgproc.SLIC, ximgproc.SLICO, ximgproc.MSLIC]
    for s in SL:
        if s == 0:
            seeds = ximgproc.createSuperpixelSEEDS(width, height, channels, num_superpixels, num_levels, prior,
                                                   num_hist_bins)
            seeds.iterate(converted_img, num_iterations)
            mask = seeds.getLabelContourMask(False)
        else:
            slic = ximgproc.createSuperpixelSLIC(converted_img, s, region_size, ruler)
            slic.iterate(num_iterations)
            mask = slic.getLabelContourMask(False)
        color_img = np.zeros(converted_img.shape, np.uint8)
        color_img[:] = (0, 0, 255)
        mask_inv = bitwise_not(mask)
        result_bg = bitwise_and(pic, pic, mask=mask_inv)
        result_fg = bitwise_and(color_img, color_img, mask=mask)
        result_ = cv2.add(result_bg, result_fg)
        result.append(result_)
    fig, ax = plt.subplots(2, 3, figsize=(6, 6))
    ax = ax.ravel()
    result.append(w_shed(pic))
    titles = ['original', 'SEEDS', 'SLIC', 'SLICO', 'MSLIC', 'Watershed']
    c = 0
    for segmen in result:
        ax[c].imshow(segmen)
        ax[c].set_title(titles[c])
        ax[c].axis('off')
        c += 1
    plt.show()


def w_shed(pic):
    gray = cvtColor(pic, COLOR_BGR2GRAY)
    ret, thresh = threshold(gray, 0, 255, THRESH_BINARY + THRESH_OTSU)
    fg = erode(thresh, None, iterations=2)
    bgt = dilate(thresh, None, iterations=3)
    ret, bg = threshold(bgt, 1, 128, 1)
    marker = cv2.add(fg, bg)
    marker32 = np.int32(marker)
    cv2.watershed(pic, marker32)
    m = cv2.convertScaleAbs(marker32)
    ret, thresh = threshold(m, 0, 255, THRESH_BINARY + THRESH_OTSU)
    res = bitwise_and(pic, pic, mask=thresh)
    return res


def check_path(path):
    try:
        data_pic = imread(path)
        return data_pic
    except:
        helpinfo('File not found/support or wrong path')


if __name__ == '__main__':
    Main()
