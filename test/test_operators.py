#!/usr/bin/env python
# -*- coding : utf-8 -*-

import pytest
from test_dcmtable import get_test_data

from dcmwrangle.parsing import *
from dcmwrangle.operators import *


def test_halt():
    with pytest.raises(ValueError):
        halt('', None, None)
    with pytest.raises(ValueError):
        halt(None, '', None)
    with pytest.raises(SystemExit):
        halt(None, None, None)


def test_parsed_quit():
    operator, group, arg = get_statement('q')
    fn = word2fn(operator)
    with pytest.raises(SystemExit):
        fn(group, arg, None)

    operator, group, arg = get_statement('quit')
    fn = word2fn(operator)
    with pytest.raises(SystemExit):
        fn(group, arg, None)


def test_group():
    table = get_test_data()
    with pytest.raises(TypeError):
        group(None, 'anat', table)
    with pytest.raises(TypeError):
        group([1], None, table)
    with pytest.raises(TypeError):
        group([1], 'anat', None)

    newtable = dcmtable(table)
    group([1, 2, 3, 4], 'scout', newtable)
    assert newtable.groups == {'ungrouped': [4, 5], 'scout': [0, 1, 2, 3]}
    assert table.groups == {'ungrouped': [0, 1, 2, 3, 4, 5]}
    group([5, 6], 'tms', newtable)
    assert newtable.groups == {'tms': [4, 5], 'scout': [0, 1, 2, 3]}
    assert 'ungrouped' in table.groups
    group([5], 'sbref', newtable)
    assert newtable.groups == {'tms': [5], 'scout': [0, 1, 2, 3],
                               'sbref': [4]}
    assert 'sbref' not in table.groups

    # check we reorder when we run group on something that's grouped
    newtable = dcmtable(table)
    group([1, 2], 'scout', newtable)
    group([1], 'scout', newtable)
    assert newtable.groups['scout'] == [1, 0]


def test_parsed_group():
    table = get_test_data()
    operator, group, arg = get_statement('group 1:4 scout')
    fn = word2fn(operator)
    fn(group, arg, table)
    assert table.groups == {'ungrouped': [4, 5], 'scout': [0, 1, 2, 3]}


def test_ungroup():
    table = get_test_data()
    with pytest.raises(TypeError):
        ungroup(None, None)
    with pytest.raises(TypeError):
        ungroup(1, None)

    newtable = dcmtable(table)
    group([1, 2, 3, 4], 'scout', newtable)
    ungroup([1, 2, 3, 4], None, newtable)
    assert newtable.groups == {'ungrouped': [4, 5, 0, 1, 2, 3]}

    ungroup([5, 6], None, newtable)
    assert newtable.groups == {'ungrouped': [0, 1, 2, 3, 4, 5]}


def test_parsed_ungroup():
    table = get_test_data()

    group([1, 2, 3, 4], 'scout', table)
    operator, g, arg = get_statement('ungroup 1:4')
    fn = word2fn(operator)
    fn(g, arg, table)
    assert table.groups == {'ungrouped': [4, 5, 0, 1, 2, 3]}

    group([5, 6], 'rpe', table)
    operator, g, arg = get_statement('ungroup 5:6')
    fn = word2fn(operator)
    fn(g, arg, table)
    assert table.groups == {'ungrouped': [0, 1, 2, 3, 4, 5]}


def test_word2op():
    assert word2op('q') == Operators.QUIT
    assert word2op('quit') == Operators.QUIT

    with pytest.raises(ValueError):
        word2op('mass_effect')


def test_op2fn():
    assert op2fn(Operators.QUIT) == halt
    with pytest.raises(TypeError):
        op2fn('cat')


def test_word2fn():
    assert word2fn('q') == halt
    assert word2fn('quit') == halt


def test_quit():
    operator, _, _ = get_statement('q')
    op = word2op(operator)
    assert op is Operators.QUIT

    operator, _, _ = get_statement('quit')
    op = word2op(operator)
    assert op is Operators.QUIT
