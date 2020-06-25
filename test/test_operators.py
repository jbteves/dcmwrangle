#!/usr/bin/env python
# -*- coding : utf-8 -*-

import pytest

from dcmwrangle.parsing import *
from dcmwrangle.operators import *


def test_halt():
    with pytest.raises(ValueError):
        halt('', None)
    with pytest.raises(ValueError):
        halt(None, '')
    with pytest.raises(SystemExit):
        halt(None, None)


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
