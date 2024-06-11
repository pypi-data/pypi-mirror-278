from dbnomics_data_model.json_utils.errors import JsonBytesParseError
from dbnomics_data_model.json_utils.parsing import parse_json_bytes_as_object


def parse_json_line_code(line: bytes) -> str:
    data = parse_json_bytes_as_object(line)

    try:
        code = data["code"]
    except KeyError as exc:
        raise JsonBytesParseError(value=line) from exc

    if not isinstance(code, str):
        raise JsonBytesParseError(value=line)

    return code
