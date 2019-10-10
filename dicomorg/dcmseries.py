#!/usr/bin/env python
# -*- coding : utf-8 -*-

"""
Simple class to facilitate series information organization
"""

import pydicom
import os.path as op

class dcmseries:
    def __init__(self, seriesnumber, seriesname, files, start):
        """Constructor for dcmseries

        Parameters
        ----------
        self
            The object itself
        seriesnumber :obj: `int`
            The series number of the dicom series
        seriesname :obj: `str`
            The series description of the dicom series
        files (N x 1) `array`
            An array of filenames
        start :obj: `str`
            A string indicating the series start time
        """
        # Set the basics
        self.seriesnumber = seriesnumber
        self.seriesname = seriesname

        # Check all files for existence
        for f in files:
            if not op.exists(f):
                raise Exception('Cannot find or access file ' + f)

        self.files = files
        self.start = start
    def __str__(self):
        """String representation of the dcmseries
        """
        return '{:3d}\t{:30s}\t{:20s}\t{:5d}'.format(self.seriesnumber,
                                              self.seriesname,
                                              self.start,
                                              len(self.files))
