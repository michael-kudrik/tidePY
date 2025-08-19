import argparse

parser = argparse.ArgumentParser()
#parser.add_argument("locations", help="list buoy locations")
parser.add_argument("double", help="multiplies by two", type=int)
args=parser.parse_args()
print(args.double*2)