from consts import *

def check_char(char: str):
    valid_escapes = {'\\t', '\\n', '\\0', "\\'", '\\"', '\\\\'}
    if len(char) == 2 and char[0] == '\\':
        if char in valid_escapes:
            return True
        else:
            return False
    elif len(char) == 1 and char not in {'\\', '"'}:
        return True
    else:
        return False


def check_string(string: str):
    # The string must begin and end with a double quote
    if len(string) < 2:
        return False
    if string[0] != '"' or string[-1] != '"':
        return False

    i = 1  # Start after the opening quote
    while i < len(string) - 1:  # Stop before the closing quote
        if string[i] == '\\':
            # Check if there's at least one more character for the escape sequence
            if i + 1 >= len(string) - 1:
                return False
            # Validate the escape sequence
            if not check_char(string[i:i+2]):
                return False
            i += 2  # Move past the escape sequence
        else:
            # Validate a regular character
            if not check_char(string[i]):
                return False
            i += 1  # Move to the next character
    return True



def implicit_cast(start, target):
    if start == target:
        return True
    if start == CONST_INT and target == INT:
        return True
    if start == INT and target == CONST_INT:
        return True
    if start == CONST_CHAR and target == CHAR:
        return True
    if start == CHAR and target == CONST_CHAR:
        return True
    if start == CONST_CHAR and target == INT:
        return True
    if start == CHAR and target == INT:
        return True
    if start == CHAR and target == CONST_INT:
        return True
    if start == CONST_CHAR and target == CONST_INT:
        return True

    if start == NIZ_CHAR and target == NIZ_CONST_CHAR:
        return True
    if start == NIZ_INT and target == NIZ_CONST_INT:
        return True
    if start == NIZ_CHAR and target == NIZ_CONST_INT:
        return True
    return False


def explicit_cast(start, target):
    if implicit_cast(start, target):
        return True
    if start == INT and target == CHAR:
        return True
    if start == INT and target == CONST_CHAR:
        return True
    if start == CONST_INT and target == CHAR:
        return True
    if start == CONST_INT and target == CONST_CHAR:
        return True
    return False


def remove_niz_from_niz_x(niz_x):
    if niz_x == NIZ_CHAR:
        return CHAR
    if niz_x == NIZ_INT:
        return INT
    if niz_x == NIZ_CONST_CHAR:
        return CONST_CHAR
    if niz_x == NIZ_CONST_INT:
        return CONST_INT


def remove_const_from_const_x(const_x):
    if const_x == CONST_CHAR:
        return CHAR
    if const_x == CONST_INT:
        return INT


def is_const_x(T: str):
    if not T:
        return False
    return T.startswith("const")


def is_niz_x(niz: str):
    return (niz == NIZ_INT or niz == NIZ_CHAR or
            niz == NIZ_CONST_INT or niz == NIZ_CONST_CHAR)


def make_const(x: str):
    if x.startswith("const"):
        return x
    return "const(" + x + ")"

def make_niz(x: str):
    return "niz(" + x + ")"


def make_frisc_hex(x: int):
    hex_str = hex(x)[2:].upper()
    if hex_str[0].isalpha():
        return "0" + hex_str
    return hex_str



class UniqueCounter:
    x = 0

    @classmethod
    def get_unique(cls):
        cls.x += 1
        return cls.x