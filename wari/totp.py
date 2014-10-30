import socket
import os
from subprocess import call
from tambo import Transport


class Totp(object):

    _help = """
HOTP user manager and utility for key/token generation

    create {username}                      Create keys for a given user (requires username argument)
    update {username} {key, step, secret}  Update items for any already stored user (key, step, or secret)
    generate                               Generates a set of HOTP keys (in both HEX and b32)
    """

    def __init__(self, argv, connection=None):
        self.argv = argv
        self.connection = connection

    def parse_args(self):
        options = ['create', 'update', 'generate']
        parser = Transport(self.argv, options=options)
        parser.catch_help = self._help
        parser.parse_args()
