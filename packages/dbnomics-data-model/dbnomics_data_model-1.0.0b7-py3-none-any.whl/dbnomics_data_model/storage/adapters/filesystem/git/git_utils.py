from functools import lru_cache
from typing import TYPE_CHECKING, cast

import daiquiri
from humanfriendly import format_size

if TYPE_CHECKING:
    from git.objects import Blob

logger = daiquiri.getLogger(__name__)


@lru_cache
def read_blob(blob: "Blob") -> bytes:
    logger.debug("Reading blob %s at %s (%s)", blob.hexsha, blob.path, format_size(blob.size, binary=True))
    blob_bytes = cast(bytes, blob.data_stream.read())
    if len(blob_bytes) != blob.size:
        msg = f"Did not read the expected number of bytes for blob {blob!r}"
        raise RuntimeError(msg)

    logger.debug(
        "Finished reading blob %s at %s (%s) as bytes", blob.hexsha, blob.path, format_size(blob.size, binary=True)
    )
    return blob_bytes
