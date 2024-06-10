from sys import stdin

from caty.plugins import Plugins
from caty.main import main


head = '''
from sys import stdin

from caty.main import main

'''.lstrip()

tpl = r'''
def dump_{ext}():
    try:
        main(stdin, '{ext}')
    except Exception as x:
        print(f'\n ! {{x}} !\n')

'''

def gen():
    exts = [Plugin.ext[0] for Plugin in Plugins]
    with open('dump.py', 'w') as dump, open('../pyproject.toml', 'a') as prj:
        dump.write(head)
        for ext in exts:
            print(ext)
            dump.write(tpl.format(**locals()))
            prj.write(f'caty_{ext} = "caty.dump:dump_{ext}"\n')


if __name__ == '__main__': gen()
