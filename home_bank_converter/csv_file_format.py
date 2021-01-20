import csv
import re
from typing import List, Optional

from home_bank_converter.csv_dialects import DialectVB, DialectDKB, DialectSparkasse
from home_bank_converter.home_bank_fields import *


class CsvFileFormat:
    name: str

    header_pattern: Optional[str] = None

    def matches(self, first_document_lines: str) -> bool:
        return re.match(self.header_pattern,
                        str(first_document_lines)) is not None

    @property
    def number_header_lines(self):
        return self.header_pattern.count(
            "\n") if self.header_pattern is not None else 0

    csv_fields: HomeBankFields = None

    dialect: csv.Dialect = None

    date_format = str

    def __init__(self):
        # assert self.header_pattern is not None
        assert self.csv_fields is not None
        assert self.dialect is not None


class CsvFileFormatDkbVisa(CsvFileFormat):
    name = "dkb_visa"

    header_pattern = '"Kreditkarte:";"\d+[*]+\d+";\n' \
                     '\n' \
                     '"Von:";"[\d,.]+";\n' \
                     '"Bis:";"[\d,.]+";\n' \
                     '"Saldo:";"[\w,.,\s]+";\n' \
                     '"Datum:";"[\d,.]+";\n' \
                     '\n'

    dialect = DialectDKB()

    csv_fields = DKBVisaFields()

    date_format = "%d.%m.%Y"


class CsvFileFormatDkbGiro(CsvFileFormat):
    name = "dkb_giro"

    header_pattern = '"Kontonummer:";"\w+\d+ / \w+";\n' \
                     '\n' \
                     '"Von:";"[\w.]+";\n' \
                     '"Bis:";"[\d.]+";\n"' \
                     'Kontostand vom [\d.]+:";"[\d.,]+ \w+";\n' \
                     '\n'

    dialect = DialectDKB()

    csv_fields = DKBGiroFields()

    date_format = "%d.%m.%Y"


class CsvFileFormatVBGiro(CsvFileFormat):
    name = "vb_giro"

    header_pattern = '"Vereinigte Volksbank eG"\n' \
                     '\n' \
                     '"Umsatzanzeige"\n' \
                     '\n' \
                     '"BLZ:";"\d+";;"Datum:";"[\d,.]+"\n' \
                     '"Konto:";"\d+";;"Uhrzeit:";"[\d,:]+"\n' \
                     '"Abfrage von:";"[\w,\s]+";;"Kontoinhaber:";"[\w,\s]+"\n' \
                     '\n' \
                     '"Zeitraum:";[\w,\s,\d,.,"]*;"von:";[\d,.,\s,"]*;"bis:";[\d,.,\s"]*\n' \
                     '"Betrag in EUR:"[",;,\w,:\s]+\n' \
                     '"Sortiert nach:";"\w+";"\w+"\n' \
                     '\n'

    csv_fields = VBGiroFields()

    dialect = DialectVB()

    date_format = "%d.%m.%Y"


class CsvFileFormatSparkasse(CsvFileFormat):
    name = "sparkasse"

    header_pattern = None  # '"Auftragskonto";"Buchungstag";"Valutadatum";"Buchungstext";"Verwendungszweck";"Beguenstigter/Zahlungspflichtiger";"Kontonummer";"BLZ";"Betrag";"Waehrung";"Info"\n'

    csv_fields = SparkasseFields()

    dialect = DialectSparkasse()

    date_format = "%d.%m.%y"

    def __repr__(self):
        return self.name


class CsvFileFormatRegistry:
    registry: List[CsvFileFormat] = list()

    def register(self, csv_file_format: CsvFileFormat):
        self.registry.append(csv_file_format)

    def find_matching_format(self, header_lines: List[str]) -> CsvFileFormat:
        header_lines_str = ''.join(header_lines)

        for csv_file_format in self.registry:
            if csv_file_format.matches(header_lines_str):
                return csv_file_format

        raise RuntimeError("Unknown header format!")

    def find_by_name(self, format_id: str):
        matches = [f for f in self.registry if f.name == format_id]

        if matches:
            return matches[0]
        else:
            raise ValueError(
                f"Unsupported CSV file format. Supported formats are {self.registry}"
            )

    @property
    def list(self):
        return [f.name for f in self.registry]


csv_file_format_registry = CsvFileFormatRegistry()
csv_file_format_registry.register(CsvFileFormatDkbVisa())
csv_file_format_registry.register(CsvFileFormatDkbGiro())
csv_file_format_registry.register(CsvFileFormatVBGiro())
csv_file_format_registry.register(CsvFileFormatSparkasse())
