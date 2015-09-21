from __future__ import print_function, division, absolute_import
import pandas
import tempfile
import unittest
from . import util

class TestGenerateTextAxis(unittest.TestCase):
    def test_single_digit(self):
        self.assertEqual(['012345678'], util.generate_text_axis(9))
        self.assertEqual([''], util.generate_text_axis(0))
        self.assertEqual(['01'], util.generate_text_axis(2))

    def test_two_digits(self):
        self.assertEqual(['0123456789', '0'],
                          util.generate_text_axis(10))
        self.assertEqual(['01234567890', '0         1'],
                          util.generate_text_axis(11))
        self.assertEqual(['012345678901', '0         1'],
                          util.generate_text_axis(12))
        self.assertEqual(['01234567890123456789', '0         1'],
                          util.generate_text_axis(20))
        self.assertEqual(['012345678901234567890', '0         1         2'],
                          util.generate_text_axis(21))
        self.assertEqual(['0123456789012345678901', '0         1         2'],
                          util.generate_text_axis(22))


if __name__ == '__main__':
    unittest.main()
