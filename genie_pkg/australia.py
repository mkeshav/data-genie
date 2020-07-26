from pkg_resources import resource_string
import json
from genie_pkg.generators import one_of, random_geo_coords
from genie_pkg import GenieException

class Australia(object):
    def __init__(self):
        self.data = json.loads(resource_string(__name__, 'data/oz_postcodes.json'))

    
    def get_random_state(self) -> str:
        return one_of(list(self.data.keys()))

    def get_random_city_postcode(self, state) -> (str, str):
        state_data = self.data[state]
        post_codes = list(state_data.keys())      
        pc = one_of(post_codes)
        locality = state_data[pc]["localities"]
        return (locality, pc)

    def get_city(self, state, postcode):
        localities = self.data[state][postcode]["localities"]
        return one_of(localities)
        
    def get_random_geo_coordinate(self, state, postcode):
        center = self.data[state][postcode].get("center", {})
        if center:
            c = (float(center["latitude"]), float(center["longitude"]),)
            return random_geo_coords(center=c)
        else:
            raise GenieException("Postcode {0} in state {1} does not have geo center".format(postcode, state))