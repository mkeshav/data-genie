import json

from jinja2 import Template
import random
import string
import json

import time

_current_milli_time = lambda: int(round(time.time() * 1000))

def random_integer(max):
    return random.randint(1, max)

def random_float(max, decimal_places):
    return round(random.uniform(1, max), decimal_places)

def random_string(length):
    return ''.join([random.choice(string.ascii_letters) for i in range(0, length)])

def random_string_with_special_chars(length):
    special = ["¢", "£", "¥"]
    random_chars = [random.choice(string.ascii_letters + ''.join(special)) for i in range(0, length - 1)]
    return ''.join([random.choice(special)] + random_chars)

def random_string_list(list_size, item_length):
    l = []
    for i in range(0, list_size):
        l.insert(0, ''.join([random.choice(string.ascii_letters) for i in range(0, item_length)])) 
    #json dumps is to get python list as json compatible string.
    return json.dumps(l)

def random_integer_list(list_size, max):
    l = []
    for i in range(0, list_size):
        l.insert(0, random_integer(max)) 
    return l

def random_bool():
    return random.choice(['true', 'false'])

def now_epoch():
    return _current_milli_time()

def _create_template_with_globals(template_string):
    t = Template(template_string)
    t.globals['random_integer'] = random_integer
    t.globals['random_float'] = random_float
    t.globals['random_string'] = random_string
    t.globals['random_string_with_special_chars'] = random_string_with_special_chars
    t.globals['random_string_list'] = random_string_list
    t.globals['now_epoch'] = now_epoch
    t.globals['random_bool'] = random_bool
    t.globals['random_integer_list'] = random_integer_list
    return t

def generate(template_string):
    return _create_template_with_globals(template_string).render()

def repeat(template_string, times):
    t = _create_template_with_globals(template_string)
    entries = []
    for i in range(0, times):
        entries.insert(0, json.loads(t.render()))
        
    return json.dumps(entries)
