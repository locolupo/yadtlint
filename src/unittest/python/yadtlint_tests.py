import unittest
from mockito import when, verify, unstub, any as any_value

import yadt_lint


class YadtLintTest(unittest.TestCase):
    def test_should_write_name_and_version_to_stdout(self):
        when(yadt_lint).write(any_value()).thenReturn(None)

        yadt_lint.run()

        verify(yadt_lint).write('yadtlint ${version}')

        unstub()