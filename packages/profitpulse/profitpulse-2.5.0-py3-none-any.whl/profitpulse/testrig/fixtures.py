from pathlib import Path

import pytest

from profitpulse.testrig.factory import scenario_for


@pytest.fixture
def header_lines():
    header_lines = [
        "Consultar saldos e movimentos � ordem - 09-08-2022",
        "",
        "Conta ;1234567890 - EUR - Conta Caderneta",
        "Data de in�cio ;01-01-2020",
        "Data de fim ;09-08-2022",
        "",
        "Data mov. ;Data valor ;Descri��o ;D�bito ;Cr�dito ;Saldo contabil�stico ;Saldo dispon�vel ;Categoria ;",  # noqa
    ]
    return header_lines


@pytest.fixture
def data_lines():
    data_lines = []

    # Append to data_lines the content of the file comprovativo_cgd.csv
    with open("tests/fixtures/comprovativo_cgd.csv", "r") as f:
        for line in f:
            if line.startswith("C") or line.startswith("D"):
                continue

            if line.startswith(" "):
                continue

            if line.strip() == "":
                continue

            data_lines.append(line.strip())

    return data_lines


@pytest.fixture
def footer_lines():
    footer_lines = " ; ; ; ;Saldo contabil�stico ;1.028,05 EUR ; ; ;"
    return footer_lines


@pytest.fixture
def transactions_file(tmp_path, header_lines, data_lines, footer_lines) -> Path:
    csv_file = (tmp_path / "transactions").with_suffix(".csv")
    with csv_file.open("w") as f:
        for line in header_lines:
            f.write(f"{line}\n")
        for line in data_lines:
            f.write(f"{line}\n")
        f.write(f"{footer_lines}\n")

    return csv_file


@pytest.fixture
def scenario(tmp_db_session, platform):
    return scenario_for(platform)
