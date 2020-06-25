#!/usr/bin/env python
# -*- coding : utf-8 -*-

import pytest

from dcmwrangle.util import *


class Point:
    """Simple class for testing.

    Attributes:
        x : the x-coordinate
        y : the y-coordinate
    """
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


def test_group_key_att():
    """Tests grouping keys by attributes of the objects."""
    # Construct some points and put them into dicts
    testdict = {}
    testdict['cat'] = Point(1, 1)
    testdict['dog'] = Point(1, 2)
    testdict['zebra'] = Point(3, 3)

    # ------------------
    # Check for failures
    # ------------------
    # Should cause error when indict is not a dict
    with pytest.raises(TypeError, match=r'indict*'):
        x_groups, x_vals = group_key_att(1, 'x')

    # Should cause error when attribute is not a string
    with pytest.raises(TypeError, match=r'attribute*'):
        x_groups, x_vals = group_key_att(testdict, 1)

    # Should cause error when subset isn't a list
    with pytest.raises(TypeError, match=r'subset*'):
        x_groups, x_vals = group_key_att(testdict, 'x', subset=1)

    # Should cause error when sort isn't a boolean
    with pytest.raises(TypeError, match=r'sort*'):
        x_groups, x_vals = group_key_att(testdict, 'x', sort='pi')

    # Check for failure when using non-existent attribute to group
    with pytest.raises(AttributeError):
        z_vals, z_groups = group_key_att(testdict, 'z')

    # Check for failure when using non-existent subset
    with pytest.raises(KeyError):
        x_groups, x_vals = group_key_att(testdict, 'x', subset=['seal'])
    # -----------------
    # Whole-dict search
    # -----------------
    x_groups, x_vals = group_key_att(testdict, 'x')
    # Use empty list subset to check corner case where subset is empty
    y_groups, y_vals = group_key_att(testdict, 'y', subset=[])
    # X Grouping
    # ----------
    # Should have two unique x-values
    assert len(x_groups) == 2

    # Should have values 1 and 3, sorted
    assert x_vals == [1, 3]

    # Group 0 should have 'cat' and 'dog
    assert sorted(x_groups[0]) == ['cat', 'dog']

    # Group 1 should have 'zebra' only
    assert x_groups[1] == ['zebra']

    # Y Grouping
    # ----------
    # Should have three unique values
    assert len(y_groups) == 3

    # Y should have values 1-3, sorted
    assert y_vals == [1, 2, 3]

    # Test groups in order; 'cat', 'dog', 'zebra'
    assert y_groups[0] == ['cat']
    assert y_groups[1] == ['dog']
    assert y_groups[2] == ['zebra']
    # ------------------------
    # Check for subset of keys
    # ------------------------
    x_groups, x_vals = group_key_att(testdict, 'x', subset=['cat', 'dog'])
    y_groups, y_vals = group_key_att(testdict, 'y', subset=['cat', 'dog'])

    # X Grouping
    # ----------
    # Should have one unique x-value
    assert len(x_groups) == 1

    # Only x-value should be 1
    assert x_vals[0] == 1

    # Group 0 should have 'cat' and 'dog'
    assert sorted(x_groups[0]) == ['cat', 'dog']

    # Y Grouping
    # ----------
    # Should have two unique y-values
    assert len(y_groups) == 2

    # The two unique y-values should be 1 and 2
    assert y_vals == [1, 2]

    # Group 0 should have 'cat'
    assert y_groups[0] == ['cat']

    # Group 1 should have 'dog'
    assert y_groups[1] == ['dog']


def test_group_key_value():
    """Test group_key_value with simple point class."""
    # Construct some points and put them into dicts
    testdict = {}
    testdict['cat'] = Point(1, 1)
    testdict['dog'] = Point(1, 2)
    testdict['zebra'] = Point(3, 3)

    # ------------------
    # Check for failures
    # ------------------
    # Should cause error when indict is not a dict
    with pytest.raises(TypeError, match=r'indict*'):
        x_groups, x_vals = group_key_val(1, 'x', None)

    # Should cause error when attribute is not a string
    with pytest.raises(TypeError, match=r'attribute*'):
        x_groups, x_vals = group_key_val(testdict, 1, None)

    # Should cause error when subset isn't a list
    with pytest.raises(TypeError, match=r'subset*'):
        x_groups, x_vals = group_key_val(testdict, 'x', None, subset=1)

    # Should cause error when sort isn't a boolean
    with pytest.raises(TypeError, match=r'sort*'):
        x_groups, x_vals = group_key_val(testdict, 'x', None, sort='pi')

    # Check for failure when using non-existent attribute to group
    with pytest.raises(AttributeError):
        z_vals, z_groups = group_key_val(testdict, 'z', None)

    # Check for failure when using non-existent subset
    with pytest.raises(KeyError):
        x_groups, x_vals = group_key_val(testdict, 'x',
                                         None, subset=['seal'])
    # -----------------------------------
    # Check for Matches to various values
    # -----------------------------------
    # Check that correct ones are hit
    matches_x_1 = group_key_val(testdict, 'x', 1)
    assert sorted(matches_x_1) == ['cat', 'dog']

    matches_x_3 = group_key_val(testdict, 'x', 3)
    assert matches_x_3 == ['zebra']

    matches_y_1 = group_key_val(testdict, 'y', 1)
    assert matches_y_1 == ['cat']

    matches_y_2 = group_key_val(testdict, 'y', 2)
    assert matches_y_2 == ['dog']

    matches_y_3 = group_key_val(testdict, 'y', 3)
    assert matches_y_3 == ['zebra']

    # Check that there is no result for a value that doesn't exist
    matches_x_naught = group_key_val(testdict, 'x', 0)
    assert matches_x_naught == []

    matches_x_null = group_key_val(testdict, 'x', None)
    assert matches_x_null == []

    matches_y_naught = group_key_val(testdict, 'y', 0)
    assert matches_y_naught == []

    matches_y_naught = group_key_val(testdict, 'y', None)
    assert matches_y_naught == []

    # Check that subset works
    testdict['philosophy'] = Point(1, -1)  # Add an overload to x = 1
    testdict['afterthought'] = Point(-1, 1)  # Add an overload to y = 1

    matches_x_subset = group_key_val(testdict, 'x', 1,
                                     subset=['cat', 'dog'])
    assert matches_x_subset == ['cat', 'dog']

    # Check that subset works for skipping a match
    matches_x_subset = group_key_val(testdict, 'x', 1,
                                     subset=['zebra'])
    assert matches_x_subset == []

    matches_y_subset = group_key_val(testdict, 'y', 1,
                                     subset=['cat', 'dog'])
    assert matches_y_subset == ['cat']

    # Check that subset works for skipping a match
    matches_y_subset = group_key_val(testdict, 'y', 3,
                                     subset=['cat', 'dog'])
    assert matches_x_subset == []


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


def test_gs_quit():
    """Tests to make sure that get_statement can find a quit symbol."""

    operator, group, arg = get_statement('q')
    assert operator == Operators.QUIT
    assert group is None
    assert arg is None

    operator, group, arg = get_statement('quit')
    assert operator == Operators.QUIT
    assert group is None
    assert arg is None
