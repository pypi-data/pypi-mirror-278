import math
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Self

from dbnomics_data_model.model.errors.observations import ObservationInvalidValue
from dbnomics_data_model.model.identifiers.attribute_code import AttributeCode
from dbnomics_data_model.model.periods import Period

from .types import ObservationValue

__all__ = ["Observation"]


@dataclass(frozen=True, kw_only=True)
class Observation:
    period: Period
    value: ObservationValue

    # An attribute value can be a code or free text.
    attributes: dict[AttributeCode, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        value = self.value
        if (
            isinstance(value, Decimal)
            and not value.is_finite()
            or isinstance(value, float)
            and not math.isfinite(value)
        ):
            raise ObservationInvalidValue(observation=self, value=value)

    @classmethod
    def create(
        cls,
        *,
        attributes: dict[str, str] | None = None,
        period: Period | str,
        value: ObservationValue,
    ) -> Self:
        if attributes is None:
            attributes = {}
        parsed_attributes = {AttributeCode.parse(code): value for code, value in attributes.items()}

        if isinstance(period, str):
            period = Period.parse(period)

        return cls(attributes=parsed_attributes, period=period, value=value)

    @property
    def __match_key__(self) -> Any:
        return self.period
