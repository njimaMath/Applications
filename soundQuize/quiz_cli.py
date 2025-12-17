"""Simple terminal quiz that plays Common Voice clips and prompts for confusing-word choices."""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
from pathlib import Path
from typing import Dict, List

try:
    from playsound import playsound
except Exception:  # playsound may not be installed or configured
    playsound = None


def load_quiz_data(path: Path) -> List[Dict[str, object]]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def available_categories(data: List[Dict[str, object]]) -> List[str]:
    categories = {item["category"] for item in data if "category" in item}
    return sorted(categories)


def choose_category(categories: List[str]) -> str:
    print("Available categories:")
    for idx, cat in enumerate(categories, start=1):
        print(f"  {idx}) {cat}")
    while True:
        choice = input("Pick a category number (or 'q' to quit): ").strip()
        if choice.lower() == "q":
            sys.exit(0)
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(categories):
                return categories[idx - 1]
        print("Invalid choice, try again.")


def blank_sentence(sentence: str, blank_index: int) -> str:
    words = sentence.split()
    idx = blank_index
    # Fallback: if index is 1-based, adjust automatically.
    if idx >= len(words) and idx - 1 < len(words):
        idx = idx - 1
    if 0 <= idx < len(words):
        words[idx] = "[   ]"
    return " ".join(words)


def play_audio_if_available(audio_path: str, enable_audio: bool) -> None:
    if not enable_audio:
        return
    if not audio_path:
        print("[no audio path provided]")
        return
    clip = Path(audio_path)
    if not clip.exists():
        print(f"[audio missing: {clip}]")
        return
    if not playsound:
        print(f"[audio available at {clip}, install playsound to enable playback]")
        return
    try:
        playsound(str(clip))
    except Exception as exc:  # pragma: no cover - playback errors are runtime-specific
        print(f"[could not play audio: {exc}]")


def run_quiz_round(item: Dict[str, object], enable_audio: bool) -> bool:
    print("\n--- New Question ---")
    sentence = str(item.get("sentence", ""))
    blank_index = int(item.get("blank_index", -1))
    option_a = str(item.get("optionA", ""))
    option_b = str(item.get("optionB", ""))
    correct = str(item.get("correct", ""))

    play_audio_if_available(str(item.get("audio", "")), enable_audio)
    print(blank_sentence(sentence, blank_index))
    print(f"A) {option_a}    B) {option_b}")

    answer = input("Your answer (A/B, or Q to quit): ").strip().lower()
    if answer in ("q", "quit"):
        sys.exit(0)

    chosen = option_a if answer == "a" else option_b
    is_correct = chosen.lower() == correct.lower()
    if is_correct:
        print(f"Correct! The sentence was: {sentence}")
    else:
        print(f"Incorrect. Correct answer: {correct}")
        print(f"Full sentence: {sentence}")
    return is_correct


def run_quiz_loop(category: str, data: List[Dict[str, object]], rounds: int, enable_audio: bool) -> None:
    items = [item for item in data if item.get("category") == category]
    if not items:
        print(f"No items found for category '{category}'.", file=sys.stderr)
        return

    score = 0
    total = 0
    while rounds == 0 or total < rounds:
        item = random.choice(items)
        if run_quiz_round(item, enable_audio):
            score += 1
        total += 1
        print(f"Score: {score}/{total}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Terminal listening quiz for confusing English sounds.")
    parser.add_argument(
        "--data",
        default="data/quiz_items.json",
        help="Path to quiz JSON generated from Common Voice metadata",
    )
    parser.add_argument(
        "--rounds",
        type=int,
        default=5,
        help="How many rounds to play (0 = endless)",
    )
    parser.add_argument(
        "--no-audio",
        action="store_true",
        help="Disable audio playback (useful if playsound is not installed)",
    )
    args = parser.parse_args()

    data_path = Path(args.data)
    if not data_path.exists():
        fallback = Path("data/sample_quiz_items.json")
        if fallback.exists():
            print(f"{data_path} not found; falling back to {fallback}")
            data_path = fallback
        else:
            print(f"Quiz data not found: {data_path}", file=sys.stderr)
            sys.exit(1)

    data = load_quiz_data(data_path)
    categories = available_categories(data)
    if not categories:
        print("No categories available in the quiz data.", file=sys.stderr)
        sys.exit(1)

    chosen_category = choose_category(categories)
    run_quiz_loop(chosen_category, data, rounds=args.rounds, enable_audio=not args.no_audio)


if __name__ == "__main__":
    main()
