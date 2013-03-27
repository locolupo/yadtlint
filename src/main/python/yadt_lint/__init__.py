"""
yadtlint

Usage:
yadtlint (-h | --help)
yadtlint target_validate <file> [options]
yadtlint services_validate <file> [options]
yadtlint --version

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


def input_target_file(args):
    filename = args['<file>']
    if filename != 'target.yaml':
        logger.error('is not a valid targetfile name, should be named target')
        sys.exit(1)
    _validate_yaml_input(args)


def input_services_file(args):
    filename = args['<file>']
    if filename != 'yadt.services':
        logger.error('is not a valid yadt services name, should be named yadt.services')
        sys.exit(1)
    _validate_yaml_input(args)


def run():

    args = docopt(__doc__, version=__version__)
    if args['services_validate']:
        input_services_file(args)
    if args['target_validate']:
        input_target_file(args)


def _get_configuration(args):  # pragma: no cover
    with open(args['<file>']) as config_file:
        configuration = yaml.load(config_file)
    return configuration


def _validate_services_schema(configuration):
    spec = phyles.package_spec(phyles.Undefined, "yadt_lint", ".", "yadt-services.yaml")
    converters = {'valid services': validate_services_input}
    schema = phyles.load_schema(spec, converters)
    try:
        config = schema.validate_config(configuration)
        logger.info(config)
        logger.info('Ok - yadt.services valid')
    except phyles.ConfigError as error:
        logger.info('Nope - yadt.services invalid')
        logger.info(error)
        logger.info(phyles.sample_config(schema))
        sys.exit(1)


def _validate_target_schema(configuration):
    spec = phyles.package_spec(phyles.Undefined, "yadt_lint", ".", "yadt-target.yaml")
    converters = {'valid hostnames': validate_hostnames}
    schema = phyles.load_schema(spec, converters)
    try:
        config = schema.validate_config(configuration)
        logger.info(config)
        logger.info('Ok - targetfile valid')
    except phyles.ConfigError as error:
        logger.info('Nope - targetfile invalid')
        logger.info(error)
        logger.info(phyles.sample_config(schema))
        sys.exit(1)


def _validate_yaml_input(args):
    try:
        configuration = _get_configuration(args)
        if args['target_validate']:
            _validate_target_schema(configuration)
        if args['services_validate']:
            _validate_services_schema(configuration)
    except ScannerError as error:
        if hasattr(error, 'problem_mark'):
            mark = error.problem_mark
            logger.error('Invalid YAML Format check position: (%s:%s)' % (mark.line + 1, mark.column + 1))
        sys.exit(1)
    except IOError as error:
        logger.error(error)
        sys.exit(1)


def validate_services_input(services):
    pass


def validate_hostnames(hosts):
    if not hosts:
        raise ValueError('No hostname given')
    for host in hosts:
        if not IS24HostPattern.match(host):
            raise ValueError('hostname invalid: %s' % host)
    return hosts
