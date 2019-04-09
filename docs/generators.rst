Available Generators
=====================

Available Generators

.. code-block:: python

   from genie_pkg.generators import *

   # Email Address
   email_id = generate_email_id(20, domain='dummy.com')

   # ip address v4
   generate_ip(v=4)

   # ip address v6
   generate_ip(v=6)

   # ip v4 inside a subnet
   generate_ipv4_in_subnet(subnet_cidr)

   # Generate a valid mastercard number
   random_mastercard_number()

   # Visa cards can be 13 or 16 digits in length
   random_visacard_number(length)

   # Geo coordinates around the center
   random_geo_coords(center=(-37.814, 144.963,), radius=10000, accuracy=3)


Australian postcode, city and state

.. code-block:: python

   from genie_pkg.australia import Australia

   a = Australia()
   a.get_random_state() #Returns one of australian states

   a.get_random_city_postcode(state="VIC") #Returns tuple(city, postcode)

   a.get_city(state="VIC", postcode="3000") #Returns MELBOURNE
