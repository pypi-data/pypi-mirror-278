from enum import Enum


class PeriodType(Enum):
    """Type of the period assigned to each Period sub-class instance in order to identify serialized values."""

    BIMESTER = "bimester"
    DAY = "day"
    MONTH = "month"
    QUARTER = "quarter"
    SEMESTER = "semester"
    WEEK = "week"
    YEAR = "year"
