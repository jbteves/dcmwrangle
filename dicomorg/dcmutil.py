#/usr/bin/env python
# -*- coding : utf-8 -*-


import os
import os.path as op
import shutil
import copy
from copy import copy
import subprocess
import pydicom
from pydicom import dcmread
from .colors import *
from .convert import *

class dcmtable:
    """A table of all dicom files in a directory

    Attributes
    ----------
    filemap : dict
        A dict where each filename hashes to its header contents
    filelist : list
        A list where you can access files iteratively

    Methods
    -------
    group_by_attribute
        Returns a set containing all files which match an input attribute
        and value.
    get_header
        Gets the dicom header for a given filename.
   
    Notes
    -----
    There is usually no reason to have both a dict and an array, however,
    there are some cases where you might want to iterate and some cases
    where you just have a file and want to inspect it. It is much faster
    to access the dict in the latter case, at the expense of memory. This
    class is NOT memory-friendly. 

    Future idea: a list-only implementation to be lightweight,
    dcmtable_light?
    """


    def __init__(self, path):
        if not op.exists(path):
            raise ValueError('Path to read dicoms from does not exist')
        path = op.abspath(path)
        pathcontents = os.listdir(path)
        # Save the path for this table
        self.tablepath = copy(path)
        # Preallocate; for large datasets this improves runtime
        self.filemap = dict.fromkeys(range(len(pathcontents)))
        self.filelist = [None for o in pathcontents]

        # Not all files are actually going to be dicoms, need to check
        end_idx = 0
        for i in range(len(pathcontents)):
            f = op.join(self.tablepath, pathcontents[i])
            try:
                self.filemap[f] = dcmread(f, stop_before_pixels=True)
                self.filelist[end_idx] = f
                end_idx += 1
            except (IsADirectoryError, pydicom.errors.InvalidDicomError):
                pass

        self.filelist = self.filelist[:end_idx+1]


    def __str__(self):
        return ('Path: ' + self.tablepath + '\n' + 
                'Total files: ' + str(len(self.filelist)))
    
    
    def get_header(self, fname):
        """Returns the dicom header object for a given filename

        Parameters
        ----------
        fname : string
            The filename you'd like the header information for

        Returns
        -------
        dicomheader : 
        """
        try:
            return self.filemap[fname]
        except KeyError:
            return None

    def group_by_attribute(self, attribute, subset=None):
        """Returns a list of a list of files and a list of names for
        unique attributes.

        Parameters
        ----------
        attribute : string
            The attribute to group by

        Returns
        -------
        file_groups : list
            A list of filename lists. Indices correspond with
            attribute_values.
        unique_values : list
            A list of values indicating the unique attribute names.
            Indices correspond with filegroups
        """

        if subset:
            filelist = subset
        else:
            filelist = self.filelist

        attribute_values = ['' for i in filelist]
        self._test_attributes(attribute)
        for i in range(len(filelist)):
            attribute_values[i] = getattr(self.filemap[filelist[i]],
                                          attribute)

        unique_values = list(set(attribute_values))
        unique_values.sort()
        file_groups = [[] for i in unique_values]
        for i in range(len(filelist)):
            f = self.filemap[filelist[i]]
            for j in range(len(unique_values)):
                v = unique_values[j]
                if getattr(f, attribute) == v:
                    file_groups[j].append(filelist[i])

        return file_groups, unique_values


    def group_by_value(self, attribute, attribute_value, subset=None):
        relevant_files = ['' for x in self.filelist]
        total_hits = 0
        if subset:
            filelist = subset
        else:
            filelist = self.filelist

        self._test_attributes(attribute)
        # Harvest the attributes and values, populating the list
        for i in range(len(filelist)):
            f = filelist[i]
            header = self.filemap[f]
            this_value = getattr(header, attribute)
            if this_value == attribute_value:
                # Hit
                relevant_files[total_hits] = f
                total_hits += 1

        # Slice off empty
        relevant_files = relevant_files[:total_hits+1]

        # Return the file group
        return relevant_files


    def access(self, fname):
        """Return the Nifti header for any valid file
        
        Parameters
        ----------
        fname : string
            The filename to get the header of

        Returns
        -------
        The header for the file

        Raises
        ------
        ValueError if the file isn't in the table
        """
        try:
            header = self.filemap[fname]
        except:
            raise ValueError('File ' + fname + ' is not in the file table.')
        return header


    def _test_attributes(self, attribute):
        try:
            getattr(self.filemap[self.filelist[0]], attribute)
        except:
            raise ValueError('Dicom header does not contain attribute ' +
                             attribute)

        
