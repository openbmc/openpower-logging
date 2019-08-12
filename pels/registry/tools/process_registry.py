#!/usr/bin/env python

import argparse
import json
import sys

r"""
Does processing on the PEL message registry JSON, such as validating
it.
"""


def check_duplicate_names(registry_json):
    r"""
    Check that there aren't any message registry entries with the same
    'Name' field.  There may be a use case for this in the future, but there
    isn't right now.

    registry_json: The message registry JSON
    """

    names = {}
    for entry in registry_json['PELs']:
        if entry['Name'] in names.keys():
            sys.exit("Found multiple uses of error Name: " + entry['Name'])
        else:
            names[entry['Name']] = {}


def validate_schema(registry, schema):
    r"""
    Validates the passed in JSON against the passed in schema JSON

    registry: Path of the file containing the registry JSON
    schema:   Path of the file containing the schema JSON
    """
    import jsonschema

    with open(registry) as registry_handle:
        registry_json = json.load(registry_handle)

        with open(schema) as schema_handle:
            schema_json = json.load(schema_handle)

            try:
                jsonschema.validate(registry_json, schema_json)
            except jsonschema.ValidationError as e:
                print(e)
                sys.exit("Schema validation failed")

        check_duplicate_names(registry_json)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='PEL message registry processor')

    parser.add_argument('-v', '--validate', action='store_true',
                        dest='validate',
                        help='Validate the JSON using the schema')

    parser.add_argument('-s', '--schema-file', dest='schema_file',
                        help='The message registry JSON schema file')

    parser.add_argument('-r', '--registry-file', dest='registry_file',
                        help='The message registry JSON file')

    args = parser.parse_args()

    if args.validate:
        if not args.schema_file:
            sys.exit("Schema file required")

        if not args.registry_file:
            sys.exit("Registry file required")

        validate_schema(args.registry_file, args.schema_file)
