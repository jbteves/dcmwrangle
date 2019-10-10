import dcmtable
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('location', help='location of dicoms to sort out')
args = parser.parse_args()

thistable = dcmtable.dcmtable(args.location)
print(thistable)
