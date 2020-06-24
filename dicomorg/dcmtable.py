#/usr/bin/env python
# -*- coding : utf-8 -*-

import os
import os.path as op

import pydicom

from dicomorg import util
from dicomorg.util import *

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
        if isinstance(basis, str):
            # Create table from file path
            self.path = basis
            toread = os.listdir(self.path)
            toread = [op.join(basis, f) for f in toread]
            self.table = {}

            for f in toread:
                try:
                    self.table[f] = pydicom.dcmread(f, 
                                                    stop_before_pixels=True)
                except:
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
            self.groups = {'ungrouped' : [i for i in range(len(self.numbers))]}
