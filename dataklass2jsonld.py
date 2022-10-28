#!/usr/bin/env python3
import argparse
import json
import sys

from utils.dataklass import convert_data

parser = argparse.ArgumentParser()
parser.add_argument('dataklass_file')
parser.add_argument('data_file')
parser.add_argument('-o|--output_file', dest='output_file', default=None)

args = parser.parse_args()

with open(args.dataklass_file) as fp:
    dataklass = json.load(fp)

with open(args.data_file) as fp:
    data = json.load(fp)

jsonld = convert_data(dataklass, data)

fp = open(args.output_file, 'w') if args.output_file is not None else sys.stdout
json.dump(jsonld, fp, indent=2)
fp.close()
