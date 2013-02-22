import unittest
from mockito import when as mock_when, verify, unstub, any as any_value

import yadt_lint


class YadtLintTest(unittest.TestCase):

    def tearDown(self):
        unstub()

    def test_should_initialize_docopt(self):
        mock_when(yadt_lint).docopt(any_value(), version=any_value()).thenReturn(None)

        yadt_lint.run()

        verify(yadt_lint).docopt(yadt_lint.__doc__, version='${version}')

    def test_should_print_hello_world_when_option_i_is_given(self):

        # given
        arguments = {'-i': True}
        mock_when(yadt_lint).docopt(any_value(), version=any_value()).thenReturn(arguments)
        mock_when(yadt_lint).print_hello_world().thenReturn(None)

        # when
        yadt_lint.run()

        # then
        verify(yadt_lint).print_hello_world()