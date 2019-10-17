#!/usr/bin/env python3

import os.path as op
import readline
from util.util import dcmtable, dcmseries
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('location', help='location of dicoms to sort out')
    args = parser.parse_args()

    thistable = dcmtable(args.location)
    print(thistable)

    DCMINSTRUCTIONS = ('Please type (i)gnore, (a)lias, (u)ndo, (r)edo, '
                       '(c)onvert, '
                       '(h)elp, or (q)uit.')
    HELPTEXT = ('Use ignore to remove certain series numbers from the '
                'table. '
                'Enter the numbers as space-delimited lists, e.g.,\n'
                '1 2 3\n'
                'Use alias to set a certain series number to have an '
                'alternative name. Enter the numbers of the series '
                'followed by '
                'your preffered aliases, e.g.,\n'
                '10 myalias 11 otheralias\n'
                'Undo will undo your latest change and restore the table '
                'to '
                'its previous state.\n'
                'Redo will redo your latest undo and restore the table to '
                'its future state. Note that using an ignore or alias '
                'command '
                'will prohibit you from using redo do due its simple '
                'implementation.\n')

    print(DCMINSTRUCTIONS)
    userinput = ''

    while True:
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
            thistable = thistable.alias(input('>> '))
        elif userinput == 'u':
            if thistable.prevtable:
                tempstate = thistable.copy()
                thistable = thistable.prevtable
                thistable.nexttable = tempstate.copy()
            else:
                print('No changes to undo')
        elif userinput == 'r':
            if thistable.nexttable:
                thistable = thistable.nexttable
            else:
                print('No changes to redo')
        elif userinput == 'c':
            print('Enter output destination (leave blank for in-place)')
            niidest = op.expanduser(input('<<'))
            if niidest == '':
                thistable.convert()
            else:
                thistable.convert(niidest)
            print('Converted successfully!')
        else:
            print('Unrecognized command ' + userinput)
        print(thistable)

if __name__ =='__main__':
    main()
