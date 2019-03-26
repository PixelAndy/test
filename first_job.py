import re
import os

path_to_pic = 'Path to file(tip c:\\folder\): '
name_pic = 'File name (tip name.jpg): '
continue_arg = 'Do you want set command? (tip y/n): '
arg1 = 'Apply Command1(tip 1): '
arg2 = 'Apply Command2(tip 2): '
arg3 = 'Apply Command3(tip 3): '
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


def check_path(paramtr):  # Now we checking correct path
    if paramtr[-1:] == chr(92):
        return True
    else:
        return False


def check_pic(paramtr):  # Checking correct filename *.jpg
    d = re.findall(r'\.\w\w\w\b', paramtr)
    if d == ['.jpg']:
        return True
    else:
        return False


def check_fullp(paramtr):  # The picture is real? return true\false
    return (os.path.exists(paramtr))


def which_arg(paramtr):
    pass


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
            if check_pic(list_of_name[x]) == False:
                print('incorrect file name or extension not supported')
                # x -= 1
                continue
            if check_fullp(full_path) == False:
                print('I don\'t see \"' + full_path + '\" this file, check path and filename')
                full_path = ''
                x -= 1
                continue

        if x == 2:  # Ask User what he's want do with picture
            if list_of_name[x] == 'y':  # now show him commands
                pass
            elif list_of_name[x] == 'n':  # he's want nothing
                print('thats all, bye')
                break
            else:  # error, enter again
                print('error, you must input only y or n')
                x -= 1
        if x == 3:  # some work arg1
            pass
        if x == 4:  # some work arg2
            pass
        if x == 5:  # some work arg3
            pass
        x += 1
