import re
import os
import numpy
import cv2
import skimage

path_to_pic = 'Path to file(tip \'c:\\folder\\\'): '
name_pic = 'File name (tip \'name.jpg\'): '
continue_arg = 'Do you want see command? (tip y/n): '
arg1 = 'View info [size and layers]'  # del
arg2 = 'Apply Command2'  # del
arg3 = 'Apply Command3'  # del
path = 0
name = 0
contin = 0
arg11 = 0
arg22 = 0
arg33 = 0
x = 0
full_path = ''

# make typle Questions - Answers.
list_of_arg = path_to_pic, name_pic, continue_arg, arg1, arg2, arg3
# make list of name arguments
list_of_name = [path, name, contin, arg11, arg22, arg33]


def viewinf(needinfo):  # Read info picture, size and
    x = skimage.io.imread(needinfo).shape
    print('Hight = ' + str(x[0]) + ' pxls\nWidth = ' + str(x[1]) + ' pxls\nLayers = ' + str(x[2]))


def rgb_hsv(): # check pixel RGB or HVS
    pass

def convert_color2gray(param): # Try convert color picture to gray color
    orig_pic = skimage.io.imread(param)
    conv2gray = skimage.color.rgb2gray(orig_pic)
    m = skimage.io.imread(param).shape
    skimage.io.imsave(conv2gray, m)



def check_path(paramtr):  # Now we checking correct path
    if paramtr[-1:] == chr(92):
        return True
    else:
        return False


def check_pic(paramtr):  # Checking correct filename *.jpg
    d = paramtr[-4:]
    if d == '.jpg' or d == '.bmp' or d == '.png':
        return True
    else:
        return False


def check_fullp(paramtr):  # The picture is real? return true\false
    return (os.path.exists(paramtr))


def which_arg(paramtr):  # I think no need to comment this)
    param = paramtr
    print('''Choose parametr:
    1 - View Info (Size And Layers)
    2 - Check PixeL is RGB or HSV
    3 - Convert pic to gray color
    4 - in progress
    5 - in progress
    6 - 6...''')
    choose = input('From 1 to 6: ')
    if choose == '1':
        viewinf(param)
    elif choose == '2':
        pass
    elif choose == '3':
        convert_color2gray(param)
    else:
        print('error, you must input only 1-6 number')


# main code
if __name__ == '__main__':
    while x < len(list_of_arg):
        list_of_name[x] = input(list_of_arg[x])

        if x == 0:  # User input path to file
            if check_path(list_of_name[x]) == False:
                print('incorrect path')
                # x -= 1
                continue

        if x == 1:  # summ path and name then checking file. if False, x-=2 and print text error
            full_path = list_of_name[x - 1] + list_of_name[x]
            if check_pic(list_of_name[x]) == False:  # If filename incorrect then input them again
                print('incorrect file name or extension not supported')
                # x -= 1
                continue
            if check_fullp(full_path) == False:  # If file not found then input path and filename again
                print('I don\'t see \"' + full_path + '\" this file, check path and filename')
                full_path = ''
                x -= 1
                continue

        if x >= 2:  # Ask User what he's want do with picture
            if list_of_name[x] == 'y':  # now show him commands
                which_arg(full_path)
                x -= 1
            elif list_of_name[x] == 'n':  # he's want nothing
                print('thats all, bye')
                break
            else:  # error, enter again
                print('error, you must input only y or n')
                x -= 1
        x += 1