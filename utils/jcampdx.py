import warnings

from nmrglue.fileio.jcampdx import _getkey, _parse_data

DATASET_KEYS = [
    'XYDATA',
    'XYPOINTS',
    'PEAKTABLE',
    '$OBSERVEDINTEGRALS',
    '$OBSERVEDMULTIPLETS',
    '$OBSERVEDMULTIPLETSPEAKS',
    '$CSSIMULATIONPEAKS'
]


def parse_key(string):
    return _getkey(string)


def parse_value(string):
    try:
        return int(string)
    except ValueError:
        try:
            return float(string)
        except ValueError:
            return string.strip()


def parse_line(line):
    return [parse_value(value) for value in line.strip()
                                                .strip('(')
                                                .strip(')')
                                                .split(',')]


def parse_buffer(buffer):
    # use nmrglues function to parse the 1D array
    return [value for value in _parse_data(buffer)[0]]


def read_blocks(file_path):
    blocks = []
    current_blocks = blocks
    current_block = None
    current_dataset = None
    current_buffer = ''

    with open(file_path) as fp:
        for line in fp.readlines():
            if not line.strip():
                # ignore empty lines
                pass

            elif line.startswith('$$'):
                # ignore comments
                pass

            elif line.startswith('##'):
                # try to parse the labeled data record
                try:
                    key, value = line.strip().lstrip('#').split('=')
                except ValueError:
                    warnings.warn('Could not parse line: "{}"'.format(line), RuntimeWarning)
                    continue

                key = parse_key(key)
                value = parse_value(value)

                if key == 'TITLE':
                    # TITLE indicates the beginning of a new block
                    if current_block is not None:
                        # if we are already in a block, store the parent block
                        # create a list of sub-blocks, and move down the hierarchy
                        parent_blocks = current_blocks
                        current_blocks = current_block['blocks'] = []

                    # create a new block and add it to current_blocks
                    current_block = {
                        'labeled_data_records': {
                            'TITLE': value
                        },
                        'datasets': []
                    }
                    current_blocks.append(current_block)

                elif key == 'END':
                    # END indicates the end of a block
                    if current_block is None:
                        # if we are not in a block, move up the hirarchy
                        # (this happens with two END after each other)
                        current_blocks = parent_blocks

                    current_block = None

                elif key not in DATASET_KEYS:
                    # regular LDR are just added to the labeled_data_records dict
                    current_block['labeled_data_records'][key] = value

                if key in DATASET_KEYS:
                    # this is the beginning of a new dataset
                    if current_buffer:
                        # if an "old" buffer exists it needs to be parsed
                        current_dataset['data'] = parse_buffer(current_buffer)

                    # create an new dataset and a new buffer, and add the dataset to the current block
                    current_dataset = {
                        'data_class': key,
                        'data': []
                    }
                    current_buffer = ''
                    current_block['datasets'].append(current_dataset)

                else:
                    if current_buffer:
                        # if there is a current_buffer, this is the end of a dataset, so it needs to be parsed
                        current_dataset['data'] = parse_buffer(current_buffer)

                    current_dataset = None
                    current_buffer = ''

            elif current_dataset is not None:
                # if we are "in" a dataset add the line to the buffer or the dataset
                if current_dataset['data_class'] == 'XYDATA':
                    current_buffer += line
                else:
                    current_dataset['data'].append(parse_line(line))

    return blocks
