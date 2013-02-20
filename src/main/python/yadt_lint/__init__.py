__version__ = '${version}'

from sys import stdout


def write(text):
    stdout.write(text)


def run():
    write('yadtlint {0}'.format(__version__))
