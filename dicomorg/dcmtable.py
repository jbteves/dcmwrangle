#/usr/bin/env python
# -*- coding : utf-8 -*-

"""
Class for making a table of dicom series
"""

import os
import os.path as op
from copy import copy
import pydicom
from dcmseries import dcmseries

class dcmtable:
    def __init__(self, path=None, prevtable=None):
        if (not path and not prevtable):
            raise Exception('You must provide a location to read dicoms '
                            'or a previous table to link to.')
        if path:
            # Construct table from a location
            if not op.exists(path):
                raise Exception('Path to read dicoms into table does not '
                                'exist.')
            # Set known members: path and prevtable
            self.path = path
            self.prevtable = None
            # Harvest dicom info
            dircontents = os.listdir(path)
            dcminfo = []
            fnames = []
            for f in dircontents:
                try:
                    dcminfo.append(pydicom.dcmread(op.join(path, f),
                                   stop_before_pixels=True))
                    fnames.append(op.join(path, f))
                except:
                    pass
            # Obtain series numbers and names
            seriesnumbers = []
            seriesnames = []
            for dcm in dcminfo:
                seriesnumbers.append(dcm.SeriesNumber)
                seriesnames.append(dcm.SeriesDescription)
            # Use series numbers to group files
            uniquenumbers = list(set(seriesnumbers))
            self.seriesnumbers = uniquenumbers
            seriesfiles = []
            uniquenames = []
            self.SeriesList = []
            for i in uniquenumbers:
                indices = [j for j, x in enumerate(seriesnumbers)
                           if x == i]
                thesefiles = []
                for j in indices:
                    thesefiles.append(fnames[j])
                seriesfiles.append(thesefiles)
                thisname = seriesnames[indices[0]]
                starttime = dcminfo[indices[0]].SeriesTime
                uniquenames.append(thisname)
                self.SeriesList.append(dcmseries(i, thisname, thesefiles,
                                       starttime))
        else:
            self = copy(prevtable)
            self.prevtable = prevtable
    def __str__(self):
        retstr = ''
        for s in self.SeriesList:
            if s.is_ignorable():
                continue
            retstr += str(s) + '\n'
        return retstr
    def ignore(self, toignore):
        idxtoignore = []
        for ignorable in toignore:
            ispresent = False
            for i in range(len(self.seriesnumbers)):
                number = str(self.seriesnumbers[i])
                if ignorable == number:
                    ispresent = True
                    idxtoignore.append(i)
                    break
            if not ispresent:
                raise Exception(ignorable + 'is not present in the table.')
        for i in idxtoignore:
            self.SeriesList[i].ignore()
