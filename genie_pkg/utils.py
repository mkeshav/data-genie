import random
import string

def generate_email(width, domain):
    actual_length = width - len(domain) - 1 # 1 for @
    if actual_length <= 0:
        minimum_expected_length = len(domain) + 2 # 1 for @
        raise Exception("With the domain {0}, Minimum length you should pass is {1}".format(domain, minimum_expected_length))

    local_part = [random.choice(string.ascii_letters) for i in range(0, actual_length)]
    return ''.join(local_part) + '@' + domain
