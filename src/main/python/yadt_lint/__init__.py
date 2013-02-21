"""
yadtlint

Usage:
yadtlint (-h | --help)
yadtlint --version
yadtlint -i

Options:
-i            specify input file [default: ./test.txt]
-h --help     Show this screen.
--version     Show version.

"""
__version__ = '${version}'


from docopt import docopt


def run():
    args = docopt(__doc__, version=__version__)
    if args and args['-i']:
        print_hello_world()


def print_hello_world():
    print ('Hello World')
