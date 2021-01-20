import argparse
import logging

import coloredlogs

from home_bank_converter.converter import Converter
from home_bank_converter.csv_file_format import csv_file_format_registry


def main():
    logging.basicConfig(level=logging.INFO)
    coloredlogs.install(level=logging.INFO)

    parser = argparse.ArgumentParser(
        description=
        "Convert a CSV export file from your online banking to a HomeBank compatible CSV format."
    )
    parser.add_argument("filename", help="The CSV file to convert.")
    parser.add_argument("--format",
                        type=str,
                        default=None,
                        choices=csv_file_format_registry.list)
    args = parser.parse_args()

    csv_parser = Converter(filename=args.filename)
    csv_parser.parse(args.format)
    csv_parser.convert_and_write()


if __name__ == '__main__':
    main()
