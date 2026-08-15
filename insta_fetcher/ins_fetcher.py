"""Command-line interface for downloading a public Instagram profile."""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

import instaloader

ACCOUNT_PATTERN = re.compile(r"^[A-Za-z0-9._]{1,30}$")
DATE_PREFIX_PATTERN = re.compile(r"^(\d{4}-\d{2}-\d{2})")


def validate_account(value: str) -> str:
    """Validate an Instagram account name before using it as a directory."""
    account = value.lstrip("@").strip()
    if not ACCOUNT_PATTERN.fullmatch(account):
        raise argparse.ArgumentTypeError("invalid Instagram account name")
    return account


def organize_by_date(output_dir: Path) -> int:
    """Move dated files into YYYY-MM-DD subdirectories."""
    moved = 0
    for item in output_dir.iterdir():
        if not item.is_file():
            continue
        match = DATE_PREFIX_PATTERN.match(item.name)
        if match is None:
            continue
        destination_dir = output_dir / match.group(1)
        destination_dir.mkdir(exist_ok=True)
        destination = destination_dir / item.name
        if destination.exists():
            continue
        shutil.move(str(item), destination)
        moved += 1
    return moved


def download_profile(account: str, output_dir: Path, profile_pic_only: bool) -> None:
    """Download public profile media with Instaloader."""
    output_dir.mkdir(parents=True, exist_ok=True)
    loader = instaloader.Instaloader(
        dirname_pattern=str(output_dir),
        filename_pattern="{date_utc:%Y-%m-%d}_{shortcode}",
        download_comments=False,
        save_metadata=False,
        compress_json=False,
        post_metadata_txt_pattern="",
    )
    loader.download_profile(
        account,
        profile_pic_only=profile_pic_only,
        fast_update=False,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Download and organize media from a public Instagram profile."
    )
    parser.add_argument("account", type=validate_account, help="public profile name")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("downloads"),
        help="parent output directory (default: downloads)",
    )
    parser.add_argument(
        "--profile-pic-only",
        action="store_true",
        help="download only the public profile picture",
    )
    parser.add_argument(
        "--no-organize",
        action="store_true",
        help="leave downloaded files in one directory",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    profile_dir = args.output.expanduser().resolve() / args.account
    download_profile(args.account, profile_dir, args.profile_pic_only)
    moved = 0 if args.no_organize else organize_by_date(profile_dir)
    print(f"Saved @{args.account} to {profile_dir} ({moved} files organized).")


if __name__ == "__main__":
    main()
