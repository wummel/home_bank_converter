import argparse
import logging

from .converter import Converter
from .csv_file_format import csv_file_format_registry


def main():
    logging.basicConfig(level=logging.INFO)
    try:
        import coloredlogs
        coloredlogs.install(level=logging.INFO)
    except ImportError:
        pass

    parser = argparse.ArgumentParser(
        description=
        "Convert a CSV export file from your online banking to a HomeBank compatible CSV format."
    )
    parser.add_argument("filename", help="The CSV file to convert.")
    parser.add_argument(
        "--format",
        type=str,
        default=None,
        choices=csv_file_format_registry.list,
    )
    args = parser.parse_args()

    csv_parser = Converter(filename=args.filename)
    input_csv_content = csv_parser.parse(args.format)
    csv_parser.convert_and_write(input_csv_content)


if __name__ == '__main__':
    main()
