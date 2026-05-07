"""
键盘布局定义 - 标准 US QWERTY 104键和87键布局
"""
from typing import List, Dict

# 单个按键的定义
# label: 显示的文字
# key_names: pynput 中的 key 标识符列表
# row: 行号 (0-5 主键盘, 6+ 小键盘)
# col: 起始列 (浮点数)
# width: 宽度倍数 (1.0 = 标准键宽)

MAIN_KEYS: List[Dict] = [
    # Row 0: 功能键行
    {'label': 'Esc',    'key_names': ['esc'],            'row': 0, 'col': 0,   'width': 1.0},
    {'label': 'F1',     'key_names': ['f1'],             'row': 0, 'col': 2,   'width': 1.0},
    {'label': 'F2',     'key_names': ['f2'],             'row': 0, 'col': 3,   'width': 1.0},
    {'label': 'F3',     'key_names': ['f3'],             'row': 0, 'col': 4,   'width': 1.0},
    {'label': 'F4',     'key_names': ['f4'],             'row': 0, 'col': 5,   'width': 1.0},
    {'label': 'F5',     'key_names': ['f5'],             'row': 0, 'col': 6.5, 'width': 1.0},
    {'label': 'F6',     'key_names': ['f6'],             'row': 0, 'col': 7.5, 'width': 1.0},
    {'label': 'F7',     'key_names': ['f7'],             'row': 0, 'col': 8.5, 'width': 1.0},
    {'label': 'F8',     'key_names': ['f8'],             'row': 0, 'col': 9.5, 'width': 1.0},
    {'label': 'F9',     'key_names': ['f9'],             'row': 0, 'col': 11,  'width': 1.0},
    {'label': 'F10',    'key_names': ['f10'],            'row': 0, 'col': 12,  'width': 1.0},
    {'label': 'F11',    'key_names': ['f11'],            'row': 0, 'col': 13,  'width': 1.0},
    {'label': 'F12',    'key_names': ['f12'],            'row': 0, 'col': 14,  'width': 1.0},
    {'label': 'PrtSc',  'key_names': ['print_screen'],   'row': 0, 'col': 15.5,'width': 1.0},
    {'label': 'ScrLk',  'key_names': ['scroll_lock'],    'row': 0, 'col': 16.5,'width': 1.0},
    {'label': 'Pause',  'key_names': ['pause'],          'row': 0, 'col': 17.5,'width': 1.0},

    # Row 1: 数字行
    {'label': '` ~',    'key_names': ['`'],              'row': 1, 'col': 0,   'width': 1.0},
    {'label': '1 !',    'key_names': ['1'],              'row': 1, 'col': 1,   'width': 1.0},
    {'label': '2 @',    'key_names': ['2'],              'row': 1, 'col': 2,   'width': 1.0},
    {'label': '3 #',    'key_names': ['3'],              'row': 1, 'col': 3,   'width': 1.0},
    {'label': '4 $',    'key_names': ['4'],              'row': 1, 'col': 4,   'width': 1.0},
    {'label': '5 %',    'key_names': ['5'],              'row': 1, 'col': 5,   'width': 1.0},
    {'label': '6 ^',    'key_names': ['6'],              'row': 1, 'col': 6,   'width': 1.0},
    {'label': '7 &',    'key_names': ['7'],              'row': 1, 'col': 7,   'width': 1.0},
    {'label': '8 *',    'key_names': ['8'],              'row': 1, 'col': 8,   'width': 1.0},
    {'label': '9 (',    'key_names': ['9'],              'row': 1, 'col': 9,   'width': 1.0},
    {'label': '0 )',    'key_names': ['0'],              'row': 1, 'col': 10,  'width': 1.0},
    {'label': '- _',    'key_names': ['-'],              'row': 1, 'col': 11,  'width': 1.0},
    {'label': '= +',    'key_names': ['='],              'row': 1, 'col': 12,  'width': 1.0},
    {'label': 'Back',   'key_names': ['backspace'],      'row': 1, 'col': 13,  'width': 2.0},

    # Row 2: QWERTY 上行
    {'label': 'Tab',    'key_names': ['tab'],            'row': 2, 'col': 0,   'width': 1.5},
    {'label': 'Q',      'key_names': ['q'],              'row': 2, 'col': 1.5, 'width': 1.0},
    {'label': 'W',      'key_names': ['w'],              'row': 2, 'col': 2.5, 'width': 1.0},
    {'label': 'E',      'key_names': ['e'],              'row': 2, 'col': 3.5, 'width': 1.0},
    {'label': 'R',      'key_names': ['r'],              'row': 2, 'col': 4.5, 'width': 1.0},
    {'label': 'T',      'key_names': ['t'],              'row': 2, 'col': 5.5, 'width': 1.0},
    {'label': 'Y',      'key_names': ['y'],              'row': 2, 'col': 6.5, 'width': 1.0},
    {'label': 'U',      'key_names': ['u'],              'row': 2, 'col': 7.5, 'width': 1.0},
    {'label': 'I',      'key_names': ['i'],              'row': 2, 'col': 8.5, 'width': 1.0},
    {'label': 'O',      'key_names': ['o'],              'row': 2, 'col': 9.5, 'width': 1.0},
    {'label': 'P',      'key_names': ['p'],              'row': 2, 'col': 10.5,'width': 1.0},
    {'label': '[ {',    'key_names': ['['],              'row': 2, 'col': 11.5,'width': 1.0},
    {'label': '] }',    'key_names': [']'],              'row': 2, 'col': 12.5,'width': 1.0},
    {'label': '\\ |',   'key_names': ['\\'],             'row': 2, 'col': 13.5,'width': 1.5},

    # Row 3: QWERTY 中行 (Home row)
    {'label': 'Caps',   'key_names': ['caps_lock'],      'row': 3, 'col': 0,   'width': 1.75},
    {'label': 'A',      'key_names': ['a'],              'row': 3, 'col': 1.75,'width': 1.0},
    {'label': 'S',      'key_names': ['s'],              'row': 3, 'col': 2.75,'width': 1.0},
    {'label': 'D',      'key_names': ['d'],              'row': 3, 'col': 3.75,'width': 1.0},
    {'label': 'F',      'key_names': ['f'],              'row': 3, 'col': 4.75,'width': 1.0},
    {'label': 'G',      'key_names': ['g'],              'row': 3, 'col': 5.75,'width': 1.0},
    {'label': 'H',      'key_names': ['h'],              'row': 3, 'col': 6.75,'width': 1.0},
    {'label': 'J',      'key_names': ['j'],              'row': 3, 'col': 7.75,'width': 1.0},
    {'label': 'K',      'key_names': ['k'],              'row': 3, 'col': 8.75,'width': 1.0},
    {'label': 'L',      'key_names': ['l'],              'row': 3, 'col': 9.75,'width': 1.0},
    {'label': '; :',    'key_names': [';'],              'row': 3, 'col': 10.75,'width':1.0},
    {'label': "' \"",   'key_names': ["'"],              'row': 3, 'col': 11.75,'width':1.0},
    {'label': 'Enter',  'key_names': ['enter'],          'row': 3, 'col': 12.75,'width':2.25},

    # Row 4: QWERTY 下行
    {'label': 'Shift',  'key_names': ['shift', 'shift_l'],'row': 4, 'col': 0,  'width': 2.25},
    {'label': 'Z',      'key_names': ['z'],              'row': 4, 'col': 2.25,'width': 1.0},
    {'label': 'X',      'key_names': ['x'],              'row': 4, 'col': 3.25,'width': 1.0},
    {'label': 'C',      'key_names': ['c'],              'row': 4, 'col': 4.25,'width': 1.0},
    {'label': 'V',      'key_names': ['v'],              'row': 4, 'col': 5.25,'width': 1.0},
    {'label': 'B',      'key_names': ['b'],              'row': 4, 'col': 6.25,'width': 1.0},
    {'label': 'N',      'key_names': ['n'],              'row': 4, 'col': 7.25,'width': 1.0},
    {'label': 'M',      'key_names': ['m'],              'row': 4, 'col': 8.25,'width': 1.0},
    {'label': ', <',    'key_names': [','],              'row': 4, 'col': 9.25,'width': 1.0},
    {'label': '. >',    'key_names': ['.'],              'row': 4, 'col': 10.25,'width':1.0},
    {'label': '/ ?',    'key_names': ['/'],              'row': 4, 'col': 11.25,'width':1.0},
    {'label': 'Shift',  'key_names': ['shift_r'],        'row': 4, 'col': 12.25,'width':2.75},

    # Row 5: 底部控制行
    {'label': 'Ctrl',   'key_names': ['ctrl', 'ctrl_l'], 'row': 5, 'col': 0,   'width': 1.25},
    {'label': 'Win',    'key_names': ['cmd', 'cmd_l'],   'row': 5, 'col': 1.25,'width': 1.25},
    {'label': 'Alt',    'key_names': ['alt', 'alt_l'],   'row': 5, 'col': 2.5, 'width': 1.25},
    {'label': '',       'key_names': ['space'],          'row': 5, 'col': 3.75,'width': 6.25},
    {'label': 'Alt',    'key_names': ['alt_r', 'alt_gr'],'row': 5, 'col': 10,  'width': 1.25},
    {'label': 'Win',    'key_names': ['cmd_r'],          'row': 5, 'col': 11.25,'width':1.25},
    {'label': 'Menu',   'key_names': ['menu'],           'row': 5, 'col': 12.5,'width': 1.25},
    {'label': 'Ctrl',   'key_names': ['ctrl_r'],         'row': 5, 'col': 13.75,'width':1.25},

    # 方向键
    {'label': '↑',      'key_names': ['up'],             'row': 6, 'col': 16.5,'width': 1.0, 'section': 'arrows'},
    {'label': '←',      'key_names': ['left'],           'row': 7, 'col': 15.5,'width': 1.0, 'section': 'arrows'},
    {'label': '↓',      'key_names': ['down'],           'row': 7, 'col': 16.5,'width': 1.0, 'section': 'arrows'},
    {'label': '→',      'key_names': ['right'],          'row': 7, 'col': 17.5,'width': 1.0, 'section': 'arrows'},
]

