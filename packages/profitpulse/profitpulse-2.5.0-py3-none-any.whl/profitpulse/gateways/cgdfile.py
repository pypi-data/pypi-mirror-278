# type: ignore
import csv
import pathlib

from profitpulse.lib.transaction import Transaction
from profitpulse.lib.year_month_day import YearMonthDay
from profitpulse.services.import_transactions import ImportTransactionsTransactionGater


class RowParser:
    """
    Example of a row list:
        ['01-01-2020', '01-01-2020', 'COMPRAS C DEB FARMACI ', '15,69', '', '2.350,49', '2.350,49', 'COMPRAS ', ''] # noqa
    """

    def __init__(self, row: list):
        if not row:
            raise ValueError("Row cannot be empty")

        self.row = row

    @property
    def value(self) -> int:
        """
        Get the value of the transaction.
        """

        debit_row_index = 3
        credit_row_index = 4

        value_index = debit_row_index
        if not self.row[debit_row_index]:
            value_index = credit_row_index

        parsed_value = self.row[value_index].replace(".", "").replace(",", "")

        if value_index == credit_row_index:
            return int(parsed_value)

        return int(parsed_value) * -1

    @property
    def description(self) -> str:
        """
        Get the description of the transaction.
        """

        return self.row[2]

    @property
    def date(self):
        """
        Get the date of the transaction.
        """

        date_list = self.row[0].split("-")
        date_list.reverse()
        return YearMonthDay("-".join(date_list))


class GatewayCGDFile(ImportTransactionsTransactionGater):
    """
    Example of a file:
        Consultar saldos e movimentos � ordem - 09-08-2022

        Conta ;1234567890 - EUR - Conta Caderneta
        Data de in�cio ;01-01-2020
        Data de fim ;09-08-2022

        Data mov. ;Data valor ;Descri��o ;D�bito ;Cr�dito ;Saldo contabil�stico ;Saldo dispon�vel ;Categoria ; # noqa
        01-01-2020;01-01-2020;COMPRAS C DEB FARMACI ;15,69;;2.350,49;2.350,49;COMPRAS ;
        09-08-2022;09-08-2022;TRF  ;;45,00;2.133,88;2.133,88;Diversos ;
        ; ; ; ;Saldo contabil�stico ;2.094,08 EUR ; ; ;
    """

    def __init__(self, csv_file_path: pathlib.Path):
        self.csv_file_path = csv_file_path
        self.read_obj = None

    def __iter__(self):
        self.read_obj = open(self.csv_file_path, "r", encoding="ISO-8859-1")
        self.csv_reader = csv.reader(self.read_obj, delimiter=";")

        return _Converter(self.csv_reader)

    def __del__(self):
        if self.read_obj is not None:
            self.read_obj.close()


class _Converter:
    def __init__(self, csv_reader):
        self._reader = csv_reader

        # Ignore the headers of the file, 7 lines
        for _ in range(7):
            next(self._reader)

    def __next__(self):
        row = next(self._reader)

        # Identify the footer of the file
        #  ; ; ; ;Saldo contabil�stico ;1.000,00 EUR ; ; ;
        if row[0] == " ":
            raise StopIteration

        row_parser = RowParser(row)

        t = Transaction(
            seller=row_parser.description.strip(),
            date_of_movement=row_parser.date,
            value=row_parser.value,
            origin="CGD",
        )

        return t
