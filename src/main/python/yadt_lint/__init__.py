"""
yadtlint

Usage:
yadtlint (-h | --help)
yadtlint --version
yadtlint [options]

Options:
-i <file>     specify input file [default: target.yaml]
-h --help     Show this screen.
--version     Show version.

"""
__version__ = '${version}'


from docopt import docopt
import yaml
import phyles
import sys


def run():
    args = docopt(__doc__, version=__version__)

    with open(args['-i']) as config_file:
        cfg = yaml.load(config_file)

    spec = phyles.package_spec(phyles.Undefined, "yadt_lint", ".", "yadt-target.yaml")
    converters = {'valid hostnames': valid_hostnames}
    schema = phyles.load_schema(spec, converters)

    try:
        config = schema.validate_config(cfg)
    except phyles.ConfigError as error:
        print(error)
        sys.exit(1)

    print config


def valid_hostnames(args):
    for arg in args:
        if not arg.startswith("dev"):
            raise ValueError("hostname invalid: %s" % arg)
    return args