class seriestable:
    def __init__(self, pathtable, orig=None):
        if orig:
            self.pathtable = orig.pathtable
            self.nexttable = copy(orig.nexttable)
            self.prevtable = copy(orig.prevtable)
            self.SeriesList = []
            for s in orig.SeriesList:
                self.SeriesList.append(copy(s))
        else:
            groups, numbers = pathtable.group_by_attribute('SeriesNumber')
            self.pathtable = pathtable
            self.SeriesList = [None for i in groups]
            self.nexttable = None
            self.prevtable = None
            for i in range(len(groups)):
                self.SeriesList[i] = dcmseries(pathtable, groups[i])
    def __str__(self):
        retstr = ''
        for s in self.SeriesList:
            if s.is_ignorable():
                continue
            retstr += str(s) + '\n'
        return retstr
    def __copy__(self):
        return seriestable(self.pathtable, orig=self)
        
    def isempty(self):
        return len(self.SeriesList) == 0
    def ignore(self, toignore):
        newtable = copy(self)
        newtable.prevtable = copy(self)
        newtable.nexttable = None
        idxtoignore = []
        for ignorable in toignore:
            ispresent = False
            for i in range(len(newtable.SeriesList)):
                number = str(newtable.SeriesList[i].get_number())
                if ignorable == number:
                    ispresent = True
                    idxtoignore.append(i)
                    break
            if not ispresent:
                raise Exception(ignorable + ' is not present in the table.')
        for i in idxtoignore:
            newtable.SeriesList[i].ignore()
        return newtable
    def alias(self, aliasinstructions):
        newtable = copy(self)
        newtable.prevtable = copy(self)
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
            for j in range(len(newtable.SeriesList)):
                if idxtoalias[i] == newtable.SeriesList[j].get_number():
                    aliasedseries = newtable.SeriesList[j]
                    aliasedseries.set_alias(aliases[i])
                    iscontained = True
                    break
            if not iscontained:
                raise Exception('Given index ' + str(idxtoalias[i]) + 
                                ' is not in range.')
        return newtable
    def convert(self, outpath=None):
        if not outpath:
            outpath = self.pathtable.tablepath
        for s in self.SeriesList:
            if s.is_ignorable():
                continue
            else:
                s.convert(outpath)
    

class dcmseries:
    def __init__(self, filetable, filegroup, orig=None):
        """Constructor for dcmseries
        Parameters
        ----------
        filetable
            The filetable for this series' path
        filegroup (N x 1) `array`
            An array of filenames that belong in this series
        tocopy
            A series from which to copy information
        """
        if orig:
            self.name = orig.name
            self.number = orig.number
            self.start = orig.start
            self.files = orig.files
            self.alias = copy(orig.alias)
            if orig.me:
                self.me = True
                self.echo_groups = orig.echo_groups
                self.echoes = orig.echoes
            else:
                self.me = False
        else:
            header = filetable.access(filegroup[0])
            self.name = header.SeriesDescription
            self.number = int(header.SeriesNumber)
            self.start = header.SeriesTime
            self.files = filegroup
            self.alias = None
            # Determine if multi-echo
            groups, echoes = filetable.group_by_attribute('EchoTime',
                                                          filegroup)
            if len(echoes) > 1:
                self.echo_groups = groups
                self.echoes = echoes
                self.me = True
            else:
                self.me = False

    def __copy__(self):
        return dcmseries(None, None, self)


    def __str__(self):
        """String representation of the dcmseries
        """
        if self.me:
            e = 'ME'
        else:
            e = 'SE'
        style = '{:3d}\t{:35s}\t{:15s}\t{:5d}\t{:2s}'
        if self.alias:
            return style.format(self.number, self.alias, self.start,
                                len(self.files), e)
        else:
            return style.format(self.number, self.name, self.start,
                                len(self.files), e)

    def ignore(self):
        """Makes this dicom series ignored in printing"""
        self.alias = ''
    def convert(self, outpath):
        """Converts this series"""
        if self.alias:
            fname = self.alias
        else:
            fname = self.name
        if self.me:
            fname += '_echo-%e'
            for i in range(len(self.echoes)):
                dcm2niix(self.echo_groups[i], fname, outpath,
                         overwrite=True)
        else:
            dcm2niix(self.files, fname, outpath)


    def set_alias(self, alias):
        self.alias = alias
    def get_number(self):
        """Returns the series number
        Returns
        -------
        The series number
        """
        return self.number
    def get_name(self):
        """Returns the series description/name as it is in the header
        Returns
        -------
        The series name
        """
        return copy(self.name)
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
    def is_me(self):
        """Returns whether the series is multi-echo"""
        return self.me
