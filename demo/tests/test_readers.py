from pathlib import Path

import pytest

from clean_code_lab.readers import make_reader


def test_adapters_share_id_contract(tmp_path: Path) -> None:
    csv = tmp_path / "observed.csv"
    csv.write_text("id\n0002\n0002\n0009\n", encoding="utf-8")
    js = tmp_path / "observed.json"
    js.write_text('["0002", "0002", "0009"]', encoding="utf-8")
    assert make_reader("csv").read(csv) == make_reader("json").read(js)
    assert make_reader("csv").read(csv) == ["0002", "0002", "0009"]


def test_invalid_csv_shape_is_rejected(tmp_path: Path) -> None:
    csv = tmp_path / "invalid.csv"
    csv.write_text("other\nu1\n", encoding="utf-8")
    with pytest.raises(ValueError, match="id column"):
        make_reader("csv").read(csv)


def test_invalid_json_id_is_rejected(tmp_path: Path) -> None:
    data = tmp_path / "invalid.json"
    data.write_text("[1]", encoding="utf-8")
    with pytest.raises(ValueError, match="nonempty ID"):
        make_reader("json").read(data)