NUMPAD_KEYS: List[Dict] = [
    {'label': 'NumLk',  'key_names': ['num_lock'],       'row': 6, 'col': 19,  'width': 1.0, 'section': 'numpad'},
    {'label': '/',      'key_names': ['num_divide'],     'row': 6, 'col': 20,  'width': 1.0, 'section': 'numpad'},
    {'label': '*',      'key_names': ['num_multiply'],   'row': 6, 'col': 21,  'width': 1.0, 'section': 'numpad'},
    {'label': '-',      'key_names': ['num_subtract'],   'row': 6, 'col': 22,  'width': 1.0, 'section': 'numpad'},

    {'label': '7',      'key_names': ['num_7'],          'row': 7, 'col': 19,  'width': 1.0, 'section': 'numpad'},
    {'label': '8',      'key_names': ['num_8'],          'row': 7, 'col': 20,  'width': 1.0, 'section': 'numpad'},
    {'label': '9',      'key_names': ['num_9'],          'row': 7, 'col': 21,  'width': 1.0, 'section': 'numpad'},
    {'label': '+',      'key_names': ['num_add'],        'row': 7, 'col': 22,  'width': 1.0, 'height': 2.0, 'section': 'numpad'},

    {'label': '4',      'key_names': ['num_4'],          'row': 8, 'col': 19,  'width': 1.0, 'section': 'numpad'},
    {'label': '5',      'key_names': ['num_5'],          'row': 8, 'col': 20,  'width': 1.0, 'section': 'numpad'},
    {'label': '6',      'key_names': ['num_6'],          'row': 8, 'col': 21,  'width': 1.0, 'section': 'numpad'},

    {'label': '1',      'key_names': ['num_1'],          'row': 9, 'col': 19,  'width': 1.0, 'section': 'numpad'},
    {'label': '2',      'key_names': ['num_2'],          'row': 9, 'col': 20,  'width': 1.0, 'section': 'numpad'},
    {'label': '3',      'key_names': ['num_3'],          'row': 9, 'col': 21,  'width': 1.0, 'section': 'numpad'},
    {'label': 'Enter',  'key_names': ['num_enter'],      'row': 9, 'col': 22,  'width': 1.0, 'height': 2.0, 'section': 'numpad'},

    {'label': '0',      'key_names': ['num_0'],          'row': 10,'col': 19,  'width': 2.0, 'section': 'numpad'},
    {'label': '.',      'key_names': ['num_decimal'],    'row': 10,'col': 21,  'width': 1.0, 'section': 'numpad'},
]

