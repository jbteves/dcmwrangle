#!/usr/bin/env python
# -*- coding : utf-8 -*-

import sys
import readline
import argparse
from dcmwrangle.colors import *
from dcmwrangle.util import *
from dcmwrangle.dcmtable import dcmtable


github_target = 'https://github.com/jbteves/dcmwrangle/issues'
prompt = '>> '

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inpath', help='directory of dicoms')
    args = parser.parse_args()
    dcmwrangle(args.inpath)

def dcmwrangle(path):
    """Allows interactive session for dicoms

    Parameters
    ----------
    path
        The path to the dicoms you'd like to wrangle.

    Raises
    ------
    ValueError
        If the path does not exist
    """
    tables = []
    tables.append(dcmtable(path))
    curr = 0
    while True:
        currtable = tables[curr]
        print(currtable)
        try:
            op, group, arg = get_statement(input(prompt))
            fn = fptable[op]
            fn(group, arg)

        except TypeError as e:
            print(red('Internal error; please post an issue to \n') +
                  blue(github_target) + '\n' +
                  red('With a copy of your table and this message: ' + 
                      str(e)))
        except ValueError as e:
            print(red(str(e)))
