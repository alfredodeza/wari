import socket
import os
import getpass
import base64
import binascii
import pyperclip
from subprocess import Popen, PIPE
from tambo import Transport
import onetimepass as otp
from wari import db, logger


def prompt_pass():
    prefix = logger.LogMessage('info', 'Type secret: ').line(newline=False)
    return getpass.getpass(prefix)


def prompt(question, default=None, lowercase=False, _raw_input=None):
    """
    A more basic prompt which just needs some kind of user input, with the
    ability to pass in a default and will sanitize responses (e.g. striping
    whitespace).
    """
    input_prompt = _raw_input or raw_input
    prefix = logger.LogMessage('info', question).line(newline=False)

    if default:
        prompt_format = '{prefix} [{default}] '.format(
            prefix=prefix,
            question=question,
            default=default
        )
    else:
        prompt_format = '{prefix} '.format(prefix=prefix, question=question)
    response = input_prompt(prompt_format)
    if not response:  # e.g. user hit Enter
        return default
    else:
        response = str(response).strip()
        if lowercase:
            return response.lower()
        return response


# XXX need to check if `openssl` is available and error accordingly
# XXX need to handle errors from Popen
def create_secret_key():
    p = Popen(['openssl',  'rand',  '-hex',  '20'], stdout=PIPE, stderr=PIPE)
    p.wait()
    return p.stdout.readline().strip('\n')



class Hotp(object):

    _help = """
HOTP user manager and utility for key/token generation

    get {username}                         Copy the secret and pin to the clipboard
    create {username}                      Create keys for a given user (requires username argument)
    remove {username}                      Removes the information for a stored username
    update {username} {key, step, secret}  Update items for any already stored user (key, step, or secret)
    generate                               Generates a set of HOTP keys (in both HEX and b32)
    """

    def __init__(self, argv, connection=None):
        self.argv = argv

    def parse_args(self):
        options = ['create', 'update', 'generate', 'remove', 'get']
        parser = Transport(self.argv, options=options)
        parser.catch_help = self._help
        parser.parse_args()

        if parser.has('create'):
            return self.create(parser.get('create'))

        if parser.has('update'):
            optional_args = ['key', 'step', 'secret', 'b32']
            items = [i for i in parser.arguments if i in optional_args]
            return self.update(parser.get('update'), items)

        if parser.has('generate'):
            return self.generate()

        if parser.has('remove'):
            return self.remove(parser.get('remove'))

        if parser.has('get'):
            items = [i for i in parser.arguments if i in ['pin']]
            return self.get(parser.get('get'), items)

    def get(self, username, items=[]):
        if not username:
            return logger.error('a username was not passed in')
        try:
            document = db.collection.find({'username':username}, limit=1)[0]
        except IndexError:
            return logger.warning('could not find any matching users to delete')

        key = document['key']
        step = int(document['step'])
        b32 = document['b32']

        pin = otp.get_hotp(b32, intervals_no=step)
        password = "%s%s" % (document['secret'], pin)
        if 'pin' in items:
            pyperclip.copy(pin)
            logger.info('pin copied to the clipboard')
        else:
            pyperclip.copy(password)
            logger.info('secret with generated pin has been copied to the clipboard')
        document['step'] = step + 1
        db.collection.update(document)

    def create(self, username):
        if not username:
            return logger.error('a username was not passed in')
        if db.collection.find({'username':username}):
            return logger.error('there is already an existing record for: %s' % username)
        secret = prompt_pass()
        key = create_secret_key()
        b32 =  base64.b32encode(binascii.unhexlify(key))
        db.collection.insert(
            {
                'username': username,
                'secret': secret,
                'key': key,
                'step': 1,
                'b32': b32,

            }
        )
        logger.info('created user %s' % username)
        logger.info('hex key: %s' % key)
        logger.info('b32 key: %s' % b32)
        logger.info('step: %s' % 1)

    def remove(self, username):
        if not username:
            return logger.error('this action requires a username as an argument')

        documents = db.collection.find({'username': username}, limit=1)

        if not documents:
            logger.warning('could not find any matching users to delete')
        else:
            db.collection.remove(documents[0])
            logger.info('removed entry for user: %s' % username)


    def update(self, username, items=[]):
        actions = {
            'key': lambda: prompt('key:'),
            'step': lambda: prompt('step:'),
            'b32': lambda: prompt('b32:'),
            'secret': prompt_pass,
        }

        documents = db.collection.find({'username': username}, limit=1)
        if not documents:
            return logger.error('could not find username: %s' % username)

        document = documents[0]

        for i in items:
            document[i] = actions[i]()

        db.collection.update(document)


    def generate(self):
        """
        Does not use the collection, will just spit out
        the generated keys
        """
        key = create_secret_key()
        b32 = base64.b32encode(binascii.unhexlify(key))
        logger.info('hex: %s' % key)
        logger.info('b32: %s' % b32)
