#!/usr/bin/env python3
import argparse
import json
import sys

from utils.jcampdx import read_blocks, convert_blocks

parser = argparse.ArgumentParser()
parser.add_argument('input_file')
parser.add_argument('-o|--output_file', dest='output_file', default=None)

args = parser.parse_args()

blocks = read_blocks(args.input_file)
jsonld = convert_blocks(blocks)

fp = open(args.output_file, 'w') if args.output_file is not None else sys.stdout
json.dump(jsonld, fp, indent=2)
fp.close()
