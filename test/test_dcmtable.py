#!/usr/bin/env python
# -*- coding : utf-8 -*-

import pytest
import pathlib
import os.path as op

from dcmwrangle import dcmtable
from dcmwrangle import colors

herepath = pathlib.Path(__file__).parent.absolute()


def get_test_data():
    data_path = op.join(herepath, 'data')
    table = dcmtable.dcmtable(data_path)
    return table


def test_get_test_data():
    table = get_test_data()
    assert isinstance(table, dcmtable.dcmtable)


def test_build_from_bad_dir():
    with pytest.raises(ValueError, match=r'Directory*'):
        dcmtable.dcmtable('/here/is/kalamazoo')


def test_build_from_nonstr():
    with pytest.raises(TypeError):
        dcmtable.dcmtable(1)


def test_dcmtable_group_info():
    table = get_test_data()
    assert table.groups == {'ungrouped': [0, 1, 2, 3, 4, 5]}


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


def test_dcmtable_str():
    table = get_test_data()
    path = op.join(herepath, 'data')
    pathstr = [colors.green('Dicom files at {0}'.format(path))]
    group = [colors.magenta('ungrouped:')]
    style = '{:3d}\t{:35s}\t{:15}\t{:5d}\t{:2s}'
    stringparts = ['' for i in range(len(table.files))]
    for i in range(len(table.files)):
        hdr = table.table[table.files[i][0]]
        name = getattr(hdr, 'SeriesDescription')
        time = getattr(hdr, 'SeriesTime')
        if len(table.echoes[i]) == 1:
            echo = 'SE'
            color = colors.blue
        else:
            echo = 'ME'
            color = colors.cyan
        nfiles = len(table.files[i])
        stringparts[i] = color(style.format(i + 1, name, time, nfiles,
                               echo))
    # Join all ports
    allparts = pathstr + group + stringparts
    finalstr = '\n'.join(allparts)

    assert table.__str__() == finalstr
