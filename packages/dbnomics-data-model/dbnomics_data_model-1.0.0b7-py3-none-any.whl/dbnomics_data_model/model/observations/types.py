from decimal import Decimal
from typing import TypeAlias

__all__ = ["ObservationNumericValue", "ObservationValue"]


ObservationNumericValue: TypeAlias = float | Decimal

ObservationValue: TypeAlias = ObservationNumericValue | None  # None represents NA
