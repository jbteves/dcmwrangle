#!/usr/bin/env python
# -*- coding : utf-8 -*-

import pytest

from dcmwrangle.parsing import *


def test_get_argument():
    """Tests to make sure you get an argument from a wordlist"""

    assert get_argument(['cat']) == 'cat'
    with pytest.raises(TypeError):
        get_argument('cat')
    with pytest.raises(ValueError):
        get_argument(['cat', 'dog'])


def test_get_srange():
    """Tests to make sure you get proper sranges from a word"""

    assert get_srange('6') == [6]
    assert get_srange('1:3') == [1, 2, 3]
    assert get_srange('3:1') == [1, 2, 3]
    assert get_srange('3:2:9') == [3, 5, 7, 9]
    assert get_srange('3:2:8') == [3, 5, 7]
    assert get_srange('9:-1:9') == [9]
    assert get_srange('9:-1:12') == []
    assert get_srange('9:-2:3') == [3, 5, 7, 9]

    with pytest.raises(TypeError):
        get_srange(None)
    with pytest.raises(TypeError):
        get_srange([])
    with pytest.raises(ValueError):
        get_srange('3.2:4')
    with pytest.raises(ValueError):
        get_srange('3:.2:4')
    with pytest.raises(ValueError):
        get_srange('3:1:4.2')
    with pytest.raises(ValueError):
        get_srange('3:')
    with pytest.raises(ValueError):
        get_srange(':')
    with pytest.raises(ValueError):
        get_srange(':3')
    with pytest.raises(ValueError):
        get_srange('-1:2')


def test_get_group():
    """Tests to make sure get_group gets correct numerical groups."""
    g, w = get_group(['1:3', 'aardvark'])
    assert g == [1, 2, 3]
    assert w == ['aardvark']
    g, w = get_group(['[1', '2', '3]', 'aardvark'])
    assert g == [1, 2, 3]
    assert w == ['aardvark']
    g, w = get_group(['1:3'])
    assert g == [1, 2, 3]
    g, w = get_group(['[3:1', '5', '7]'])
    assert g == [1, 2, 3, 5, 7]
    g, w = get_group([])
    assert g is None
    with pytest.raises(ValueError):
        get_group(['['])
    with pytest.raises(ValueError):
        get_group('')
    with pytest.raises(ValueError):
        get_group(None)
    with pytest.raises(ValueError):
        get_group(['[1', '2'])


def test_get_statement():
    """Tests to make sure we correctly parse statements."""
    operator, group, arg = get_statement('q')
    assert operator == 'q'
    assert group is None
    assert arg is None

    operator, group, arg = get_statement('q [1 2 3] boo')
    assert operator == 'q'
    assert group == [1, 2, 3]
    assert arg == 'boo'

    operator, group, arg = get_statement('q boo')
    assert operator == 'q'
    assert group is None
    assert arg == 'boo'
