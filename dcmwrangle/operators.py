#!/usr/bin/env python
# -*- coding : utf-8 -*-

import sys
from enum import Enum


class Operators(Enum):
    QUIT = 0 


optable = {'q': Operators.QUIT,
           'quit': Operators.QUIT}

def halt(group, arg):
    """Halts execution of a program.

    Parameters
    ----------
    group
        Should not pass this
    arg
        Should not pass this

    Raises
    ------
    ValueError
        If you pass arguments anyway.
    """
    if group is not None:
        raise ValueError('Quit does not take a group')
    if arg is not None:
        raise ValueError('Quit does not take arguments')
    sys.exit()

fptable = {Operators.QUIT: halt}

def word2op(word):
    """Looks up the operator from a word.

    Parameters
    ----------
    word : str
        The word to look up.

    Raises
    ------
    ValueError
        If the word does not map to any operators.
    """

    if word in optable:
        return optable[word]
    else:
        raise ValueError('Operator {0} does not exist'.format(word))

def op2fn(op):
    """Looks up the function from an operator.

    Parameters
    ----------
    op : Operators
        The operator to look up.

    Raises
    ------
    TypeError
        If the op is not an Operators
    """
    if not isinstance(op, Operators):
        raise TypeError('{0} is not an operator', op)
    else:
        return fptable[op]

def word2fn(word):
    """Looks up the function from a word.

    Parameters
    ----------
    word : str
        The word to look up the function for

    Raises
    ------
    ValueError
        If the word does not map to any operators.
    """
    return op2fn(word2op(word))
