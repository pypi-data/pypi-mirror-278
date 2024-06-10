"""
    This module will generate the random email
"""

import random
import string


def get_random_string():
    """
        return the random string
    """
    return "".join(random.choices(string.ascii_lowercase, k=10))


def generate_email():
    """
    generate a random string of lowercase letters
    """
    # choose a random top-level domain
    tld = random.choice(["com"])

    return f"{get_random_string()}@mailnesia.{tld}"
