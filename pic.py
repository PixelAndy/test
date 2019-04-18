import re
import os
import numpy
import cv2
import skimage
import sys
import argparse


def createParser():
    parser = argparse.ArgumentParser(
        prog='pic',
        description='''This is my 1st program''',
        add_help=False
    )

    parent_group = parser.add_argument_group(title='Arguments')

    parent_group.add_argument('--help', '-h', action='help', help='Call help')

    subparsers = parser.add_subparsers(dest='command',
                                       title='Possible arguments',
                                       description='This аrguments must be 1st after %(prog)s')

    hello_parser = subparsers.add_parser('hello',
                                         add_help=False,
                                         help='Запуск в режиме "Hello, world!"',
                                         description='''Запуск в режиме "Hello, world!"''')

    hello_group = hello_parser.add_argument_group(title='Параметры')

    hello_group.add_argument('--names', '-n', nargs='+', default=['мир'],
                             help='Список приветствуемых людей',
                             metavar='ИМЯ')

    hello_group.add_argument('--help', '-h', action='help', help='Справка')

    goodbye_parser = subparsers.add_parser('goodbye',
                                           add_help=False,
                                           help='Запуск в режиме "Goodbye, world!"',
                                           description='''В этом режиме программа прощается с миром.''')

    goodbye_group = goodbye_parser.add_argument_group(title='Arguments')

    goodbye_group.add_argument('--count', '-c', type=int, default=1,
                               help='Сколько раз попрощаться с миром',
                               metavar='КОЛИЧЕСТВО')

    goodbye_group.add_argument('--help', '-h', action='help', help='Call help')

    return parser


def run_hello(namespace):
    for name in namespace.names:
        print("Привет, {}!".format(name))


def run_goodbye(namespace):
    for _ in range(namespace.count):
        print("Прощай, мир!")


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])

    print(namespace)

    if namespace.command == "hello":
        run_hello(namespace)
    elif namespace.command == "goodbye":
        run_goodbye(namespace)
    else:
        parser.print_help()