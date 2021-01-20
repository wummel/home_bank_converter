import csv
import locale
import logging
import os
from datetime import datetime
from typing import List, Optional

from home_bank_converter.csv_file_format import csv_file_format_registry

locale.setlocale(locale.LC_ALL, "en_US.UTF-8")


def convert_date(date_string, date_format: str):
    date = datetime.strptime(date_string, date_format)
    return date.strftime('%d-%m-%Y')


class Converter(object):
    max_header_lines = 13

    def __init__(self, filename: str):
        self.filename = filename

    def parse(self, csv_file_format: Optional[str]):
        with open(self.filename, 'r', encoding='iso-8859-1') as csvfile:
            csv_lines = csvfile.readlines()

            potential_header_lines = csv_lines[:self.max_header_lines]

            if csv_file_format is None:
                logging.info("Auto-discovering CSV file format ...")
                self.csv_file_format = csv_file_format_registry.find_matching_format(
                    potential_header_lines)
            else:
                self.csv_file_format = csv_file_format_registry.find_by_name(
                    csv_file_format)

            logging.info(f"File format is '{self.csv_file_format}'")

            self.transaction_header_line = csv_lines[
                self.csv_file_format.number_header_lines]
            self.transaction_lines = csv_lines[(
                self.csv_file_format.number_header_lines +
                1):]  # skip header row

            logging.info(
                f"Discovered {len(self.transaction_lines)} transactions.")

    @property
    def output_filename(self):
        from os.path import splitext
        return "{}_HomeBank{}".format(*splitext(self.filename))

    home_bank_field_names = [
        "date", "paymode", "info", "payee", "memo", "amount", "category",
        "tags"
    ]

    def convert_and_write(self):
        fieldnames = self.transaction_header_line.replace('"', '').replace(
            "\n", "").split(';')

        reader = csv.DictReader(
            self.transaction_lines,
            dialect=self.csv_file_format.dialect,
            fieldnames=fieldnames,
        )

        logging.info(
            f"Writing transactions to '{os.path.abspath(self.output_filename)}'"
        )

        with open(self.output_filename, 'w') as outfile:
            fields = self.csv_file_format.csv_fields

            writer = csv.DictWriter(
                outfile,
                dialect='dkb',
                fieldnames=self.home_bank_field_names,
            )

            for row in reader:
                row: List[str]

                def soll_haben_sign(var):
                    return {"S": -1.0, "H": 1.0}[var]

                sign = soll_haben_sign(
                    row[fields.SIGN]) if fields.SIGN else 1.0

                amount_str = row[fields.AMOUNT].replace(".", "").replace(
                    ",", ".")  # 1.000,00 -> 1000.00
                amount = float(amount_str)

                amount *= sign

                writer.writerow({
                    'date':
                    convert_date(row[fields.DATE],
                                 self.csv_file_format.date_format),
                    'paymode':
                    8,
                    'info':
                    None,
                    'payee':
                    row[fields.PAYEE].replace("\n", " ")
                    if fields.PAYEE else None,
                    'memo':
                    row[fields.MEMO].replace("\n", " "),
                    'amount':
                    amount,
                    'category':
                    None,
                    'tags':
                    None
                })
