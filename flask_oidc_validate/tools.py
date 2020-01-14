# encoding: utf-8

import base64
import json
import random
import string
import ssl


def base64_urldecode(s):
    ascii_string = str(s)
    ascii_string += '=' * (4 - (len(ascii_string) % 4))
    return base64.urlsafe_b64decode(ascii_string)


def base64_urlencode(s):
    return str(base64.urlsafe_b64encode(s),'utf-8').split("=")[0].replace('+', '-').replace('/', '_')


def decode_token(token):
    """
    Decode a jwt into readable format.

    :param token:
    :return: A decoded jwt, or None if its not a JWT
    """
    parts = token.split('.')

    if token and len(parts) == 3:
        return base64_urldecode(parts[0]).decode("utf-8"), base64_urldecode(parts[1]).decode("utf-8")

    # It's not a JWT
    return None


def generate_random_string(size=20):
    """
    :return: a random string with a default size of 20 bytes using only ascii characters and digits
    """
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))


def get_ssl_context(config):
    """
    :return a ssl context with verify and hostnames settings
    """
    ctx = ssl.create_default_context()

    if 'verify_ssl_server' in config and not bool(config['verify_ssl_server']):
        print ('Not verifying ssl certificates')
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    return ctx


def print_json(map):
    print (json.dumps(map, indent=4, sort_keys=True))

