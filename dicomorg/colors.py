"""
Stores ASCII escape codes for color for simplicity.
Yes, there are other packages for this, but I'm trying to minimize
dependencies and these are trivial
"""


def color_reset():
    return '\u001b[0m'


def build_color_string(code, string, reset=True):
    newstr = code + string
    if reset:
        return newstr + color_reset()
    else:
        return newstr

def black(tocolor, reset=True, bright=True):
    if bright:
        return build_color_string('\u001b[30;1m', tocolor, reset)
    else:
        return build_color_string('\u001b[30m', tocolor, reset)


def red(tocolor, reset=True, bright=True):
    if bright:
        return build_color_string('\u001b[31;1m', tocolor, reset)
    else:
        return build_color_string('\u001b[31m', tocolor, reset)


def green(tocolor, reset=True, bright=True):
    if bright:
        return build_color_string('\u001b[32;1m', tocolor, reset)
    else:
        return build_color_string('\u001b[32m', tocolor, reset)


def yellow(tocolor, reset=True, bright=True):
    if bright:
        return build_color_string('\u001b[33;1m', tocolor, reset)
    else:
        return build_color_string('\u001b[33m', tocolor, reset)

def blue(tocolor, reset=True, bright=True):
    if bright:
        return build_color_string('\u001b[34;1m', tocolor, reset)
    else:
        return build_color_string('\u001b[34m', tocolor, reset)

def magenta(tocolor, reset=True, bright=True):
    if bright:
        return build_color_string('\u001b[35;1m', tocolor, reset)
    else:
        return build_color_string('\u001b[35m', tocolor, reset)

def cyan(tocolor, reset=True, bright=True):
    if bright:
        return build_color_string('\u001b[36;1m', tocolor, reset)
    else:
        return build_color_string('\u001b[36m', tocolor, reset)

def white(tocolor, reset=True, bright=True):
    if bright:
        return build_color_string('\u001b[37;1m', tocolor, reset)
    else:
        return build_color_string('\u001b[37m', tocolor, reset)

