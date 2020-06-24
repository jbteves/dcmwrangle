#/usr/bin/env python
# -*- coding : utf-8 -*-

import os
import os.path as op

import pydicom
from dicomorg import dcmtable

def get_test_data():
    data_path = op.join(op.abspath('.'), 'data')
    table = dcmtable.dcmtable(data_path)
    return table

def test_get_test_data():
    table = get_test_data()
    assert isinstance(table, dcmtable.dcmtable)

def test_dcmtable_group_info():
    table = get_test_data()
    assert table.groups == {'ungrouped' : [0, 1, 2, 3, 4, 5]}


def test_dcmtable_series_names():
    table = get_test_data()
    assert len(table.names) == 6
    assert table.names == ['AAHEAD_SCOUT_TMS', 
                                 'AAHEAD_SCOUT_TMS_MPR_sag',
                                 'AAHEAD_SCOUT_TMS_MPR_cor',
                                 'AAHEAD_SCOUT_TMS_MPR_tra',
                                 'MBME_RPE1_TMS_SBRef', 'MBME_RPE1_TMS']


def test_dcmtable_series_numbers():
    table = get_test_data()
    assert table.numbers == [1, 2, 3, 4, 5, 6]

def test_dcmtable_series_filecounts():
    table = get_test_data()
    assert len(table.files[0]) == 128
    assert len(table.files[1]) == 5
    assert len(table.files[2]) == 3
    assert len(table.files[3]) == 3
    assert len(table.files[4]) == 3
    assert len(table.files[5]) == 9


def test_dcmtable_series_echoes():
    table = get_test_data()
    assert table.echoes[0] == [1.37]
    assert table.echoes[1] == [1.37]
    assert table.echoes[2] == [1.37]
    assert table.echoes[3] == [1.37]
    assert table.echoes[4] == [11.2, 32.36, 53.52]
    assert table.echoes[5] == [11.2, 32.36, 53.52]
