# Converts all schema from .yaml format to .json
# and compiles them all together into a schema.org-style graph format
# to be used in the Data Discovery Engine (https://discovery.biothings.io/schema-playground).
# Context, etc. is taken from the last valid entry.

# Usage: `python3 assemble_schema.py -f analysis protocols` --> compiles together the analysis/protocols .yamls into outbreak.json
# or assemble(["analysis"])

import sys
import os.path
import json
import yaml
import argparse

"""
Parser inputs
"""
# setup command line argument parser
parser = argparse.ArgumentParser(description='Compile together data for CViSB from raw files')
parser.add_argument("--files", "-f", required=True,
                    # 1 or more values expected => creates a list
                    help="Enter the names of the .yaml files to be compiled together. Should not include '.yaml'-- just the bare file names",  nargs="*",
                    type=str)


def assemble(args, outfile="outbreak.json"):
    final_schema = {"@context": list(), "@id": None, "@graph": list()}
    for name in args.files:
        schema_data = read_yaml(f"{name}.yaml")
        if(schema_data["@id"]):
            final_schema["@id"] = schema_data["@id"]
        if(schema_data["@context"]):
            final_schema["@context"] = schema_data["@context"]
        final_schema["@graph"].extend(schema_data["@graph"])
    with open(outfile, 'w') as out_f:
        json.dump(schema_data, out_f, indent=2)
    return(final_schema)


def read_yaml(yaml_file):
    '''Convert input yaml file as JSON file.'''
    with open(yaml_file) as in_f:
        schema_data = yaml.safe_load(in_f)
    return(schema_data)


if __name__ == '__main__':
    assemble(parser.parse_args())
