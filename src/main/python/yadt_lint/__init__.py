"""
yadtlint

Usage:
yadtlint (-h | --help)
yadtlint validate <file>
yadtlint --version
yadtlint [options]

Options:
-h --help     Show this screen.
--version     Show version.

"""
from docopt import docopt
from logging import getLogger, basicConfig, INFO
import yaml
from yaml.scanner import ScannerError
import phyles
import sys
import re

__version__ = '${version}'


IS24HostnameRegex = ".*((BeR|hAm|dev|tuV|Lst)[a-z]{3}\d\d).*"
IS24HostPattern = re.compile(IS24HostnameRegex, re.IGNORECASE)

logger = getLogger('yadt_lint')
basicConfig()
logger.setLevel(INFO)


def _get_configuration(args):  # pragma: no cover
    with open(args['<file>']) as config_file:
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

    try:
        configuration = _get_configuration(args)
        _validate_schema(configuration)
    except ScannerError as error:
        logger.error('Invalid YAML Format')
        logger.error(error)
        sys.exit(1)
    except IOError as error:
        logger.error(error)
        sys.exit(1)
    except TypeError as error:
        logger.error('No input given')
        logger.error(error)
        sys.exit(1)


def validate_hostnames(hosts):
    if not hosts:
        raise ValueError('No hostname given')
    for host in hosts:
        if not IS24HostPattern.match(host):
            raise ValueError("hostname invalid: %s" % host)
    return hosts
