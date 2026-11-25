import csv
import json
import re
from pathlib import Path
from typing import Literal, Protocol

_ID = re.compile(r"[a-zA-Z0-9_-]{1,32}")


class IdReader(Protocol):
    def read(self, path: Path) -> list[str]: ...


def validate_id(value: object) -> str:
    if not isinstance(value, str) or _ID.fullmatch(value) is None:
        raise ValueError("Expected a nonempty ID using letters, digits, '_' or '-'")
    return value


class CsvReader:
    def read(self, path: Path) -> list[str]:
        with path.open(encoding="utf-8", newline="") as source:
            reader = csv.DictReader(source)
            if "id" not in (reader.fieldnames or []):
                raise ValueError("CSV needs an id column")
            return [validate_id(row["id"]) for row in reader]


class JsonReader:
    def read(self, path: Path) -> list[str]:
        observations: object = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(observations, list):
            raise ValueError("JSON needs an array of IDs")
        return [validate_id(value) for value in observations]


def make_reader(kind: Literal["csv", "json"]) -> IdReader:
    if kind == "csv":
        return CsvReader()
    if kind == "json":
        return JsonReader()
    raise ValueError("Unsupported file format")
