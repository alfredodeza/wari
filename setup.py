import re


module_file = open("wari/__init__.py").read()
metadata = dict(re.findall("__([a-z]+)__\s*=\s*'([^']+)'", module_file))
long_description = open('README.rst').read()

from setuptools import setup, find_packages

setup(
    name             = 'wari',
    description      = 'personal OTP (one time password) manager',
    packages         = find_packages(),
    author           = 'Alfredo Deza',
    author_email     = 'contact [at] deza.pe',
    version          = metadata['version'],
    url              = 'http://github.com/alfredodeza/wari',
    scripts          = ['bin/wari'],
    license          = "MIT",
    zip_safe         = False,
    keywords         = "otp, one time password, cli, manager",
    install_requires = ['tambo', 'pyperclip', 'onetimepass', 'nosqlite'],
    long_description = long_description,
    classifiers      = [
                        'Development Status :: 4 - Beta',
                        'Intended Audience :: Developers',
                        'License :: OSI Approved :: MIT License',
                        'Topic :: Utilities',
                        'Operating System :: MacOS :: MacOS X',
                        'Operating System :: POSIX',
                        'Programming Language :: Python :: 2.6',
                        'Programming Language :: Python :: 2.7',
                        'Programming Language :: Python :: Implementation :: PyPy'
                      ]
)
