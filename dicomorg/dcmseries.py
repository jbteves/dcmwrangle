#!/usr/bin/env python
# -*- coding : utf-8 -*-

"""
Simple class to facilitate series information organization
"""

import pydicom
import os.path as op
import copy

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
        self.alias = None

        # Check all files for existence
        for f in files:
            if not op.exists(f):
                raise Exception('Cannot find or access file ' + f)

        self.files = files
        self.start = start
    def __str__(self):
        """String representation of the dcmseries
        """
        if self.alias:
            return '{:3d}\t{:30s}\t{:20s}\t{:5d}'.format(self.seriesnumber,
                                                  self.alias,
                                                  self.start,
                                                  len(self.files))
        else:
            return '{:3d}\t{:30s}\t{:20s}\t{:5d}'.format(self.seriesnumber,
                                                  self.seriesname,
                                                  self.start,
                                                  len(self.files))
    def ignore(self):
        """Makes this dicom series ignored in printing"""
        self.alias = ''
    def set_alias(self, alias):
        self.alias = alias
    def get_seriesnumber(self):
        """Returns the series number

        Returns
        -------
        The series number
        """
        return self.seriesnumber
    def get_seriesname(self):
        """Returns the series description/name as it is in the header

        Returns
        -------
        The series name
        """
        return copy.copy(self.seriesname)
    def get_files(self):
        """Returns the filenames in the series

        Returns
        -------
        A copy of the series files
        """
        return copy.copy(self.files)
    def get_start(self):
        """Returns the start time of the series as defined in the header
        -------
        A string of the start time
        """
        return copy.copy(self.start)
    def get_alias(self):
        return copy.copy(self.alias)
    def is_ignorable(self):
        """Returns whether the series is ignorable

        Returns
        -------
        Whether the series is ignorable
        """
        return self.alias == ''
