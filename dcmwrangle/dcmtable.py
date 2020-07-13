#!/usr/bin/env python3
# -*- coding : utf-8 -*-

import os
import os.path as op
from copy import deepcopy

from pydicom import dcmread, errors

from dcmwrangle.util import group_key_att
from dcmwrangle import colors


class dcmtable:
    """The grand dicom table

    Attributes
    ----------
    path : str
        The path to the dicoms that the table describes
    table : dict
        A dictionary containing file-header pairs as key-value pairs
    groups : dict
        A dictionary where each group name is a key to the list of series
        numbers associated with that group.
    numbers : list
        A list indicating which series numbers are present, indices match
        the seriesname and seriesfile attributes.
    names : list
        A list indicating the name of each series number.
    files : list
        A list indicating the files associated with each series number.
    echoes: list
        A list indicating the echo times for each series.
    """

    def __init__(self, basis):
        """Constructor for dcmtable

        Parameters
        ----------
        basis : str
            A string indicating where the dicom files are that this table
            should build from.

        Raises
        ------
        TypeError
            If the basis is not a string
        ValueError
            If the basis does not exist
        """
        if isinstance(basis, str):
            # Create table from file path
            self.path = op.abspath(basis)
            if not op.isdir(self.path):
                raise ValueError('Directory supplied '
                                 '({0}) does not exist!'.format(self.path))
            toread = os.listdir(self.path)
            toread = [op.join(basis, f) for f in toread]
            self.table = {}

            for f in toread:
                try:
                    if op.isdir(f):
                        continue
                    else:
                        self.table[f] = dcmread(f, stop_before_pixels=True)
                except errors.InvalidDicomError:
                    continue

            # Find all series
            files, numbers = group_key_att(self.table, 'SeriesNumber')
            self.files = files
            self.numbers = [int(i) for i in numbers]

            # Get all series names, make sure no name overloading
            self.names = ['' for i in self.files]
            for i in range(len(self.files)):
                sfiles, snames = group_key_att(self.table,
                                               'SeriesDescription',
                                               subset=self.files[i])
                if len(snames) != 1:
                    raise ValueError('Dicoms contain multiple names for '
                                     'same series number!')
                self.names[i] = snames[0]

            # Get the echo times for the series
            self.echoes = [[] for i in self.numbers]
            for i in range(len(self.files)):
                _, echoes = group_key_att(self.table, 'EchoTime',
                                          subset=self.files[i])
                echoes = [float(e) for e in echoes]
                self.echoes[i] = echoes

            # Create the common group
            self.groups = {'ungrouped': [i for i in range(len(self.numbers))]}
        elif isinstance(basis, dcmtable):
            self.path = basis.path
            self.table = basis.table
            self.files = basis.files
            self.numbers = deepcopy(basis.numbers)
            self.names = deepcopy(basis.names)
            self.echoes = deepcopy(basis.echoes)
            self.groups = deepcopy(basis.groups)
        else:
            thistype = type(basis)
            raise TypeError('basis must be str or dcmtable, '
                            '{0} supplied'.format(thistype))

    def number2idx(self, number):
        """Converts a number to an index of series.

        Parameters
        ----------
        number
            The series number to index.

        Raises
        ------
        ValueError
            If the series number is not present in the table.
        """
        if not number in self.numbers:
            raise ValueError('Series {0} not in table.'.format(number))
        return self.numbers.index(number)

    def __str__(self):
        allparts = [colors.green('Dicom files at {0}'.format(self.path))]
        style = '{:3d}\t{:35s}\t{:15}\t{:5d}\t{:2s}'
        for g in self.groups:
            if g == 'ignored':
                continue
            allparts += [colors.magenta('{0}:'.format(g))]
            stringparts = ['' for i in range(len(self.groups[g]))]
            for i in range(len(self.groups[g])):
                idx = self.groups[g][i]
                hdr = self.table[self.files[idx][0]]
                name = getattr(hdr, 'SeriesDescription')
                time = getattr(hdr, 'SeriesTime')
                if len(self.echoes[idx]) == 1:
                    echo = 'SE'
                    color = colors.blue
                else:
                    echo = 'ME'
                    color = colors.cyan
                nfiles = len(self.files[idx])
                stringparts[i] = color(style.format(self.numbers[idx],
                                       name, time, nfiles, echo))
            allparts += stringparts
        finalstr = '\n'.join(allparts)

        return finalstr
