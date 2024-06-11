from typing import TYPE_CHECKING

from dbnomics_data_model.errors import DataModelError

if TYPE_CHECKING:
    from dbnomics_data_model.model.observations import Observation
    from dbnomics_data_model.model.observations.types import ObservationValue


class ObservationError(DataModelError):
    def __init__(self, *, msg: str, observation: "Observation") -> None:
        super().__init__(msg=msg)
        self.observation = observation


class ObservationInvalidValue(ObservationError):
    def __init__(self, *, observation: "Observation", value: "ObservationValue") -> None:
        msg = f"Invalid observation value: {value!r}"
        super().__init__(msg=msg, observation=observation)
