import sys

from tambo import Transport
from wari import logger
import wari
from wari.decorators import catches
from wari.hotp import Hotp
from wari.totp import Totp


class Wari(object):
    _help = """
wari: A small OTP manager and utility to store user's keys and/or generate them
for other services.

Version: %s

Commands:

hotp                 Subcommand to interact with event based tokens (HOTP)
totp                 Subcommand to interact with time based tokens (TOTP)


    """

    mapper = {
            'totp': Totp,
            'hotp': Hotp,
    }

    def __init__(self, argv=None, parse=True):
        if argv is None:
            argv = sys.argv
        if parse:
            self.main(argv)

    def help(self):
        return self._help % wari.__version__

    @catches(KeyboardInterrupt)
    def main(self, argv):
        parser = Transport(argv, mapper=self.mapper,
                           check_help=False,
                           check_version=False)
        parser.parse_args()
        parser.catch_help = self.help()
        parser.catch_version = wari.__version__
        parser.mapper = self.mapper
        if len(argv) <= 1:
            return parser.print_help()

        # create the connection and set the collection
        conn = wari.db.get_connection()
        wari.db.connection = conn
        wari.db.collection = conn['wari']

        parser.dispatch()
        parser.catches_help()
        parser.catches_version()
        conn.close()
