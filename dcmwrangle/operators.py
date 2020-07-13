#!/usr/bin/env python
# -*- coding : utf-8 -*-

import sys
from enum import Enum

from dcmwrangle.dcmtable import dcmtable


class Operators(Enum):
    QUIT = 0,
    GROUP = 1,
    UNGROUP = 2


optable = {'q': Operators.QUIT,
           'quit': Operators.QUIT,
           'g': Operators.GROUP,
           'group': Operators.GROUP,
           'ungroup': Operators.UNGROUP}

def halt(domain, arg, table):
    """Halts execution of a program.

    Parameters
    ----------
    domain
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
    if domain is not None:
        raise ValueError('Quit does not take a group')
    if arg is not None:
        raise ValueError('Quit does not take arguments')
    sys.exit()

def group(domain, arg, table):
    """Groups a dcmtable's series.

    Parameters
    ----------
    domain : list
        The series domain.
    arg : str
        The name of the group you'd like to make.
    table : dcmtable
        The dcmtable you'd like to modify

    Raises
    ------
    TypeError
        If the specified types are not matched.
    ValueError
        If the series domain is outside of the range of the table.
    """
    if not isinstance(domain, list):
        raise TypeError('Series group must be list, is of type '
                        '{0}'.format(str(type(domain))))
    if not isinstance(arg, str):
        raise TypeError('Group name must be str, is of type '
                        '{0}'.format(str(type(arg))))
    if not isinstance(table, dcmtable):
        raise TypeError('Table must be dcmtable, is of type '
                        '{0}'.format(str(type(arg))))

    indices = []
    for s in domain:
        indices.append(table.number2idx(s))
    for g in table.groups:
        domain_indices = table.groups[g]
        for i in indices:
            if i in domain_indices:
                domain_indices.remove(i)
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


def ungroup(domain, arg, table):
    """Ungroups a dcmtable's series.

    Parameters
    ----------
    domain : list
        The series domain.
    arg : None
        Should be None
    table : dcmtable
        The dcmtable you'd like to modify

    Raises
    ------
    TypeError
        If the specified types are not matched.
    ValueError
        If the series domain is outside of the range of the table.
    """
    if not isinstance(domain, list):
        raise TypeError('Series group must be list, is of type '
                        '{0}'.format(str(type(domain))))
    if arg:
        raise TypeError('Ungroup cannnot take argument')
    if not isinstance(table, dcmtable):
        raise TypeError('Table must be dcmtable, is of type '
                        '{0}'.format(str(type(arg))))

    group(domain, 'ungrouped', table)


fptable = {Operators.QUIT: halt,
           Operators.GROUP: group,
           Operators.UNGROUP: ungroup}

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