# 中间功能区 (Insert, Home, PageUp, Delete, End, PageDown)
INS_DEL_KEYS: List[Dict] = [
    {'label': 'Ins',    'key_names': ['insert'],         'row': 6, 'col': 4.5, 'width': 1.0, 'section': 'ins_del'},
    {'label': 'Home',   'key_names': ['home'],           'row': 6, 'col': 5.5, 'width': 1.0, 'section': 'ins_del'},
    {'label': 'PgUp',   'key_names': ['page_up'],        'row': 6, 'col': 6.5, 'width': 1.0, 'section': 'ins_del'},
    {'label': 'Del',    'key_names': ['delete'],         'row': 7, 'col': 4.5, 'width': 1.0, 'section': 'ins_del'},
    {'label': 'End',    'key_names': ['end'],            'row': 7, 'col': 5.5, 'width': 1.0, 'section': 'ins_del'},
    {'label': 'PgDn',   'key_names': ['page_down'],      'row': 7, 'col': 6.5, 'width': 1.0, 'section': 'ins_del'},
]


def get_layout_104() -> List[Dict]:
    """获取全键 (104键) 布局"""
    return MAIN_KEYS + INS_DEL_KEYS + NUMPAD_KEYS


def get_layout_87() -> List[Dict]:
    """获取紧凑 (87键) 布局 - 无小键盘"""
    return MAIN_KEYS + INS_DEL_KEYS


def get_all_key_names(layout: List[Dict]) -> List[str]:
    """获取布局中所有 key_name 标识符列表"""
    names = []
    for key in layout:
        names.extend(key['key_names'])
    return names
