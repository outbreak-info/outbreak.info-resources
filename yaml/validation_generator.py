import json
import csv
import os

with open('yaml/csvs/naid_test.csv', 'r') as fin:
    csv_reader = csv.reader(fin)

    validation = {}
    validation["$validation"]  = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties" : {},
        "required" : [],
        "definitions" : {}
    }

    cols = []
    for row in csv_reader:
        if len(cols) == 0:
            cols = row
        else:  
            variable_name = row[cols.index("variable name")]
            variable_description = row[cols.index("variable name")]
            variable_type = row[cols.index("expected type")]
            is_required = row[cols.index("marginality")] == "required"

            validation["$validation"]["properties"][variable_name] = {
                "description" : variable_description,
                "type" : variable_type,
            }

            if is_required:
                validation["$validation"]["required"].append(variable_name)

    with open ('yaml/json_out/naid_test.json', 'w') as fout: 
        fout.write(json.dumps(validation, indent=2))