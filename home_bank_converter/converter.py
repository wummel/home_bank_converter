import csv
import locale
import logging
import os
import re
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from .csv_file_format import csv_file_format_registry, CsvFileFormat

locale.setlocale(locale.LC_ALL, "en_US.UTF-8")


def convert_date(date_string, date_format: str):
    date = datetime.strptime(date_string, date_format)
    return date.strftime('%d-%m-%Y')


@dataclass
class InputCsvContent:
    transaction_header_line: str = None
    transaction_lines: List[str] = None
    csv_file_format: CsvFileFormat = None

    @property
    def n_transactions(self):
        return len(self.transaction_lines)


class Converter:
    max_header_lines = 13

    def __init__(self, filename: str):
        self.filename = filename

    def parse(self, csv_file_format: Optional[str]):

        input_csv_content = InputCsvContent()

        with open(self.filename, 'r', encoding='iso-8859-1') as csvfile:
            csv_lines = csvfile.readlines()

            potential_header_lines = csv_lines[:self.max_header_lines]

            if csv_file_format is None:
                logging.info("Auto-discovering CSV file format ...")
                input_csv_content.csv_file_format = csv_file_format_registry.find_matching_format(
                    potential_header_lines)
            else:
                input_csv_content.csv_file_format = csv_file_format_registry.find_by_name(
                    csv_file_format)

            logging.info(
                f"File format is '{input_csv_content.csv_file_format}'")

            input_csv_content.transaction_header_line = csv_lines[
                input_csv_content.csv_file_format.number_header_lines]

            # skip header row
            input_csv_content.transaction_lines = \
                csv_lines[(input_csv_content.csv_file_format.number_header_lines + 1):]

            logging.info(
                f"Discovered {input_csv_content.n_transactions} transactions.")

            return input_csv_content

    @property
    def output_filename(self):
        from os.path import splitext
        return "{}.homebank{}".format(*splitext(self.filename))

    home_bank_field_names = [
        "date", "paymode", "info", "payee", "memo", "amount", "category",
        "tags"
    ]

    def convert_and_write(self, input_csv_content: InputCsvContent):
        fieldnames = input_csv_content.transaction_header_line.replace(
            '"', '').replace("\n", "").split(';')

        reader = csv.DictReader(
            input_csv_content.transaction_lines,
            dialect=input_csv_content.csv_file_format.dialect,
            fieldnames=fieldnames,
        )

        logging.info(
            f"Writing transactions to '{os.path.abspath(self.output_filename)}'"
        )

        with open(self.output_filename, 'w') as outfile:
            fields = input_csv_content.csv_file_format.csv_fields

            writer = csv.DictWriter(
                outfile,
                dialect='dkb',
                fieldnames=self.home_bank_field_names,
            )

            for row in reader:
                row: List[str]

                match fields.PAYEE:
                    case dict():
                        payee = re.findall(fields.PAYEE.get("regex"), row[fields.PAYEE.get("name")])
                        payee = payee[0] if payee else None
                    case None:
                        payee = None
                    case _:
                        payee = row[fields.PAYEE].replace("\n", " ")

                match fields.MEMO:
                    case dict():
                        memo = re.findall(fields.MEMO.get("regex"), row[fields.MEMO.get("name")])
                        memo = memo[0] if memo else None
                    case None:
                        memo = None
                    case _:
                        memo = row[fields.MEMO].replace("\n", " ")

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
                    convert_date(
                        row[fields.DATE],
                        input_csv_content.csv_file_format.date_format),
                    'paymode':
                    fields.PAYMENT_MAPPING.get(row[fields.PAYMENT], 8) if fields.PAYMENT else 8,
                    'info':
                    None,
                    'payee':
                    payee,
                    'memo':
                    memo,
                    'amount':
                    amount,
                    'category':
                    None,
                    'tags':
                    None
                })
