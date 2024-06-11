import csv
from collections.abc import Iterable, Iterator
from decimal import Decimal
from pathlib import Path
from typing import cast

from dbnomics_data_model.model import ObservationValue
from dbnomics_data_model.model.constants import PERIOD, VALUE
from dbnomics_data_model.model.series import Series
from dbnomics_data_model.storage.adapters.filesystem.constants import NOT_AVAILABLE

from .errors.tsv_utils import TsvHeaderWriteError, TsvRowWriteError


def format_float(value: float) -> str:
    """Remove the '.0' prefix of a float.

    >>> format_float(1)
    '1'
    >>> format_float(1.0)
    '1'
    >>> format_float(1.1)
    '1.1'
    """
    return f"{value:.0f}" if value % 1 == 0 else str(value)


def format_observation_value(observation_value: ObservationValue) -> str:
    if observation_value is None:
        return NOT_AVAILABLE

    if isinstance(observation_value, Decimal):
        return str(observation_value)

    return format_float(observation_value)


def iter_tsv_rows(rows: Iterable[list[str]]) -> Iterator[tuple[tuple[str, ObservationValue], list[str]]]:
    """Yield parsed rows from raw rows.

    The header row must not be in the input iterable.
    """
    for row in rows:
        period = row[0]
        value = parse_observation_value(row[1])
        attribute_value_codes = row[2:]
        yield ((period, value), attribute_value_codes)


def iter_tsv_text_rows(lines: Iterator[str]) -> Iterator[list[str]]:
    r"""Yield rows from TSV as text.

    Each row is a `list` like `[period, value, attribute1, attribute2, ...]`.
    The first row is the header. Attributes are optional.

    Examples
    --------
    >>> from io import StringIO
    >>> def test(s): return list(iter_tsv_rows(StringIO(s)))
    >>> test("")
    []
    >>> test("     ")
    [['     ']]
    >>> test("period\tvalue")
    [['period', 'value']]
    >>> test("period\tvalue\n")
    [['period', 'value']]
    >>> test("period\tvalue\n2018\t0.2")
    [['period', 'value'], ['2018', '0.2']]
    >>> test("period\tvalue\n\n2018\t0.2")
    [['period', 'value'], ['2018', '0.2']]
    >>> test("period\tvalue\tattribute1\n2018\t0.2\tZ\n")
    [['period', 'value', 'attribute1'], ['2018', '0.2', 'Z']]
    >>> test("period\tvalue\tstatus\n\n2017\t0.1\t\n2018\t0.2\tE")
    [['period', 'value', 'status'], ['2017', '0.1', ''], ['2018', '0.2', 'E']]
    >>> test("period\tvalue\n2018\tNaN")
    [['period', 'value'], ['2018', 'NaN']]

    """
    for line in lines:
        line1 = line.strip("\n")
        if not line1:
            continue
        cells = line1.split("\t")
        yield cells


def parse_observation_value(value: str) -> ObservationValue:
    if value == NOT_AVAILABLE:
        return None

    return float(value)


def save_tsv_file(file_path: Path, series: Series) -> None:
    """Save observations to a TSV file."""
    attribute_codes = series.get_observation_attribute_codes()

    with file_path.open("wt", encoding="utf-8", newline="") as fp:
        fieldnames = [PERIOD, VALUE, *sorted(attribute_codes)]
        writer = csv.DictWriter(fp, fieldnames=fieldnames, delimiter="\t", quotechar='"')

        try:
            writer.writeheader()
        except Exception as exc:
            raise TsvHeaderWriteError(fieldnames=fieldnames, file_path=file_path) from exc

        for observation in series.observations:
            row = {
                **cast(dict[str, str], observation.attributes),
                PERIOD: str(observation.period),
                VALUE: format_observation_value(observation.value),
            }
            try:
                writer.writerow(row)
            except Exception as exc:
                raise TsvRowWriteError(file_path=file_path, row=row) from exc
