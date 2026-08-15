import argparse
from pathlib import Path

import pytest

from insta_fetcher.ins_fetcher import organize_by_date, validate_account


def test_validate_account_accepts_plain_and_at_prefixed_names() -> None:
    assert validate_account("nasa") == "nasa"
    assert validate_account("@open.ai") == "open.ai"


def test_validate_account_rejects_paths() -> None:
    with pytest.raises(argparse.ArgumentTypeError):
        validate_account("../private")


def test_organize_by_date_moves_only_dated_files(tmp_path: Path) -> None:
    dated = tmp_path / "2026-08-15_ABC123.jpg"
    undated = tmp_path / "profile_pic.jpg"
    dated.write_bytes(b"image")
    undated.write_bytes(b"profile")

    assert organize_by_date(tmp_path) == 1
    assert (tmp_path / "2026-08-15" / dated.name).read_bytes() == b"image"
    assert undated.exists()
