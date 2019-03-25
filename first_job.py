path_to_pic = 'Введите путь к изображению: '
name_pic = 'Как называется картинка: '
continue_arg = 'Желаете указать команды? (y/n): '
arg1 = 'Аргумент1: '
arg2 = 'Аргумент2: '
arg3 = 'Аргумент3: '
path = 0
name = 0
contin = 0
arg11 = 0
arg22 = 0
arg33 = 0
x = 0

# создаем кортеж для вопросов - подсказок. Кортеж - потому что его нельзя редактировать, экономия памяти
list_of_arg = path_to_pic, name_pic, continue_arg, arg1, arg2, arg3
# создаем список,  потому что надо будет заносить значения
list_of_name = [path, name, contin, arg11, arg22, arg33]

# это основной цикл
while x < len(list_of_arg):
    list_of_name[x] = input(list_of_arg[x])  # присваиваем списку имени значение которое вводит юзер
    if x == 2:  # проверяем хочет ли юзер что то сделать с изображением
        if list_of_name[x] == 'y':  # если хочет, то принимаем аргумент далее
            pass
        elif list_of_name[x] == 'n':  # если не хочет, то выходим из цикла и ТЗ выполнено
            print('по ТЗ - дальше делать нечего')
            break
        else:  # если допущена ошибка при вводе, то просим ввести еще раз
            print('error')
            print(list_of_name)
            x -= 1
    elif x == 3: # обработка аргумента arg1
        pass
    elif x == 4:# обработка аргумента arg2
        pass
    elif x == 5:# обработка аргумента arg3
        pass
    else:
        pass
    x += 1
