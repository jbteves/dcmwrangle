#!/usr/bin/env python3

import os
import os.path as op
import readline
from copy import copy
from dicomorg.dcmutil import *
from dicomorg.colors import *
# Aliases; this isn't pythonic but modules are hard
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--location',
                        help='location of dicoms to sort out')
    parser.add_argument('-t', '--template',
                        help='template to use to sort the dicoms',
                        default=None)
    args = parser.parse_args()
    location = op.abspath(args.location)
    dicomorg(location, template=args.template)


def dicomorg(path, template=None):
    if template:
        print('Feature unavailable right now')
    DCMINSTRUCTIONS = ('Please type (i)gnore, (a)lias, (u)ndo, (r)edo, '
                       '(c)onvert, (f)orce convert (overwrites files), '
                       'change (p)ath, '
                       '(h)elp, or (q)uit.')
    IGNTEXT = ('Use ignore to remove certain series numbers from the '
               'table. '
               'Enter the numbers as space-delimited lists, e.g.,\n'
               '1 2 3\n')

    ALIASTEXT = ('Use alias to set a certain series number to have an '
                 'alternative name. Enter the numbers of the series '
                 'followed by '
                 'your preffered aliases, e.g.,\n'
                 '10 myalias 11 otheralias\n')

    UNDOTEXT = ('Undo will undo your latest change and restore the table '
                'to '
                'its previous state.\n')

    REDOTEXT = ('Redo will redo your latest undo and restore the table to '
                'its future state. Note that using an ignore or alias '
                'command '
                'will prohibit you from using redo do due its simple '
                'implementation.\n')

    PATHTEXT = ('Changing path will dump the current table and read a new '
                'path, creating a new table.\n')

    HELPTEXT = (IGNTEXT + ALIASTEXT + UNDOTEXT + REDOTEXT + PATHTEXT)

    print(DCMINSTRUCTIONS)
    print('Loading data...')
    userinput = ''

    currtable = dcmtable(path)
    thistable = seriestable(currtable)
    print(currtable.tablepath)

    while True:
        if thistable.isempty():
            print('This directory does not have dicoms.'
                  'Please enter a new path.')
            userinput = 'p'
        else:
            if not (userinput == 'c' or userinput == 'f'):
                print(thistable)
            userinput = input('>> ')
        if userinput == 'i':
            userinput = input('>> ')
            inputvalues = userinput.split(' ')
            thistable = thistable.ignore(inputvalues)
        elif userinput == 'h':
            print(HELPTEXT)
            continue
        elif userinput == 'q':
            break
        elif userinput == 'a':
            userinput = input('>> ')
            thistable = thistable.alias(userinput)
        elif userinput == 'u':
            if thistable.prevtable:
                temptable = copy(thistable.prevtable)
                temptable.nexttable = copy(thistable)
                thistable = temptable
            else:
                print('No changes to undo')
        elif userinput == 'r':
            if thistable.nexttable:
                thistable = thistable.nexttable
            else:
                print('No changes to redo')
        elif userinput == 'c':
            print('Enter output destination (leave blank for in-place)')
            niidest = input('>> ')
            if niidest == None or len(niidest) == 0:
                print('Sending to ' + path)
                thistable.convert()
            else:
                niidest = op.abspath(niidest)
                print('Sending to ' + niidest)
                thistable.convert(outpath=niidest)
        elif userinput == 'f':
            print('Enter output destination (leave blank for in-place)')
            niidest = input('>> ')
            if niidest == None or len(niidest) == 0:
                print('Sending to ' + path)
                thistable.convert(force=True)
            else:
                niidest = op.abspath(niidest)
                print('Sending to ' + niidest)
                thistable.convert(outpath=niidest, force=True)
        elif userinput == 'p':
            print('Enter new reading path.')
            if not thistable.isempty():
                print('WARNING: purges current table.')
            path = op.abspath(op.expanduser(input('>> ')))
            if not op.exists(newdcmpath):
                print('Given path ' + newdcmpath + ' does not exist!')
                continue
            currtable = dcmtable(newdcmpath)
            thistable = seriestable(newdcmpath)
        else:
            print('Unrecognized command ' + userinput)

if __name__ =='__main__':
    main()
