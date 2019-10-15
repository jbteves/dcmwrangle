import dcmtable
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('location', help='location of dicoms to sort out')
args = parser.parse_args()

thistable = dcmtable.dcmtable(args.location)
print(thistable)

DCMINSTRUCTIONS = 'Please type (i)gnore, (h)elp, or (q)uit.'
HELPTEXT = ('Use ignore to remove certain series numbers from the table. '
            'Enter the numbers as space-delimited lists, e.g., 1 2 3')

print(DCMINSTRUCTIONS)
userinput = ''

while True:
    userinput = input('>> ')
    if userinput == 'i':
        userinput = input('>> ')
        inputvalues = userinput.split(' ')
        thistable.ignore(inputvalues)
        print(thistable)
    elif userinput == 'h':
        print(HELPTEXT)
    elif userinput == 'q':
        break
    else:
        print('Unrecognized command ' + userinput)
