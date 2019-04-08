from pkg_resources import resource_string
import json
from random import choice

class Australia(object):
    def __init__(self):
        self.data = json.loads(resource_string(__name__, 'data/oz_postcodes.json'))

    
    def get_state(self) -> str:
        return choice(list(self.data.keys()))
    