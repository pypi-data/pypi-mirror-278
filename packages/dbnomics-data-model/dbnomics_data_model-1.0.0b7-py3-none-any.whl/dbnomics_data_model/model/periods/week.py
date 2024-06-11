from dataclasses import dataclass
from datetime import date
from functools import cached_property
from typing import TYPE_CHECKING, ClassVar, Self, cast

from isoweek import Week
from parsy import ParseError

from dbnomics_data_model.model.errors.periods import PeriodParseError
from dbnomics_data_model.model.periods.converters import month_to_bimester, month_to_quarter, month_to_semester
from dbnomics_data_model.model.periods.formatters import format_week_num, format_year_num
from dbnomics_data_model.model.periods.period import Period
from dbnomics_data_model.model.periods.types import PeriodType

if TYPE_CHECKING:
    from dbnomics_data_model.model.periods.bimester import BimesterPeriod
    from dbnomics_data_model.model.periods.month import MonthPeriod
    from dbnomics_data_model.model.periods.quarter import QuarterPeriod
    from dbnomics_data_model.model.periods.semester import SemesterPeriod


__all__ = ["WeekPeriod"]


@dataclass(frozen=True, order=True)
class WeekPeriod(Period):
    week_num: int

    type_: ClassVar[PeriodType] = PeriodType.WEEK

    def __post_init__(self) -> None:
        # Check that week is constructible.
        self._week  # noqa: B018

    @classmethod
    def from_date(cls, value: Week) -> Self:
        week = Week.withdate(value)
        return cls.from_week(week)

    @classmethod
    def from_week(cls, value: Week) -> Self:
        return cls(value.year, value.week)

    @classmethod
    def parse(cls, value: str) -> Self:
        from . import parsers

        try:
            week_period = cast(Self, parsers.week_period.parse(value))
        except ParseError as exc:
            raise PeriodParseError(period_raw=value) from exc

        return week_period

    def __str__(self) -> str:
        return f"{format_year_num(self.year_num)}-W{format_week_num(self.week_num)}"

    @cached_property
    def bimester(self) -> "BimesterPeriod":
        from dbnomics_data_model.model.periods.bimester import BimesterPeriod

        month_num = self.first_day.month
        bimester_num = month_to_bimester(month_num)
        return BimesterPeriod(self.year_num, bimester_num)

    @cached_property
    def first_day(self) -> date:
        return cast(date, self._week.monday())

    @cached_property
    def month(self) -> "MonthPeriod":
        from dbnomics_data_model.model.periods.month import MonthPeriod

        month_num = self.first_day.month
        return MonthPeriod(self.year_num, month_num)

    @cached_property
    def next(self) -> Self:
        new_week = cast(Week, self._week + 1)
        return self.from_week(new_week)

    @cached_property
    def previous(self) -> Self:
        new_week = cast(Week, self._week - 1)
        return self.from_week(new_week)

    @cached_property
    def quarter(self) -> "QuarterPeriod":
        from dbnomics_data_model.model.periods.quarter import QuarterPeriod

        month_num = self.first_day.month
        quarter_num = month_to_quarter(month_num)
        return QuarterPeriod(self.year_num, quarter_num)

    @cached_property
    def semester(self) -> "SemesterPeriod":
        from dbnomics_data_model.model.periods.semester import SemesterPeriod

        month_num = self.first_day.month
        semester_num = month_to_semester(month_num)
        return SemesterPeriod(self.year_num, semester_num)

    def _ordinal_difference(self, other: Self) -> int:
        return cast(int, self._week - other._week)  # noqa: SLF001

    @cached_property
    def _week(self) -> Week:
        return Week(self.year_num, self.week_num)
