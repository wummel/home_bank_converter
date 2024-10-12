import csv


class DialectDKB(csv.Dialect):
    delimiter = ';'
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = csv.QUOTE_MINIMAL


class DialectVB(csv.Dialect):
    delimiter = ';'
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = csv.QUOTE_MINIMAL


class DialectSparkasse(csv.Dialect):
    delimiter = ';'
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = csv.QUOTE_MINIMAL


class DialectAchtzehnZweiundzwanzig(csv.Dialect):
    delimiter = ';'
    quotechar = '"'
    doublequote = False
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = csv.QUOTE_MINIMAL


class DialectComdirect(csv.Dialect):
    delimiter = ';'
    quotechar = '"'
    doublequote = False
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = csv.QUOTE_MINIMAL


csv.register_dialect("dkb", DialectDKB)
csv.register_dialect("vb", DialectVB)
csv.register_dialect("sparkasse", DialectSparkasse)
csv.register_dialect("1822direkt", DialectAchtzehnZweiundzwanzig)
csv.register_dialect("comdirect", DialectComdirect)
