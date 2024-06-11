from dataclasses import dataclass
from typing import TYPE_CHECKING

from dbnomics_data_model.json_utils import JsonObject

if TYPE_CHECKING:
    from dbnomics_data_model.validation.errors.validation_error_data import ValidationErrorData


@dataclass(kw_only=True)
class ErrorChainNode:
    cause: "ErrorChainNode | None"
    data: "ValidationErrorData | None"
    message: str
    type: str

    def to_json(self) -> JsonObject:
        result: JsonObject = {"message": self.message, "type": self.type}

        if self.cause is not None:
            result["cause"] = self.cause.to_json()

        if self.data is not None:
            result.update(self.data.to_json())

        return result


def build_error_chain(error: BaseException) -> ErrorChainNode:
    cause_error = error.__cause__
    cause = build_error_chain(cause_error) if cause_error is not None else None
    data: ValidationErrorData | None = getattr(error, "__validation_error_data__", None)
    return ErrorChainNode(cause=cause, data=data, message=str(error), type=type(error).__name__)
