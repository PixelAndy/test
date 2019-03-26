path_to_pic = 'Path to file(tip c://folder/): '
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

# make typle Questions - Answers.
list_of_arg = path_to_pic, name_pic, continue_arg, arg1, arg2, arg3
# make list of name arguments
list_of_name = [path, name, contin, arg11, arg22, arg33]


def which_arg():
    pass


# mail code
if __name__ == '__main__':
    while x < len(list_of_arg):
        list_of_name[x] = input(list_of_arg[x])  # User input path to file
        if x == 1:
            pass  # summ path and name then checking file. if False, x-=2 and print text error

        if x == 2:  # Ask User what he's want do with picture
            if list_of_name[x] == 'y':  # now show him commands
                pass
            elif list_of_name[x] == 'n':  # he's want nothing
                print('thats all, bye')
                break
            else:  # error, enter again
                print('error, you must input only y or n')
                x -= 1
        elif x == 3:  # some work arg1
            pass
        elif x == 4:  # some work arg2
            pass
        elif x == 5:  # some work arg3
            pass
        else:
            pass
        x += 1
