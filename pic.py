from matplotlib import pyplot as plt
from os.path import dirname, splitext, join
import numpy as np
import sys
import argparse
from skimage import io, segmentation
from skimage.util import img_as_ubyte
from skimage.future import graph
from skimage.exposure import equalize_hist
from skimage.color import rgb2gray, label2rgb
from skimage.morphology import erosion, disk, dilation, opening, closing, white_tophat, black_tophat
from skimage.filters import (threshold_otsu, threshold_yen,
                             threshold_isodata, threshold_li, threshold_mean,
                             threshold_minimum, threshold_triangle, sobel)


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
    
    Example: pic.py c:\\folder\\someName.jpg -i --ibp 10x5 --c2g name
    
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
    conv2gray = rgb2gray(pic)
    dirPath = dirname(path)
    ext = splitext(path)[1]
    save = join(dirPath, name + ext)
    io.imsave(save, conv2gray, check_contrastbool=False) if ext != '.png' else io.imsave(save, conv2gray)


def viewinfo(pic, **kwargs):  # Read info picture, size and layers
    x = pic.shape
    if len(x) > 2:
        print('Hight = {} pxls\nWidth = {} pxls\nLayers = {}'.format(*x))
    else:
        print('Hight = {} pxls\nWidth = {} pxls\nLayers = 1'.format(*x))


def histogr(pic, **kwargs):
    if len(pic.shape) > 2:
        pic = rgb2gray(pic)
    eqw_pic = equalize_hist(pic)
    plt.imshow(eqw_pic, cmap="gray")
    plt.show()


def morf_op(pic, **kwargs):
    if len(pic.shape) > 2:
        pic = rgb2gray(pic)
    fig, ax = plt.subplots(2, 4, figsize=(7, 8))
    ax = ax.ravel()
    pic_ubyte = img_as_ubyte(pic)
    operations = [pic, erosion, dilation, opening, closing, white_tophat, black_tophat]
    titles = ['original', 'erosion', 'dilation', 'opening', 'closing', 'white tophat', 'black tophat']
    selem = disk(6)
    c = 0
    for op in operations:
        ax[c].imshow(op(pic_ubyte, selem), cmap='gray') if c != 0 else ax[c].imshow(pic_ubyte, cmap='gray')
        ax[c].set_title(titles[c])
        ax[c].axis('off')
        c += 1
    ax[7].axis('off')
    plt.show()


def bin_pic(pic, **kwargs):
    if len(pic.shape) > 2:
        pic = rgb2gray(pic)
    fig, ax = plt.subplots(2, 4, figsize=(7, 8))
    ax = ax.ravel()
    thresholds = th = pic_th = [img_as_ubyte, threshold_minimum, threshold_triangle, threshold_mean,
                                threshold_li, threshold_yen, threshold_otsu, threshold_isodata]
    s_title = ['original', 'minimum', 'triangle', 'mean', 'li', 'yen', 'otsu', 'isodata']
    tr = 0
    for threshold in thresholds:
        th[tr] = threshold(pic)

        if tr != 0:
            pic_th[tr] = pic > th[tr]
        else:
            pic_th[tr] = pic

        ax[tr].imshow(pic_th[tr], cmap='gray')
        ax[tr].set_title(s_title[tr])
        ax[tr].axis('off')
        tr += 1
    plt.show()


def segmentat(pic, **kwargs):
    # if picture not in gray scale (if == 2 then - picture in grayscale and no need check next condition)
    # and if contain alpha channel
    if (len(pic.shape) != 2) and (pic.shape[2] == 4):
        pic_wo_alph = pic[:, :, :3]  # delete alpha
    else:
        pic_wo_alph = pic

    RAG1, RAG2 = RAG_Thresholding(pic_wo_alph)
    rand_w = seg_random_walker(pic_wo_alph)

    img = img_as_ubyte(pic_wo_alph[::2, ::2])

    segments_fz = segmentation.felzenszwalb(img, scale=100, sigma=0.5, min_size=50)
    segments_slic = segmentation.slic(img, n_segments=250, compactness=10, sigma=1)
    segments_quick = segmentation.quickshift(img, kernel_size=3, max_dist=6, ratio=0.5)
    gradient = sobel(rgb2gray(img))
    segments_watershed = segmentation.watershed(gradient, markers=250, compactness=0.001)

    fig, ax = plt.subplots(2, 4, figsize=(7, 8))
    ax = ax.ravel()
    segmentations = [pic_wo_alph, RAG1, RAG2, rand_w, segments_fz, segments_slic, segments_quick, segments_watershed]
    titles = ['original', 'R A G 1', 'R A G 2', 'Random Walker', 'Felzenszwalb', 'Slic', 'Quick', 'Watershed']
    c = 0
    for segmen in segmentations:
        ax[c].imshow(segmentation.mark_boundaries(img, segmen)) if c > 3 else ax[c].imshow(segmen)
        ax[c].set_title(titles[c])
        ax[c].axis('off')
        c += 1
    plt.show()


def RAG_Thresholding(pic):
    labels1 = segmentation.slic(pic, compactness=30, n_segments=400)
    out1 = label2rgb(labels1, pic, kind='avg')
    g = graph.rag_mean_color(pic, labels1)
    labels2 = graph.cut_threshold(labels1, g, 29)
    out2 = label2rgb(labels2, pic, kind='avg')
    return out1, out2


def seg_random_walker(pic):
    pic_wo_alph = img_as_ubyte(pic)
    markers = np.zeros(pic_wo_alph.shape, dtype=np.uint8)
    markers[pic_wo_alph < 250] = 1
    markers[pic_wo_alph > 150] = 2
    labels = segmentation.random_walker(pic_wo_alph, markers)
    out = label2rgb(labels, pic_wo_alph, kind='avg')
    return out


def check_path(path):
    try:
        data_pic = io.imread(path)
        return data_pic
    except:
        helpinfo('File not found/support or wrong path')


if __name__ == '__main__':
    Main()
