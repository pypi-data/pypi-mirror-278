from parsy import Parser, fail, regex, seq, string, success

from dbnomics_data_model.model.constants import LATEST_RELEASE
from dbnomics_data_model.model.identifiers.bare_dataset_id import BareDatasetId
from dbnomics_data_model.model.identifiers.dataset_code import DatasetCode
from dbnomics_data_model.model.identifiers.dataset_id import DatasetId
from dbnomics_data_model.model.identifiers.resolvable_dataset_code import ResolvableDatasetCode
from dbnomics_data_model.model.identifiers.series_code import series_code_re
from dbnomics_data_model.model.identifiers.series_id import SeriesId
from dbnomics_data_model.model.identifiers.simple_code import SimpleCode, simple_code_re

colon = string(":")
slash = string("/")

simple_code = regex(simple_code_re).desc("simple code")
provider_code = simple_code.desc("provider code")
bare_dataset_code = simple_code.desc("bare dataset code")
release_code_raw = simple_code.desc("release code raw")
resolvable_release_code = release_code_raw


def to_release_code(release_code_raw: SimpleCode) -> Parser:
    if release_code_raw == LATEST_RELEASE:
        return fail(f"this release code value is reserved: {LATEST_RELEASE!r}")

    return success(release_code_raw)


release_code = release_code_raw.bind(to_release_code)

dataset_code = seq(
    bare_dataset_code=bare_dataset_code,
    release_code=(colon >> release_code).optional(),
).combine_dict(DatasetCode)

resolvable_dataset_code = seq(
    bare_dataset_code=bare_dataset_code,
    resolvable_release_code=(colon >> resolvable_release_code).optional(),
).combine_dict(ResolvableDatasetCode)


dataset_id = seq(
    provider_code=provider_code,
    dataset_code=slash >> dataset_code,
).combine_dict(DatasetId)

bare_dataset_id = seq(
    provider_code=provider_code,
    bare_dataset_code=slash >> bare_dataset_code,
).combine_dict(BareDatasetId)

resolvable_dataset_id = seq(
    provider_code=provider_code,
    resolvable_dataset_code=slash >> resolvable_dataset_code,
).combine_dict(BareDatasetId)

series_code = regex(series_code_re).desc("series code")

series_id = seq(
    provider_code=provider_code,
    dataset_code=slash >> dataset_code,
    series_code=slash >> series_code,
).combine_dict(SeriesId)
