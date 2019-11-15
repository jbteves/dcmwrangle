"""
Stores ASCII escape codes for color for simplicity.
Yes, there are other packages for this, but I'm trying to minimize
dependencies and these are trivial
"""


# TODO: make non-reset functionality
def black(tocolor, reset=True):
    return '\u001b[30m' + tocolor + '\u001b[0m'


def red(tocolor, reset=True):
    return '\u001b[31m' + tocolor + '\u001b[0m'


def green(tocolor, reset=True):
    return '\u001b[32m' + tocolor + '\u001b[0m'


def yellow(tocolor, reset=True):
    return '\u001b[33m' + tocolor + '\u001b[0m'


def blue(tocolor, reset=True):
    return '\u001b[34m' + tocolor + '\u001b[0m'

def magenta(tocolor, reset=True):
    return '\u001b[35m' + tocolor + '\u001b[0m'

def cyan(tocolor, reset=True):
    return '\u001b[36m' + tocolor + '\u001b[0m'

def white(tocolor, reset=True):
    return '\u001b[37m' + tocolor + '\u001b[0m'
