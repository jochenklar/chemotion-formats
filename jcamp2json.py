import argparse
import json

from utils.jcampdx import read_blocks
from utils.jsonld import convert_blocks

parser = argparse.ArgumentParser()
parser.add_argument('input_file')
parser.add_argument('output_file')

args = parser.parse_args()

blocks = read_blocks(args.input_file)
data = convert_blocks(blocks)

with open(args.output_file, 'w') as fp:
    json.dump(data, fp, indent=2)
