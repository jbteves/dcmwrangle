#!/usr/bin/env python
# -*- coding : utf-8 -*-

import sys
from enum import Enum

from dcmwrangle.dcmtable import dcmtable


class Operators(Enum):
    QUIT = 0,
    GROUP = 1


optable = {'q': Operators.QUIT,
           'quit': Operators.QUIT,
           'g': Operators.GROUP,
           'group': Operators.GROUP}

def halt(group, arg, table):
    """Halts execution of a program.

    Parameters
    ----------
    group
        Should not pass this.
    arg
        Should not pass this.
    table : dcmtable
        Should be a dcmtable, but gets ignored.

    Raises
    ------
    ValueError
        If you the first two pass arguments anyway.
    """
    if group is not None:
        raise ValueError('Quit does not take a group')
    if arg is not None:
        raise ValueError('Quit does not take arguments')
    sys.exit()

def group(g, arg, table):
    """Groups a dcmtable's series.

    Parameters
    ----------
    g : list
        The series group.
    arg : str
        The name of the group you'd like to make.
    table : dcmtable
        The dcmtable you'd like to modify

    Raises
    ------
    TypeError
        If the specified types are not matched.
    ValueError
        If the series group is outside of the range of the table.
    """
    if not isinstance(g, list):
        raise TypeError('Series group must be list, is of type '
                        '{0}'.format(str(type(g))))
    if not isinstance(arg, str):
        raise TypeError('Group name must be str, is of type '
                        '{0}'.format(str(type(arg))))
    if not isinstance(table, dcmtable):
        raise TypeError('Table must be dcmtable, is of type '
                        '{0}'.format(str(type(arg))))

    indices = []
    for s in g:
        indices.append(table.number2idx(s))
    for g in table.groups:
        group_indices = table.groups[g]
        for i in indices:
            if i in group_indices:
                group_indices.remove(i)
    emptygroups = []
    for g in table.groups:
        if not table.groups[g]:
            emptygroups.append(g)
    for g in emptygroups:
        del table.groups[g]
    if arg not in table.groups:
        table.groups[arg] = indices
    else:
        for idx in indices:
            table.groups[arg].append(idx)


fptable = {Operators.QUIT: halt,
           Operators.GROUP: group}

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
