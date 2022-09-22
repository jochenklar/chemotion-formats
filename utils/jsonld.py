DATA_TYPE_TYPES = {
    'NMR SPECTRUM': 'NMRSpectrum',
    'NMRPEAKTABLE': 'NMRPeaktable',
    'CYCLIC VOLTAMMETRY': 'CyclicVoltammetry'
}

DATA_CLASS_TYPES = {
    'XYDATA': 'XYData',
    'XYPOINTS': 'XYPoints',
    'PEAKTABLE': 'Peaktable',
    '$OBSERVEDINTEGRALS': 'ObservedIntegrals',
    '$OBSERVEDMULTIPLETS': 'ObservedMultiplets',
    '$OBSERVEDMULTIPLETSPEAKS': 'ObservedMultipletsPeaks',
    '$CSSIMULATIONPEAKS': 'CSSimulationPeaks'
}


def convert_blocks(blocks):
    data = []
    for block in blocks:
        convert_block(data, block)
    return data


def convert_block(data, block):
    data_type = block['labeled_data_records']['DATATYPE']

    if data_type == 'LINK':
        for block in block['blocks']:
            convert_block(data, block)

    elif data_type in DATA_TYPE_TYPES:
        item = {
            '@type': DATA_TYPE_TYPES[data_type],
            'name': block['labeled_data_records']['TITLE']
        }

        for key in block['labeled_data_records'].keys():
            if key not in ['TITLE', 'DATACLASS', 'DATATYPE', 'JCAMPDX']:
                item[key.lower()] = block['labeled_data_records'][key]

        for dataset in block['datasets']:
            data_class = dataset['data_class']

            if data_class in DATA_CLASS_TYPES:
                if 'datasets' not in item:
                    item['datasets'] = []

                item['datasets'].append({
                    '@type': DATA_CLASS_TYPES[data_class],
                    'data': dataset['data']
                })

        data.append(item)
