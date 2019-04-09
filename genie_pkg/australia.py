from pkg_resources import resource_string
import json
from genie_pkg.generators import one_of, random_geo_coords

class Australia(object):
    def __init__(self):
        self.data = json.loads(resource_string(__name__, 'data/oz_postcodes.json'))

    
    def get_random_state(self) -> str:
        return one_of(list(self.data.keys()))

    def get_random_postcode(self, state) -> str:
        state_data = self.data[state]
        post_codes = list(state_data.keys())        
        return one_of(post_codes)

    
    def get_random_geo_coordinate(self, state, postcode):
        center = self.data[state][postcode].get("center", {})
        if center:
            c = (float(center["latitude"]), float(center["longitude"]),)
            return random_geo_coords(center=c)
        else:
            raise Exception("Postcode {0} in state {1} does not have geo center".format(postcode, state))