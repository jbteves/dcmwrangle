import dcmtable
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('location', help='location of dicoms to sort out')
args = parser.parse_args()

thistable = dcmtable.dcmtable(args.location)
print(thistable)

DCMINSTRUCTIONS = 'Please type (i)gnore, (a)lias, (h)elp, or (q)uit.'
HELPTEXT = ('Use ignore to remove certain series numbers from the table. '
            'Enter the numbers as space-delimited lists, e.g.,\n'
            '1 2 3\n'
            'Use alias to set a certain series number to have an '
            'alternative name. Enter the numbers of the series followed by '
            'your preffered aliases, e.g.,\n'
            '10 myalias 11 otheralias\n')

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
    else:
        print('Unrecognized command ' + userinput)
    print(thistable)
