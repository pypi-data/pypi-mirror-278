# coding=utf-8
from typing import Iterable, Any

from .color import _Color, Color


class ConsoleTable:

    def __init__(self, data: Iterable[dict[str, Any]], max_width=100, caption='',
                 caption_color=Color.yellow, title_color=Color.thin_cyan, colorize=True):
        def init_value(val):
            if isinstance(val, str | _Color):
                return val
            if val is None:
                return ''
            return str(val)
        self.colorize = colorize
        self.caption = caption
        self.caption_color = caption_color
        self.title_color = title_color
        self.data = [{str(k): init_value(v) for k, v in row.items()} for row in data]
        self.header = list(self.data[0].keys()) if data else []
        self.max_width = max_width
        self.col_width = []
        self._table_str = ""
        self.col_width = self._get_widths()
        self._table_str = self.make_table_str() if self.colorize else self.make_table_str_without_color()

    @staticmethod
    def _get_string_width(val: str):
        w = 0
        for v in val:
            if u'\u4e00' <= v <= u'\u9fff' or v in '【】（）—…￥！·、？。，《》：；‘“':
                w += 2
            else:
                w += 1
        return w

    def _get_widths(self):
        """获取列宽度，列宽度为整列数据中的最大数据宽度"""

        col_width = [self._get_string_width(key) for key in self.header]
        for row in self.data:
            for i, key in enumerate(self.header):
                value = row.get(key, '')
                width = min(self._get_string_width(value), self.max_width)
                col_width[i] = max(col_width[i], width)
        return col_width

    def make_table_str(self):
        def format_str(val, width):
            length = self._get_string_width(val)
            left = (width - length) // 2
            right = (width - length) - left
            return f'{" " * left}{val}{" " * right}'

        header = ' | '.join(str(self.title_color(format_str(key, w))) for w, key in zip(self.col_width, self.header))
        if self.caption:
            caption = self.caption_color(format_str(self.caption, sum(self.col_width) + (len(self.col_width) - 1) * 3))
            header = caption + '\n' + header
        rows = [' | '.join(format_str(row.get(key, ""), w) for w, key in zip(self.col_width, self.header)) for row in
                self.data]
        return '\n'.join([header, '=' * (sum(self.col_width) + (len(self.col_width) - 1) * 3)] + rows)

    def make_table_str_without_color(self):
        def format_str(val, width):
            length = self._get_string_width(val)
            left = (width - length) // 2
            right = (width - length) - left
            return f'{" " * left}{val}{" " * right}'

        def get_value(row, key):
            val = row.get(key, "")
            if isinstance(val, _Color):
                return val.raw
            return val

        header = ' | '.join(str(format_str(key, w)) for w, key in zip(self.col_width, self.header))
        if self.caption:
            caption = format_str(self.caption, sum(self.col_width) + (len(self.col_width) - 1) * 3)
            header = caption + '\n' + header
        rows = [' | '.join(format_str(get_value(row, key), w) for w, key in zip(self.col_width, self.header)) for row in
                self.data]
        return '\n'.join([header, '=' * (sum(self.col_width) + (len(self.col_width) - 1) * 3)] + rows)

    def __str__(self):
        return self._table_str

    __repr__ = __str__


if __name__ == '__main__':
    table = ConsoleTable(
        [{'server_name': 'intelligent-platform-product', 'status': Color.green('成功'), 'message': '构建成功'}],
        caption='构建结果',
    )
    print(table)
