#/usr/bin/env python
# -*- coding : utf-8 -*-


import os
import os.path as op
import shutil
from copy import copy
import subprocess
import pydicom
from pydicom import dcmread

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
        self.tablepath = path
        # Preallocate; for large datasets this improves runtime
        self.filemap = dict.fromkeys(range(len(pathcontents)))
        self.filelist = ['' for i in range(len(pathcontents))]
        toremove = []

        # Not all files are actually going to be dicoms, need to check
        end_idx = 0
        for i in range(len(pathcontents)):
            f = op.join(self.tablepath, pathcontents[i])
            try:
                self.filemap[f] = dcmread(f, stop_before_pixels=True)
                self.filelist[i] = f
                end_idx += 1
            except (IsADirectoryError, pydicom.errors.InvalidDicomError):
                pass

        # Slice out blank elements
        self.filelist[:end_idx+1]

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
    def __init__(self, pathtable, prevtable=None, nexttable=None):
        if (not prevtable and not nexttable):
            groups, _ = pathtable.group_by_attribute('SeriesNumber')
            self.pathtable = pathtable
            self.SeriesList = [None for i in groups]
            self.nexttable = None
            self.prevtable = None
            for i in range(len(groups)):
                self.SeriesList[i] = dcmseries(pathtable, groups[i])
        elif nexttable:
            self.pathtable = pathtable
            self.SeriesList = []
            for s in nexttable.SeriesList:
                self.SeriesList.append(dcmseries(pathtable, 
                                                 s.get_files(), s))
            self.nexttable = nexttable
            if self.prevtable:
                self.prevtable = prevtable
        else:
            self.pathtable = pathtable
            self.SeriesList = []
            for s in prevtable.SeriesList:
                self.SeriesList.append(dcmseries(pathtable,
                                                 s.get_files(), s))
                self.SeriesList[-1].set_alias(s.get_alias())
            self.prevtable = prevtable
    def __copy__(self):
        newtable = type(self)
        self.pathtable = copy.pathtable
        self.SeriesList = []
        for s in copy.SeriesList:
            self.SeriesList.append(s)
        self.nexttable = copy.nexttable
        self.prevtable = copy.prevtable

        return newtable
    def __str__(self):
        retstr = ''
        for s in self.SeriesList:
            if s.is_ignorable():
                continue
            retstr += str(s) + '\n'
        return retstr
    def isempty(self):
        return len(self.SeriesList) == 0
    def ignore(self, toignore):
        newtable = seriestable(self.pathtable, prevtable=self)
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
                raise Exception(ignorable + 'is not present in the table.')
        for i in idxtoignore:
            newtable.SeriesList[i].ignore()
        return newtable
    def alias(self, aliasinstructions):
        newtable = seriestable(self.pathtable, prevtable=self)
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
    def __init__(self, filetable, filegroup, tocopy=None):
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
        if tocopy:
            self.name = tocopy.name
            self.number = tocopy.number
            self.start = tocopy.start
            self.files = tocopy.files
            self.alias = tocopy.alias
        else:
            header = filetable.access(filegroup[0])
            self.name = header.SeriesDescription
            self.number = header.SeriesNumber
            self.start = header.SeriesTime
            self.files = filegroup
            self.alias = None


    def __copy__(self):
        return dcmseries(None, None, self)
        

    def __str__(self):
        """String representation of the dcmseries
        """
        if self.alias:
            return '{:3d}\t{:30s}\t{:20s}\t{:5d}'.format(self.number,
                                                  self.alias,
                                                  self.start,
                                                  len(self.files))
        else:
            return '{:3d}\t{:30s}\t{:20s}\t{:5d}'.format(self.number,
                                                  self.name,
                                                  self.start,
                                                  len(self.files))
    def ignore(self):
        """Makes this dicom series ignored in printing"""
        self.alias = ''
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
