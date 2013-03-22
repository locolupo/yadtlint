"""
yadtlint

Usage:
yadtlint (-h | --help)
yadtlint --version
yadtlint [options]

Options:
--validate <file> specify input file for validation [default: target.yaml]
-h --help     Show this screen.
--version     Show version.

"""
from docopt import docopt
from logging import getLogger, basicConfig
import yaml
import phyles
import sys
import re

__version__ = '${version}'


IS24HostnameRegex = ".*((BeR|hAm|dev|tuV|Lst)[a-z]{3}\d\d).*"
IS24HostPattern = re.compile(IS24HostnameRegex, re.IGNORECASE)

logger = getLogger('yadt_lint')
basicConfig()


def _get_configuration(args):
    with open(args['--validate']) as config_file:
        configuration = yaml.load(config_file)
    return configuration


def _validate_schema(configuration):
    spec = phyles.package_spec(phyles.Undefined, "yadt_lint", ".", "yadt-target.yaml")
    converters = {'valid hostnames': validate_hostnames}
    schema = phyles.load_schema(spec, converters)
    try:
        config = schema.validate_config(configuration)
        logger.info(config)
        logger.info("Ok - targetfile valid")
    except phyles.ConfigError as error:
        logger.info("Nope - targetfile invalid")
        logger.info(error)
        logger.info(phyles.sample_config(schema))
        sys.exit(1)


def run():

    args = docopt(__doc__, version=__version__)

    configuration = _get_configuration(args)

    _validate_schema(configuration)


def validate_hostnames(hosts):
    if not hosts:
        raise ValueError('No hostname given')
    for host in hosts:
        if not IS24HostPattern.match(host):
            raise ValueError("hostname invalid: %s" % host)
    return hosts
