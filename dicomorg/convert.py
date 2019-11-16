"""Simple utilities for dicom conversions"""

import os
import os.path as op
import subprocess

def dcm2niix(files, fname, path, overwrite=True, verbose=False):
    """Converts files using dcm2niix"""
    tempname = op.join(path, '.tmp.dcm2niix.txt')
    with open(tempname, 'w') as metafile:
        for f in files:
            metafile.write(f + '\n')

    fulldest = op.join(path, fname)
    if not op.exists(path):
        os.mkdir(path)
    elif op.exists(fulldest) and not overwrite:
        raise ValueError('File ' + fulldest + ' would be overwritten.')

    args = ['dcm2niix', '-o', path, '-f', fname, '-s', 'y', tempname]

    if verbose:
        completion = subprocess.run(args)
    else:
        completion = subprocess.run(args, stdout=subprocess.DEVNULL)

    os.remove(tempname)

    if completion.returncode:
        raise Exception('dcm2niix failed')
