#/usr/bin/env python
# -*- coding : utf-8 -*-


import os
import os.path as op
import shutil
from copy import copy
import subprocess
import pydicom

class dcmtable:
    def __init__(self, path=None, prevtable=None, nexttable=None):
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
            self.prevtable = prevtable
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
        elif nexttable:
            self.seriesnumbers = copy(nexttable.seriesnumbers)
            self.seriesnumbers = copy(nexttable.seriesnumbers)
            self.SeriesList = []
            for o in nexttable.SeriesList:
                self.SeriesList.append(dcmseries(o.get_seriesnumber(),
                                                 o.get_seriesname(),
                                                 o.get_files(),
                                                 o.get_start()))
                self.SeriesList[-1].set_alias(o.get_alias())
            self.nexttable = nexttable
            self.prevtable = prevtable
            self.path = copy(nexttable.path)
        elif prevtable:
            self.seriesnumbers = copy(prevtable.seriesnumbers)
            self.SeriesList = []
            for o in prevtable.SeriesList:
                self.SeriesList.append(dcmseries(o.get_seriesnumber(),
                                                 o.get_seriesname(),
                                                 o.get_files(),
                                                 o.get_start()))
                self.SeriesList[-1].set_alias(o.get_alias())
            self.prevtable = prevtable
            self.path = copy(prevtable.path)
    def __str__(self):
        retstr = ''
        for s in self.SeriesList:
            if s.is_ignorable():
                continue
            retstr += str(s) + '\n'
        return retstr
    def ignore(self, toignore):
        newtable = dcmtable(prevtable=self)
        newtable.nexttable = None
        idxtoignore = []
        for ignorable in toignore:
            ispresent = False
            for i in range(len(newtable.seriesnumbers)):
                number = str(newtable.seriesnumbers[i])
                if ignorable == number:
                    ispresent = True
                    idxtoignore.append(i)
                    break
            if not ispresent:
                raise Exception(ignorable + 'is not present in the table.')
        for i in idxtoignore:
            newtable.SeriesList[i].ignore()
        return newtable
    def alias(self, aliasinstructions):
        newtable = dcmtable(prevtable=self)
        newtable.nexttable = None
        aliaswords = aliasinstructions.split(' ')
        if len(aliaswords) % 2 != 0:
            raise Exception('Alias indices are not paired with aliases.')
        idxtoalias = []
        aliases = []
        for i in range(round(len(aliaswords)/2)):
            try:
                series_to_alias = int(aliaswords[i*2])
                idxtoalias.append(series_to_alias)
            except:
                raise Exception(aliaswords[i] + ' cannot be converted to '
                                'a series number.')
            aliases.append(aliaswords[i*2+1])
        for i in range(len(idxtoalias)):
            iscontained = False
            for j in range(len(newtable.seriesnumbers)):
                if str(idxtoalias[i]) == str(newtable.seriesnumbers[j]):
                    aliasedseries = newtable.SeriesList[j]
                    aliasedseries.set_alias(aliases[i])
                    iscontained = True
            if not iscontained:
                raise Exception('Given index ' + str(idxtoalias[i]) + 
                                ' is not in range.')
        return newtable
    def copy(self):
        newtable = dcmtable(prevtable=self)
        newtable.path = copy(self.path)
        newtable.seriesnumbers = copy(self.seriesnumbers)
        newtable.seriesnumbers = copy(self.seriesnumbers)
        newtable.SeriesList = []
        for o in self.SeriesList:
            newtable.SeriesList.append(dcmseries(o.get_seriesnumber(),
                                             o.get_seriesname(),
                                             o.get_files(),
                                             o.get_start()))
            newtable.SeriesList[-1].set_alias(o.get_alias())
        newtable.nexttable = self.nexttable
        newtable.prevtable = self.prevtable
        return newtable
    def convert(self, outpath=None):
        if not outpath:
            outpath = self.path
        for s in self.SeriesList:
            if s.is_ignorable():
                continue
            to_copy = s.get_files()
            if s.get_alias():
                fname = s.get_alias()
            else:
                fname = s.get_seriesname()
            orgdicom = op.join(self.path, fname)

            if not op.exists(orgdicom):
                os.mkdir(orgdicom)
            for f in to_copy:
                shutil.copyfile(f, op.join(orgdicom, op.basename(f)))

            if not op.exists(outpath):
                try:
                    os.mkdir(outpath)
                except OSError:
                    raise Exception('Could not make a directory')

            dcm2niix_args = ['dcm2niix', '-o', outpath, '-f',
                             fname, orgdicom]
            completion = subprocess.run(dcm2niix_args, 
                                        stdout=subprocess.DEVNULL)
            if completion.returncode != 0:
                raise Exception('dcm2niix failed')
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
        return copy(self.seriesname)
    def get_files(self):
        """Returns the filenames in the series
        Returns
        -------
        A copy of the series files
        """
        return copy(self.files)
    def get_start(self):
        """Returns the start time of the series as defined in the header
        -------
        A string of the start time
        """
        return copy(self.start)
    def get_alias(self):
        return copy(self.alias)
    def is_ignorable(self):
        """Returns whether the series is ignorable
        Returns
        -------
        Whether the series is ignorable
        """
        return self.alias == ''
