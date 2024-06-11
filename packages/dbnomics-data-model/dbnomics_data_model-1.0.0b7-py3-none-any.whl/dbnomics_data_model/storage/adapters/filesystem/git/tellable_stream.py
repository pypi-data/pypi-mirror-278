from collections.abc import Iterator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from git.cmd import Git


class TellableStream:
    def __init__(self, stream: "Git.CatFileContentStream") -> None:
        self._stream = stream
        self._position = 0

    def __iter__(self) -> Iterator[bytes]:
        for line in self._stream:
            yield line
            self._position += len(line)

    def read(self, size: int = -1) -> bytes:
        data = self._stream.read(size)
        self._position += len(data)
        return data

    def tell(self) -> int:
        return self._position
