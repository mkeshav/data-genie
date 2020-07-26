import json
import random
from typing import NewType

from jinja2 import Template

from genie_pkg.generators import *
import string

def random_string_list(list_size, item_length):
    l = []
    for _ in range(0, list_size):
        l.insert(0, ''.join([random.choice(string.ascii_letters)
                             for _ in range(0, item_length)]))
    # json dumps is to get python list as json compatible string.
    return json.dumps(l)


def random_integer_list(list_size, start, max):
    l = []
    for _ in range(0, list_size):
        l.insert(0, random_integer(start, max))
    return l


def random_choice_of(choices) -> str:
    return str(one_of(choices))


def random_email_id(width, domain) -> str:
    return generate_email_id(width, domain)


def random_ipv4() -> str:
    return generate_ip()


def date_with_format(format_string='%Y/%m/%d', delta_days=0):
    return random_date_from_today(format_string, delta_days)


def random_geo(center=(-37.814, 144.963,), radius=10000, accuracy=3):
    x0, y0 = random_geo_coords(center, radius, accuracy)
    return json.dumps({"latitude": x0, "longitude": y0})


def random_text():
    return random_wonderland_text()

JinjaTemplate = NewType('JinjaTemplate', Template)


def _add_template_functions(template: JinjaTemplate) -> JinjaTemplate:
    template.globals['random_integer'] = random_integer
    template.globals['random_float'] = random_float
    template.globals['random_string'] = random_string
    template.globals['random_string_with_special_chars'] = random_string_with_special_chars
    template.globals['random_string_list'] = random_string_list
    template.globals['now_epoch'] = now_epoch
    template.globals['random_bool'] = random_bool
    template.globals['random_integer_list'] = random_integer_list
    template.globals['guid'] = guid
    template.globals['random_choice_of'] = random_choice_of
    template.globals['date_with_format'] = date_with_format
    template.globals['random_email_id'] = random_email_id
    template.globals['random_ipv4'] = random_ipv4
    template.globals['random_geo'] = random_geo
    template.globals['random_mastercard_number'] = random_mastercard_number
    template.globals['random_visacard_number'] = random_visacard_number
    template.globals['random_text'] = random_text
    return template


def generate(template_string) -> str:
    '''
        Generate json data for the provided specification

        Args:
            template_string (str): Jinja template string

        Returns:
            data (str): Jinja template rendered.
    '''

    t = Template(template_string)
    return _add_template_functions(t).render()


def generate_with_custom_template_function(template: JinjaTemplate) -> str:
    '''
        Generate json data for the provided specification

        Args:
            template (Template): Jinja template

        Returns:
            data (str): Jinja template rendered.
    '''

    return _add_template_functions(template).render()
