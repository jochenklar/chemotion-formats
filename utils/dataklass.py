def convert_data(dataklass, data):
    jsonld = {
        '@context': {}
    }

    for layer_name, layer in data.items():
        for field_name, field in layer.items():
            dataklass_fields = dataklass['layers'].get(layer_name, {}).get('fields', [])
            dataklass_field = next((f for f in dataklass_fields if f['field'] == field_name), None)

            rdf_field = dataklass_field.get('rdf_field', field_name)
            rdf_subfield = dataklass_field.get('rdf_subfield')
            rdf_property = dataklass_field.get('rdf_property')

            if rdf_field not in jsonld['@context']:
                jsonld['@context'][rdf_field] = rdf_property

            if rdf_subfield is None:
                jsonld[rdf_field] = field

            else:
                if rdf_field not in jsonld:
                    jsonld[rdf_field] = {}

                jsonld[rdf_field][rdf_subfield] = field

    return jsonld
