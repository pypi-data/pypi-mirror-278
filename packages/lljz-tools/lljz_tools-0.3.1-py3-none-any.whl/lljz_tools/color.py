"""
@file   : color.py
@author : jiangmenggui@hosonsoft.com
@data   : 2024/4/2
"""
import re


class _Color:

    def __init__(self, s: str, start, end, name):
        self.raw = s
        self.s = start + s + end
        self.start = start
        self.end = end
        self.name = name

    def __len__(self):
        return self.raw.__len__()

    def __str__(self):
        return self.s.__str__()

    def __repr__(self):
        return self.s.__repr__()

    def __iter__(self):
        return self.raw.__iter__()

    def __add__(self, other):
        return self.s + other

    def __radd__(self, other):
        return other + self.s

    def __format__(self, format_spec):
        return self.start + self.raw.__format__(format_spec) + self.end


class _ColorFactory:

    def __init__(self, name, start, end='\033[0m'):
        self.name = name
        self.start = start
        self.end = end

    def __call__(self, __val: str, /, ):
        return _Color(__val, self.start, self.end, self.name)


class Color:
    UNDERLINE = '\033[4m'
    red = _ColorFactory('red', '\033[91m')
    green = _ColorFactory('green', '\033[92m')
    yellow = _ColorFactory('yellow', '\033[93m')
    blue = _ColorFactory('blue', '\033[94m')
    magenta = _ColorFactory('purple', '\033[95m')
    cyan = _ColorFactory('cyan', '\033[96m')
    white = _ColorFactory('white', '\033[97m')
    thin_red = _ColorFactory('red', '\033[31m')
    thin_green = _ColorFactory('green', '\033[32m')
    thin_yellow = _ColorFactory('yellow', '\033[33m')
    thin_blue = _ColorFactory('blue', '\033[34m')
    thin_magenta = _ColorFactory('purple', '\033[35m')
    thin_cyan = _ColorFactory('cyan', '\033[36m')
    thin_white = _ColorFactory('white', '\033[37m')

    success = green
    fail = red
    warning = yellow

    @classmethod
    def color(cls, __val: str, /, *, style='i u r white on red'):
        colors = ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
        thin_colors = [f'thin_{c}' for c in colors]

        def get_color(color: str, background=False):
            background = 10 if background else 0
            try:
                if color.startswith('thin_'):
                    return thin_colors.index(color) + 30 + background
                return colors.index(color) + 90 + background
            except ValueError as e:
                raise ValueError(f'{color!r} not in {colors}')

        style = re.split(r'\s+', style)
        values = set()
        i = 0
        while i < len(style):
            s = style[i]
            if s == 'i':
                values.add(3)
            elif s == 'u':
                values.add(4)
            elif s == 'r':
                values.add(7)
            elif s == 'b' or s == 'bold':
                values.add(1)
            elif s == 'on':
                next_color = style[i + 1]
                values.add(get_color(next_color, True))
                i += 1
            else:
                values.add(get_color(s))
            i += 1

        return _ColorFactory('color', f'\033[{";".join(map(str, values))}m')(__val)


if __name__ == '__main__':
    print(Color.red('hello world'))
    print(Color.green('hello world'))
    print(Color.yellow('hello world'))
    print(Color.blue('hello world'))
    print(Color.cyan('hello world'))
    print(Color.magenta('hello world'))
    print(Color.white('hello world'))
    print(Color.thin_red('hello world'))
    print(Color.thin_green('hello world'))
    print(Color.thin_yellow('hello world'))
    print(Color.thin_blue('hello world'))
    print(Color.thin_cyan('hello world'))
    print(Color.thin_magenta('hello world'))
    print(Color.thin_white('hello world'))
    print('ni hao ' + Color.red('world') + '!')
    print('|'.join(map(str, [Color.red('hello'), Color.green('world')])))
    print(Color.warning('warning: hello world'))
    print('\033[5;34;46mhello world\033[0m')
    print('=' * 50)
    print(Color.color('hello World', style='bold white on black'))
    print(Color.color('hello World', style='on red'))
    print(Color.color('hello World', style='on green'))
    print(Color.color('hello World', style='on yellow'))
    print(Color.color('hello World', style='on blue'))
    print(Color.color('hello World', style='on magenta'))
    print(Color.color('hello World', style='on cyan'))
    print(Color.color('hello World', style='on white'))
    print('=' * 50)
    print(Color.color('Hello World', style='white i u'))
    pass
