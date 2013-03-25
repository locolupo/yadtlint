import unittest
from mockito import when as mock_when, verify, unstub, any as any_value, mock, never
from yaml.scanner import ScannerError
import phyles

import yadt_lint


class YadtLintTest(unittest.TestCase):

    def setUp(self):
        mock_when(yadt_lint.logger).info(any_value()).thenReturn(None)
        mock_when(yadt_lint.logger).error(any_value()).thenReturn(None)

    def tearDown(self):
        unstub()

    def test_should_initialize_docopt(self):
        mock_when(yadt_lint).docopt(any_value(), version=any_value()).thenReturn(None)
        mock_when(yadt_lint)._get_configuration(any_value()).thenReturn(None)
        mock_when(yadt_lint)._validate_schema(any_value()).thenReturn(None)

        yadt_lint.run()

        verify(yadt_lint).docopt(yadt_lint.__doc__, version=yadt_lint.__version__)

    def test_run_should_call_get_configuration_and_validate_schema(self):
        mock_args = mock()
        mock_when(yadt_lint).docopt(any_value(), version=any_value()).thenReturn(mock_args)
        mock_configuration = mock()
        mock_when(yadt_lint)._get_configuration(any_value()).thenReturn(mock_configuration)
        mock_when(yadt_lint)._validate_schema(any_value()).thenReturn(None)

        yadt_lint.run()

        verify(yadt_lint)._get_configuration(mock_args)
        verify(yadt_lint)._validate_schema(mock_configuration)

    def test_run_should_exit_with_error_when_yaml_parsing_fails(self):
        mock_args = mock()
        mock_when(yadt_lint).docopt(any_value(), version=any_value()).thenReturn(mock_args)
        mock_when(yadt_lint)._get_configuration(any_value()).thenRaise(ScannerError)
        mock_when(yadt_lint.sys).exit(any_value()).thenReturn(None)

        yadt_lint.run()

        verify(yadt_lint.sys).exit(1)

    def test_run_should_exit_with_error_when_wrong_file_is_given(self):

        mock_args = mock()
        mock_when(yadt_lint).docopt(any_value(), version=any_value()).thenReturn(mock_args)
        mock_when(yadt_lint)._get_configuration(any_value()).thenRaise(IOError)
        mock_when(yadt_lint.sys).exit(any_value()).thenReturn(None)

        yadt_lint.run()

        verify(yadt_lint.sys).exit(1)

    def test_validate_hosts_should_raise_exception_when_host_is_invalid(self):
        host_list = ['devman01', 'tuvman01', 'foofail01']
        self.assertRaises(ValueError, yadt_lint.validate_hostnames, host_list)

    def test_validate_hosts_should_raise_exception_when_host_is_not_given(self):
        host_list = []
        self.assertRaises(ValueError, yadt_lint.validate_hostnames, host_list)

    def test_validate_hosts_should_not_raise_exception_when_host_is_valid(self):
        host_list = ['devman01', 'tuvman01']
        yadt_lint.validate_hostnames(host_list)

    def test_should_exit_with_error_when_phyles_schema_validation_fails(self):
        mock_when(yadt_lint.phyles).package_spec(any_value(), any_value(), any_value(), any_value()).thenReturn(None)
        mock_schema = mock()
        mock_when(yadt_lint.phyles).load_schema(any_value(), any_value()).thenReturn(mock_schema)
        mock_when(mock_schema).validate_config(any_value()).thenRaise(phyles.ConfigError)
        mock_when(yadt_lint.phyles).sample_config(any_value()).thenReturn(None)
        mock_when(yadt_lint.sys).exit(any_value()).thenReturn(None)

        yadt_lint._validate_schema(mock())

        verify(yadt_lint.sys).exit(1)

    def test_should_not_exit_when_phyles_schema_validation_succeeds(self):
        mock_when(yadt_lint.phyles).package_spec(any_value(), any_value(), any_value(), any_value()).thenReturn(None)
        mock_schema = mock()
        mock_when(yadt_lint.phyles).load_schema(any_value(), any_value()).thenReturn(mock_schema)
        mock_when(mock_schema).validate_config(any_value()).thenReturn(None)
        mock_when(yadt_lint.phyles).sample_config(any_value()).thenReturn(None)
        mock_when(yadt_lint.sys).exit(any_value()).thenReturn(None)

        yadt_lint._validate_schema(mock())

        verify(yadt_lint.sys, never).exit(1)