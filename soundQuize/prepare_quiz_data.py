"""Convert Common Voice metadata into quiz-ready JSON items.

Usage example:
    python prepare_quiz_data.py --tsv data/corpus/train.tsv --root data/corpus --output data/quiz_items.json
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


CATEGORY_PAIRS: Dict[str, List[Tuple[str, str]]] = {
    "positive_negative": [
        ("can", "can't"),
        ("do", "don't"),
        ("have", "haven't"),
        ("is", "isn't"),
        ("are", "aren't"),
        ("will", "won't"),
    ],
    "L_R": [
        ("light", "right"),
        ("late", "rate"),
        ("led", "red"),
        ("glass", "grass"),
        ("fly", "fry"),
    ],
    "V_B": [
        ("vase", "base"),
        ("vet", "bet"),
        ("vest", "best"),
        ("vote", "boat"),
        ("vial", "bile"),
    ],
    "S_TH": [
        ("sin", "thin"),
        ("sink", "think"),
        ("sick", "thick"),
        ("sum", "thumb"),
        ("seem", "theme"),
    ],
    "D_TH": [
        ("day", "they"),
        ("den", "then"),
        ("doe", "though"),
        ("dare", "there"),
        ("dose", "those"),
    ],
}


PUNCTUATION = ".,;:!?\"'()[]{}"


def normalize_word(word: str) -> str:
    return word.strip(PUNCTUATION).lower()


def match_pair(words: List[str], pair: Tuple[str, str]) -> int:
    """Return the index of a word that matches the pair, or -1."""
    normalized = [normalize_word(w) for w in words]
    first, second = pair
    found_indices = [idx for idx, w in enumerate(normalized) if w in (first, second)]
    if not found_indices:
        return -1
    found_words = {normalized[idx] for idx in found_indices}
    # Skip sentences containing both confusing words to avoid ambiguity.
    if len(found_words) > 1:
        return -1
    return found_indices[0] if found_indices else -1


def preferred_audio_path(row: Dict[str, str], root: Path, clip_subdir: str) -> str | None:
    rel = row.get("path") or row.get("clip") or row.get("audio")
    if not rel:
        return None
    rel_path = Path(rel)
    if clip_subdir:
        rel_path = Path(clip_subdir) / rel_path
    return str((root / rel_path).as_posix())


def build_item(
    sentence: str,
    words: List[str],
    blank_index: int,
    pair: Tuple[str, str],
    category: str,
    audio_path: str | None,
) -> Dict[str, object]:
    return {
        "category": category,
        "audio": audio_path or "",
        "sentence": sentence.strip(),
        "blank_index": blank_index,
        "optionA": pair[0],
        "optionB": pair[1],
        "correct": words[blank_index].strip(PUNCTUATION),
    }


def iterate_rows(tsv_path: Path) -> Iterable[Dict[str, str]]:
    with tsv_path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            yield row


def process_file(
    tsv_path: Path,
    root: Path,
    clip_subdir: str,
    max_per_category: int,
) -> List[Dict[str, object]]:
    items: List[Dict[str, object]] = []
    counts = {category: 0 for category in CATEGORY_PAIRS}
    seen: set[tuple[str, str]] = set()

    for row in iterate_rows(tsv_path):
        sentence = row.get("sentence") or row.get("text")
        if not sentence:
            continue
        words = sentence.split()
        normalized_words = [normalize_word(w) for w in words]
        added = False

        for category, pairs in CATEGORY_PAIRS.items():
            if counts[category] >= max_per_category:
                continue
            for pair in pairs:
                if pair[0] in normalized_words and pair[1] in normalized_words:
                    continue  # ambiguous
                blank_index = match_pair(words, pair)
                if blank_index == -1:
                    continue

                key = (category, sentence)
                if key in seen:
                    continue

                audio = preferred_audio_path(row, root, clip_subdir)
                items.append(build_item(sentence, words, blank_index, pair, category, audio))
                seen.add(key)
                counts[category] += 1
                added = True
                break
            if added:
                break
    return items


def save_items(items: List[Dict[str, object]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(items, handle, ensure_ascii=False, indent=2)
    print(f"Wrote {len(items)} items to {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create quiz data from Common Voice metadata (TSV).")
    parser.add_argument("--tsv", required=True, help="Path to Common Voice metadata TSV (train.tsv, dev.tsv, etc.)")
    parser.add_argument(
        "--root",
        default="data/corpus",
        help="Root directory containing TSV and clips subdir (default: data/corpus)",
    )
    parser.add_argument(
        "--clip-subdir",
        default="clips",
        help="Relative directory under root that stores audio files (default: clips)",
    )
    parser.add_argument(
        "--output",
        default="data/quiz_items.json",
        help="Output JSON path (default: data/quiz_items.json)",
    )
    parser.add_argument(
        "--max-per-category",
        type=int,
        default=50,
        help="Limit number of quiz items per category (default: 50)",
    )
    args = parser.parse_args()

    tsv_path = Path(args.tsv)
    if not tsv_path.exists():
        print(f"TSV not found: {tsv_path}", file=sys.stderr)
        sys.exit(1)

    items = process_file(tsv_path, Path(args.root), args.clip_subdir, args.max_per_category)
    if not items:
        print("No quiz items were created. Check your pair lists or TSV content.", file=sys.stderr)
    save_items(items, Path(args.output))


if __name__ == "__main__":
    main()
