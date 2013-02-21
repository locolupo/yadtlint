"""
yadtlint

Usage:
yadtlint (-h | --help)
yadtlint --version

Options:
-h --help     Show this screen.
--version     Show version.

"""
__version__ = '${version}'

from docopt import docopt


def run():
    docopt(__doc__, version=__version__)
