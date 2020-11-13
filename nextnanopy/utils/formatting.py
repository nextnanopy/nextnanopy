from nextnanopy.nnp.format import fmt as nnpfmt
from nextnanopy.nn3.format import fmt as nn3fmt
from nextnanopy.negf.format import fmt as negffmt

fmts = {
    'nextnano++': nnpfmt,
    'nextnano3': nn3fmt,
    'nextnano.NEGF': negffmt,
}


def input_file_type(fullpath):
    if is_nn3_input_file(fullpath):
        return 'nextnano3'
    elif is_nnp_input_file(fullpath):
        return 'nextnano++'
    elif is_negf_input_file(fullpath):
        return 'nextnano.NEGF'
    elif is_msb_input_file(fullpath):
        return 'nextnano.MSB'
    else:
        return 'not valid'


def pattern_in_file(fullpath, input_pattern):
    with open(fullpath, 'r') as f:
        for line in f:
            if input_pattern in line:
                return True
    return False


def is_nn3_input_file(fullpath):
    fmt = fmts['nextnano3']
    return pattern_in_file(fullpath, fmt['input_pattern'])


def is_nnp_input_file(fullpath):
    fmt = fmts['nextnano++']
    return pattern_in_file(fullpath, fmt['input_pattern'])


def is_negf_input_file(fullpath):
    fmt = fmts['nextnano.NEGF']
    return pattern_in_file(fullpath, fmt['input_pattern'])


def is_msb_input_file(fullpath):
    fmt = fmts['nextnano.MSB']
    return pattern_in_file(fullpath, fmt['input_pattern'])


def is_variable(text, var_char):
    boolean = False
    text = str(text).strip()
    if not text:
        boolean = False
    elif text[0] == var_char and '=' in text:
        boolean = True
    return boolean


def is_nn3_variable(text):
    fmt = fmts['nextnano3']
    return is_variable(text, var_char=fmt['var_char'])


def is_nnp_variable(text):
    fmt = fmts['nextnano++']
    return is_variable(text, var_char=fmt['var_char'])


def autofmt_variable_value(value):
    cases = [int, float, str]
    for case in cases:
        try:
            value = case(value)
            break
        except:
            pass
    return value


def parse_variable(text, var_char, com_char):
    text = str(text).strip()
    if text[0] == var_char:
        text = str(text[1:])
    name, right = text.split('=', maxsplit=1)
    if com_char in right:
        value, comment = right.split(com_char, maxsplit=1)
    else:
        value = right
        comment = ''
    name, value, comment = [_str.strip() for _str in [name, value, comment]]
    value = autofmt_variable_value(value)
    return name, value, comment


def parse_nn3_variable(text):
    fmt = fmts['nextnano3']
    return parse_variable(text, var_char=fmt['var_char'], com_char=fmt['com_char'])


def parse_nnp_variable(text):
    fmt = fmts['nextnano++']
    return parse_variable(text, var_char=fmt['var_char'], com_char=fmt['com_char'])


def text(init='', mid='', end='', fmt=lambda i, m, f: i + m + f):
    return fmt(str(init), str(mid), str(end))


def text_to_lines(text):
    for line in str(text).split('\n'):
        yield line


def lines_to_text(*lines):
    ls = '\n'.join([str(t) for t in lines])
    return ls


def modify_lines_in_text(init='', mid='', end=''):
    ls = text_to_lines(mid)
    new = [text(init, line, end) for line in ls]
    return lines_to_text(*new)


def paragraph(content):
    return text('\n', content, '\n')


def preview(text, nums=True):
    lines = text_to_lines(text)
    for i, line in enumerate(lines):
        if nums:
            print(f'{i} {line}')
        else:
            print(f'{line}')
