"""Download Common Voice datasets from the Hugging Face Hub.

Example:
    # Download the English "validated" split
    python download_common_voice.py --language en --split validated

    # Download a different language and extract to a custom directory
    python download_common_voice.py --language de --extract-to data/german_corpus

    # See all available splits for a language
    python download_common_voice.py --language es --list-splits
"""

from __future__ import annotations

import argparse
import os
import sys
import tarfile
from pathlib import Path

from huggingface_hub import hf_hub_download, list_repo_files
from huggingface_hub.utils import HfHubHTTPError


DEFAULT_REPO = "mozilla-foundation/common_voice_16_1"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download Common Voice from Hugging Face Hub.")
    parser.add_argument(
        "--repo",
        default=os.getenv("CV_REPO", DEFAULT_REPO),
        help=f"Repo name on Hugging Face Hub (default: {DEFAULT_REPO})",
    )
    parser.add_argument(
        "--language",
        default="en",
        help="Language code (e.g., 'en', 'de', 'fr') to download (default: en)",
    )
    parser.add_argument(
        "--split",
        default="validated",
        help="Dataset split to download (e.g., 'validated', 'train', 'dev', 'test', default: validated)",
    )
    parser.add_argument(
        "--list-splits",
        action="store_true",
        help="List available splits for the specified language and exit.",
    )
    parser.add_argument(
        "--output-dir",
        default="data",
        help="Directory to save the downloaded archive (default: data)",
    )
    parser.add_argument(
        "--extract-to",
        default="data/corpus",
        help="Directory to extract the archive into (default: data/corpus)",
    )
    parser.add_argument(
        "--no-extract",
        dest="extract",
        action="store_false",
        help="Skip extraction; only download the archive",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force redownload even if the file exists locally.",
    )
    return parser.parse_args()


def get_available_splits(repo: str, language: str) -> list[str]:
    try:
        files = list_repo_files(repo, repo_type="dataset")
    except HfHubHTTPError as exc:
        print(f"Could not list repo files: {exc}", file=sys.stderr)
        print("Check if the repo name and your connection are correct.", file=sys.stderr)
        sys.exit(1)

    prefix = f"data/{language}/"
    suffix = ".tar.gz"
    return [f.removeprefix(prefix).removesuffix(suffix) for f in files if f.startswith(prefix) and f.endswith(suffix)]


def download_archive(
    repo: str,
    language: str,
    split: str,
    output_dir: Path,
    force: bool,
) -> Path:
    filename = f"{language}.tar.gz"
    repo_filename = f"data/{language}/{split}.tar.gz"
    local_path = output_dir / filename

    try:
        downloaded_path_str = hf_hub_download(
            repo_id=repo,
            filename=repo_filename,
            repo_type="dataset",
            local_dir=str(output_dir),
            local_dir_use_symlinks=False,  # Keep it simple
            force_download=force,
            resume_download=True,
        )
        # The returned path is the one in the cache, we need the one in our output dir
        final_path = Path(downloaded_path_str)
        if not local_path.exists() or force:
             # Move cached file to target location if not already there
            final_path.replace(local_path)
        else:
            print(f"File already exists at {local_path}, skipping download. Use --force to overwrite.")
            return local_path
            
        print(f"Downloaded archive: {local_path}")
        return local_path

    except HfHubHTTPError as exc:
        print(f"Failed to download '{repo_filename}' from '{repo}': {exc}", file=sys.stderr)
        print("Check the language and split names, or try --list-splits.", file=sys.stderr)
        sys.exit(1)


def extract_archive(archive_path: Path, target_dir: Path) -> None:
    if not archive_path.exists():
        print(f"Archive not found: {archive_path}", file=sys.stderr)
        sys.exit(1)
    target_dir.mkdir(parents=True, exist_ok=True)
    print(f"Extracting {archive_path} to {target_dir} ...")
    try:
        with tarfile.open(archive_path, "r:gz") as tar:
            members = tar.getmembers()
            for member in members:
                # Path traversal check
                member_path = target_dir.joinpath(member.name).resolve()
                if not str(member_path).startswith(str(target_dir.resolve())):
                    raise RuntimeError(f"Blocked unsafe path in archive: {member.name}")
            tar.extractall(path=target_dir, members=members)
    except (tarfile.TarError, RuntimeError) as exc:
        print(f"Extraction failed: {exc}", file=sys.stderr)
        sys.exit(1)
    print("Extraction complete.")


def main() -> None:
    args = parse_args()

    if args.list_splits:
        print(f"Available splits for '{args.language}' in '{args.repo}':")
        for split_name in get_available_splits(args.repo, args.language):
            print(f"- {split_name}")
        return

    archive_path = download_archive(
        repo=args.repo,
        language=args.language,
        split=args.split,
        output_dir=Path(args.output_dir),
        force=args.force,
    )

    if args.extract:
        extract_archive(archive_path, Path(args.extract_to))


if __name__ == "__main__":
    main()
