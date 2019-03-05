import pytest
import sys
import os
import json

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../genie_pkg")

from json_genie import generate, repeat

def test_simple():
    template = '''
        {
            "id": {{random_integer(1000)}},
            "k2": "{{random_string_with_special_chars(5)}}",
            "k3": {{random_string_list(2, 8)}}
        }
    '''
    d = json.loads(generate(template))
    assert set(d.keys()) == set(['id', 'k3', 'k2'])

def test_list():
    template = '''
        [
            {
                "id": {{random_integer(1000)}}
            }
        ]
    '''
    print(generate(template))
    l = json.loads(generate(template))

    assert set(l[0].keys()) == set(['id'])

def test_repeat():
    template = '''
        {
            "id": {{random_integer(1000)}}
        }
    '''
    d = json.loads(repeat(template, 2))
    assert len(d) == 2
