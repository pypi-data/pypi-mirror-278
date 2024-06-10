from sys import stdin

from caty.main import main


def dump_csv():
    try:
        main(stdin, 'csv')
    except Exception as x:
        print(f'\n ! {x} !\n')


def dump_ini():
    try:
        main(stdin, 'ini')
    except Exception as x:
        print(f'\n ! {x} !\n')


def dump_json():
    try:
        main(stdin, 'json')
    except Exception as x:
        print(f'\n ! {x} !\n')


def dump_pickle():
    try:
        main(stdin, 'pickle')
    except Exception as x:
        print(f'\n ! {x} !\n')


def dump_sqlite():
    try:
        main(stdin, 'sqlite')
    except Exception as x:
        print(f'\n ! {x} !\n')


def dump_toml():
    try:
        main(stdin, 'toml')
    except Exception as x:
        print(f'\n ! {x} !\n')


def dump_txt():
    try:
        main(stdin, 'txt')
    except Exception as x:
        print(f'\n ! {x} !\n')


def dump_yaml():
    try:
        main(stdin, 'yaml')
    except Exception as x:
        print(f'\n ! {x} !\n')


def dump_bin():
    try:
        main(stdin, 'bin')
    except Exception as x:
        print(f'\n ! {x} !\n')


def dump_oct():
    try:
        main(stdin, 'oct')
    except Exception as x:
        print(f'\n ! {x} !\n')


def dump_dec():
    try:
        main(stdin, 'dec')
    except Exception as x:
        print(f'\n ! {x} !\n')


def dump_hex():
    try:
        main(stdin, 'hex')
    except Exception as x:
        print(f'\n ! {x} !\n')


def dump_config():
    try:
        main(stdin, 'config')
    except Exception as x:
        print(f'\n ! {x} !\n')


def dump_html():
    try:
        main(stdin, 'html')
    except Exception as x:
        print(f'\n ! {x} !\n')

