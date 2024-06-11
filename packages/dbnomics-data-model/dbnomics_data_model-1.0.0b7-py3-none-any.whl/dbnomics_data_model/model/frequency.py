from dataclasses import dataclass
from enum import Enum
from typing import Literal, Self, TypeAlias, cast

from dbnomics_data_model.model.errors.frequency import InvalidFrequencyCode

__all__ = ["Frequency", "FrequencyCode"]


FrequencyCode: TypeAlias = Literal["A", "B", "D", "M", "Q", "S", "W"]
frequency_codes = ["A", "B", "D", "M", "Q", "S", "W"]


@dataclass(frozen=True, kw_only=True)
class FrequencyItem:
    code: FrequencyCode
    label: str


class Frequency(Enum):
    ANNUAL = FrequencyItem(code="A", label="Annual")
    BIMESTRIAL = FrequencyItem(code="B", label="Bimestrial")
    DAILY = FrequencyItem(code="D", label="Daily")
    MONTHLY = FrequencyItem(code="M", label="Monthly")
    QUARTERLY = FrequencyItem(code="Q", label="Quarterly")
    SEMESTRIAL = FrequencyItem(code="S", label="Semestrial")
    WEEKLY = FrequencyItem(code="W", label="Weekly")

    @classmethod
    def from_code(cls, code: FrequencyCode) -> Self:
        for item in cls:
            if item.value.code == code:
                return item

        raise AssertionError

    @classmethod
    def parse_code(cls, value: str) -> Self:
        if value not in frequency_codes:
            raise InvalidFrequencyCode(value=value)

        code = cast(FrequencyCode, value)
        return cls.from_code(code)
