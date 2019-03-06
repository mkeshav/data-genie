import pytest
import sys
import os
import json

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../genie_pkg")

from json_genie import generate, generate_with_custom_template_function
from jsonschema import validate
from jinja2 import Template
import random

def test_almighty():
    schema = {
        "type": "object",
        "properties": {
            "k1" : {"type" : "number"},
            "k2" : {"type" : "string"},
            "k3" : {"type" : "array", "items": {"type": "string"}},
            "k4" : {"type" : "number"},
            "k5" : {"type" : "boolean"},
            "k6" : {"type" : "number"},
            "k7" : {"type" : "string"},
            "k8" : {
                "type": "array",
                "items": {
                    "anyOf": [
                        {
                            "type": "object",
                            "properties": {
                                "y1": {
                                    "type": "integer"
                                },
                                "y2": {
                                    "type": "integer"
                                }
                            },
                            "required": [
                                "y1"
                            ]
                        }
                    ]
                }
            },
            "k9": {"type": "array", "items": {"type": "integer"}},
            "k10": {"type": "string"}
        }
    }

    template = '''
        {
            "k1": {{random_integer(1000)}},
            "k2": "{{random_string_with_special_chars(5)}}",
            "k3": {{random_string_list(2, 8)}},
            "k4": {{random_float(100, 2)}},
            "k5": {{random_bool()}},
            "k6": {{now_epoch()}},
            "k7": "{{random_string(5)}}",
            "k8": [
                {
                    "y1": {{random_integer(1000)}}
                },
                {
                    "y1": {{random_integer(1000)}}
                }
            ],
            "k9": {{random_integer_list(2, 100)}},
            "k10": "{{guid()}}"
        }
    '''
    d = json.loads(generate(template))
    validate(instance=d, schema=schema)

fruit_choices = ['mango', 'apple', 'durian', 'jackfruit']
def favourite_fruit():
    return random.choice(fruit_choices)

def test_generate_with_custom_template_function():
    template = '''
        {
            "k1": {{random_integer(1000)}},
            "k2": "{{favourite_fruit()}}"
        }
    '''

    schema = {
        "type": "object",
        "properties": {
            "k1" : {"type" : "number"},
            "k2" : {"type" : "string", "enum": fruit_choices}
        }
    }

    t = Template(template)
    t.globals['favourite_fruit'] = favourite_fruit

    d = json.loads(generate_with_custom_template_function(t))
    validate(instance=d, schema=schema)