class HomeBankFields:
    DATE = None
    PAYEE = None
    MEMO = None
    AMOUNT = None
    SIGN = None
    PAYMENT = None
    PAYMENT_MAPPING = {}


class DKBGiroFields(HomeBankFields):
    """
    This is meant to be a mapping from DKB Giro to HomeBank fields
    """

    DATE = u'Buchungstag'
    PAYEE = u"Auftraggeber / Begünstigter"
    MEMO = "Verwendungszweck"
    AMOUNT = "Betrag (EUR)"
    # PAYMODE = "Buchungstext"


class DKBVisaFields(HomeBankFields):
    DATE = u"Belegdatum"
    AMOUNT = u"Betrag (EUR)"
    MEMO = u"Beschreibung"


class VBGiroFields(HomeBankFields):
    DATE = u"Buchungstag"
    AMOUNT = u"Umsatz"
    MEMO = u"Vorgang/Verwendungszweck"
    PAYEE = u"Empfänger/Zahlungspflichtiger"

    SIGN = u" "


class SparkasseFields(HomeBankFields):
    DATE = u"Buchungstag"
    AMOUNT = u"Betrag"
    MEMO = u"Verwendungszweck"
    PAYEE = u"Beguenstigter/Zahlungspflichtiger"


class AchtzehnZweiundzwanzigFields(HomeBankFields):
    DATE = u"Wertstellung"
    AMOUNT = u"Soll/Haben"
    MEMO = u"Vwz.0"
    PAYEE = u"Empfänger/Auftraggeber Name"
    PAYMENT = u"Buchungsart"
    PAYMENT_MAPPING = {"Barausz.Debit.GA SPK": 3, "Gutschrift Überw.": 4, "Debitkartenzahlung": 6, "Entgeltabschluss": 10, "Rechnung": 10, "Rechnungsabschluss": 10, "Überweisung": 4, "Dauerauftrag": 7, "Lastschrift": 11}
