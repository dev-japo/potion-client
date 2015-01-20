# Copyright 2014 Novo Nordisk Foundation Center for Biosustainability, DTU.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import string
from jsonschema import validate
from potion_client.constants import *


def camelize(a_string):
    assert isinstance(a_string, str)
    return "".join([part.capitalize() for part in a_string.replace("-", "_").split("_")])


def params_to_dictionary(params_string):
    d = {}
    for part in params_string.split("&"):
        key, value = part.split("=")
        if key not in d:
            d[key] = []
        d[key].append(value)

    for key in d.keys():
        if len(d[key]) == 1:
            d[key] = d[key][0]

    return d


def dictionary_to_params(d):
    s = []
    for key, value in d.items():
        s.append("%s=%s" % (key, value))

    return "&".join(s)


def extract_keys(a_string, formatter=string.Formatter()):
    format_iterator = formatter.parse(a_string)
    return [t[1] for t in format_iterator if not t[1] is None]


def validate_schema(schema, obj):
    if schema is not None:
        validate(obj, schema)
    return obj


def convert_value_list(values, definition):
    return [convert_value(value, definition) for value in values]


def convert_value_dict(dictionary, definition):
    if PROPERTIES in definition:
        return_obj = {}
        for key in definition[PROPERTIES].keys():
            return_obj[key] = dictionary[definition[PROPERTIES][key][FORMAT]]
        return return_obj
    else:
        return dictionary


def convert_value_object(obj, definition):
    if PROPERTIES in definition:
        return_obj = {}
        for key in definition[PROPERTIES].keys():
            return_obj[key] = getattr(obj, definition[PROPERTIES][key][FORMAT])
        return return_obj
    else:
        return obj


def convert_empty_value_type(definition):
    python_types = type_for(definition[TYPE])
    if type(None) in python_types:
        return None

    if len(python_types) == 1:
        if list in python_types:
            return []
        if dict in python_types:
            return {}


def convert_value(value, definition):
    if value is None:
        return convert_empty_value_type(definition)
    elif isinstance(value, list):
        return convert_value_list(value, definition)
    elif isinstance(value, dict):
        return convert_value_dict(value, definition)
    elif isinstance(value, object):
        return convert_value_object(value, definition)
    else:
        return value


def type_for(json_type):
    if isinstance(json_type, str):
        return [TYPES[json_type]]
    else:
        return [TYPES[t] for t in json_type]


def parse_uri(uri):
    split = uri.split("/")
    resource_name, resource_id = split[-2], split[-1]
    return resource_name, resource_id


def evaluate_list(a_list, client):
    if len(a_list) > 0:
        if isinstance(a_list[0], dict) and REF in a_list[0]:
            return [evaluate_ref(el[REF], client) for el in a_list]

    return a_list


def evaluate_ref(uri, client):
    resource_name, resource_id = parse_uri(uri)
    klass = client.resource(resource_name)
    return klass(resource_id)


