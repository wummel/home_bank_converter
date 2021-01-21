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

        converter.convert_and_write(input_csv_content)


    def test_parse_dkb_visa(self):
        filename = os.path.join(TEST_ASSETS_DIR, "dkb-visa.csv")

        converter = Converter(filename)
        input_csv_content = converter.parse("dkb-visa")

        self.assertEqual(input_csv_content.n_transactions, 3)

        converter.convert_and_write(input_csv_content)


    def test_parse_dkb_giro(self):
        filename = os.path.join(TEST_ASSETS_DIR, "dkb-giro.csv")

        converter = Converter(filename)
        input_csv_content = converter.parse("dkb-giro")

        self.assertEqual(input_csv_content.n_transactions, 3)

        converter.convert_and_write(input_csv_content)
