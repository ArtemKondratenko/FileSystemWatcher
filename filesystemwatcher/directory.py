from __future__ import annotations

import os
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime as DateTime
from pathlib import Path


class DirectoryStateDifference:
    pass


@dataclass(kw_only=True)
class FileDifference(DirectoryStateDifference):
    filename: Path


@dataclass(kw_only=True)
class FileModified(FileDifference):
    pass


@dataclass(kw_only=True)
class FileCreated(FileDifference):
    pass


@dataclass(kw_only=True)
class FileRemoved(FileDifference):
    pass


@dataclass(kw_only=True, unsafe_hash=True)
class FileState:
    path: Path
    modified_at: DateTime


class DirectoryState:
    """Состояние директории, зафиксированное в какой-то момент времени.

    Состояние директории не является полным в том смысле, что из него нельзя
    целиком восстановить директорию.

    Основная цель — это иметь возможность обнаружить отличия между двумя
    различными состояними директории."""

    path: Path
    files: set[FileState]

    def __init__(self, path: Path) -> None:
        self.files = set()

        for subdir, _, filenames in os.walk(path):
            for filename in filenames:
                file_path = os.path.join(subdir, filename)
                modification_datetime = DateTime.fromtimestamp(
                    os.path.getmtime(file_path))
                file_state = FileState(path=Path(file_path),
                                       modified_at=modification_datetime)
                self.files.add(file_state)

    def differences(self, other: DirectoryState) -> Iterable[DirectoryStateDifference]:
        self_files_by_path = {f.path: set() for f in self.files}
        other_files_by_path = {f.path: set() for f in other.files}

        for f in self.files:
            self_files_by_path[f.path].add(f)
        for f in other.files:
            other_files_by_path[f.path].add(f)

        removed_filenames = self_files_by_path.keys() - other_files_by_path.keys()
        for filename in removed_filenames:
            yield FileRemoved(filename=filename)

        created_filenames = other_files_by_path.keys() - self_files_by_path.keys()
        yield from (FileCreated(filename=filename)
                    for filename in created_filenames)

        identical_filenames = self_files_by_path.keys() & other_files_by_path.keys()
        for filename in identical_filenames:
            self_states = self_files_by_path[filename]
            other_states = other_files_by_path[filename]
            if self_states != other_states:
                yield FileModified(filename=filename)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DirectoryState):
            return False
        return list(self.differences(other)) == []
