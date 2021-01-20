import os
from unittest import TestCase

from home_bank_converter.converter import Converter

TEST_ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")


class TestConverter(TestCase):
    def test_parse_sparkasse(self):
        filename = os.path.join(TEST_ASSETS_DIR, "sparkasse.csv")

        converter = Converter(filename)
        input_csv_content = converter.parse("sparkasse")

        self.assertEqual(input_csv_content.n_transactions, 2)
