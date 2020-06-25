"""Simple utilities for dicom conversions"""

import os
import os.path as op
import subprocess
from glob import glob

from .colors import *

class ConversionError(Exception):
    pass

def dcm2niix(files, fname, path, overwrite=False, verbose=False):
    """Converts files using dcm2niix"""
    tempname = op.join(path, '.tmp.dcm2niix.txt')
    with open(tempname, 'w') as metafile:
        for f in files:
            metafile.write(f + '\n')

    fulldest = op.join(path, fname)
    if not op.exists(path):
        os.mkdir(path)

    # Special case: in multi-echo, need to replace %e with 1
    # This is slightly unsafe in that theoretically an echo-2 could exist bu
    # not an echo-1, but this seems unlikely 
    checkname = fulldest.replace('%e', '1') + '.nii'
    if op.exists(checkname) or op.exists(checkname + '.gz'):
        if not overwrite:
            raise ValueError('File ' + fulldest + ' would be overwritten.')
        elif op.exists(checkname):
            os.remove(checkname)
        elif op.exists(checkname + '.gz'):
            os.remove(checkname + '.gz')

    args = ['dcm2niix', '-o', path, '-f', fname, '-s', 'y', tempname]

    if verbose:
        completion = subprocess.run(args)
    else:
        completion = subprocess.run(args, encoding='utf-8', 
                                    stderr=subprocess.STDOUT,
                                    stdout=subprocess.PIPE)

    os.remove(tempname)

    if completion.returncode:
        if verbose:
            raise ConversionError('dcm2niix failed')
        else:
            raise ConversionError('dcm2niix failed: ' + completion.stdout)
