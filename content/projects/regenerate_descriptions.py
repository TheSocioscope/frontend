#!/usr/bin/env python3
"""
Regenerates project descriptions from interview transcripts using the Claude API.
Reads fos-transcripts/<CODE>_audio_transcription.json, extracts interviewee speech,
and writes factual descriptions in EN / FR / ES / DE back to the project JSON.

Usage:
    python regenerate_descriptions.py
    python regenerate_descriptions.py --dry-run          # print descriptions, don't write
    python regenerate_descriptions.py --codes AM-002     # single case
    python regenerate_descriptions.py --model claude-sonnet-4-6
"""

import json
import os
import re
import sys
import time
from argparse import ArgumentParser
from pathlib import Path

try:
    import anthropic
except ImportError:
    sys.exit("Error: run  pip install anthropic  first.")

# ---------------------------------------------------------------------------
# Case mapping: interview code -> project pubId
# ---------------------------------------------------------------------------
CASES = {
    "AM-002": "479752",
    "AR-002": "450652",
    "AR-172": "452552",
    "AR-055": "452052",
    "CA-002": "495252",
    "CO-307": "469252",
    "CO-336": "499552",
    "CO-601": "467152",
    "CR-001": "441152",
    "DK-024": "448352",
    "DK-122": "464952",
    "ES-011": "495652",
    "ES-055": "472052",
    "FR-111": "498852",
    "FR-194": "484752",
    "FR-253": "457652",
    "GE-010": "470152",
    "IN-011": "503452",
    "KE-086": "475252",
    "LK-002": "478852",
    "MA-022": "478252",
    "UG-021": "462652",
    "US-068": "508152",
    "WL-001": "470252",
    "ZA-040": "510952",
}

# Interviewer / moderator speaker names to exclude (lowercase)
INTERVIEWER_NAMES = {
    "alex", "oleg", "interviewer", "moderator", "intervieweur",
    "entrevistador", "interviewer 1", "interviewer 2",
    "int", "int.", "q", "question",
}

# Hard cap: characters of interviewee speech to send to the API
# (~15 000 words — well within claude's context but avoids huge CO-307)
MAX_CHARS = 90_000

SYSTEM_PROMPT = """\
You are a research writer producing factual descriptions of food-system initiatives
for a public-facing database. You will receive a transcript of an interview with
someone involved in a food-related organisation, business, farm, or project.

Write a factual, third-person description of what this organisation does, based
solely on what is said in the transcript. Follow these rules strictly:

1. Be factual and concrete — describe what the organisation actually does, how it
   works, what it produces or provides, who it works with, and what its goals are.
2. Do NOT interpret, evaluate, or speculate — do not write "seems to", "appears to",
   "aims to" (use "works to"), "focuses on", "is committed to", or similar soft
   language. State facts.
3. Do NOT use the words: initiative, case, project (unless it is an official name),
   scheme, programme (unless official), or endeavour.
4. Avoid proper nouns — venue names, personal names, brand names — where possible.
   If the transcript name transcription seems unreliable for a proper noun, omit it.
   Use a name only when it is clearly correct and necessary for identification.
5. Write 3–4 paragraphs, roughly 200–300 words in English. Be specific and dense
   with concrete detail drawn from the transcript.
6. Translations into FR, ES, DE must be natural and idiomatic — not word-for-word.

Return ONLY a JSON object with exactly these four keys: "en", "fr", "es", "de".
No markdown, no explanation, no extra keys.
"""


def find_transcript(transcripts_dir: Path, code: str) -> Path | None:
    # Case-insensitive glob
    for f in transcripts_dir.iterdir():
        if f.name.lower().startswith(code.lower() + "_"):
            return f
    return None


def is_interviewer(speaker: str) -> bool:
    return speaker.strip().lower() in INTERVIEWER_NAMES


def extract_interviewee_speech(transcript_data: dict) -> str:
    """
    Concatenate all non-interviewer speech across all sheets.
    Returns a single string of paragraphs labelled by speaker turn.
    """
    chunks = []
    seen_speakers: set[str] = set()

    for sheet in transcript_data.get("sheets", []):
        for entry in sheet.get("entries", []):
            speaker = entry.get("speaker", "").strip()
            text = entry.get("text", "").strip()
            if not text or is_interviewer(speaker):
                continue
            seen_speakers.add(speaker)
            chunks.append(text)

    speech = "\n\n".join(chunks)

    # Trim if oversized
    if len(speech) > MAX_CHARS:
        # Keep first 60 % and last 20 % to capture both opening and closing remarks
        head = int(MAX_CHARS * 0.65)
        tail = int(MAX_CHARS * 0.20)
        speech = speech[:head] + "\n\n[... transcript trimmed for length ...]\n\n" + speech[-tail:]

    return speech


def call_claude(client: anthropic.Anthropic, speech: str, model: str) -> dict:
    response = client.messages.create(
        model=model,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": (
                    "Here is the interviewee's speech from the transcript:\n\n"
                    + speech
                    + "\n\nPlease write the description now."
                ),
            }
        ],
    )
    raw = response.content[0].text.strip()

    # Strip markdown fences if present
    if raw.startswith("```"):
        raw = re.sub(r"^```[a-z]*\n?", "", raw)
        raw = re.sub(r"\n?```$", "", raw.strip())

    result = json.loads(raw)
    for lang in ("en", "fr", "es", "de"):
        if lang not in result:
            raise ValueError(f"Claude response missing '{lang}' key")
    return result


def process_case(
    code: str,
    pub_id: str,
    transcripts_dir: Path,
    projects_dir: Path,
    client: anthropic.Anthropic,
    model: str,
    dry_run: bool,
) -> bool:
    transcript_path = find_transcript(transcripts_dir, code)
    if transcript_path is None:
        print(f"  [{code}] Transcript not found — skipping.")
        return False

    project_path = projects_dir / f"{pub_id}.json"
    if not project_path.exists():
        print(f"  [{code}] Project file {pub_id}.json not found — skipping.")
        return False

    with open(transcript_path, encoding="utf-8") as f:
        transcript_data = json.load(f)

    speech = extract_interviewee_speech(transcript_data)
    if len(speech) < 100:
        print(f"  [{code}] Too little interviewee speech extracted — skipping.")
        return False

    print(f"  [{code}] {len(speech):,} chars of speech → calling Claude ...", end="", flush=True)

    try:
        descriptions = call_claude(client, speech, model)
    except (json.JSONDecodeError, ValueError) as e:
        print(f" ERROR parsing response: {e}")
        return False
    except anthropic.APIError as e:
        print(f" API ERROR: {e}")
        return False

    print(" done.")

    if dry_run:
        print(f"\n--- [{code}] EN preview ---")
        print(descriptions["en"][:600], "...")
        print()
        return True

    with open(project_path, encoding="utf-8") as f:
        project = json.load(f)

    project["description"] = {
        "en": descriptions["en"],
        "fr": descriptions["fr"],
        "es": descriptions["es"],
        "de": descriptions["de"],
    }

    with open(project_path, "w", encoding="utf-8") as f:
        json.dump(project, f, ensure_ascii=False, indent=2)
        f.write("\n")

    return True


def main() -> None:
    parser = ArgumentParser(description="Regenerate project descriptions from transcripts.")
    parser.add_argument("--api-key", default=os.environ.get("ANTHROPIC_API_KEY"))
    parser.add_argument("--model", default="claude-sonnet-4-6")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--codes",
        nargs="+",
        metavar="CODE",
        help="Only process these codes (e.g. AM-002 AR-002)",
    )
    parser.add_argument(
        "--transcripts-dir",
        default=str(Path(__file__).parent.parent.parent / "fos-transcripts"),
    )
    parser.add_argument(
        "--projects-dir",
        default=str(Path(__file__).parent),
    )
    args = parser.parse_args()

    if not args.api_key:
        sys.exit("Error: set ANTHROPIC_API_KEY or pass --api-key")

    transcripts_dir = Path(args.transcripts_dir)
    projects_dir = Path(args.projects_dir)

    cases = {k: v for k, v in CASES.items() if not args.codes or k in args.codes}
    if not cases:
        sys.exit("No matching cases found.")

    client = anthropic.Anthropic(api_key=args.api_key)

    print(f"Processing {len(cases)} case(s) with {args.model}{'  [DRY RUN]' if args.dry_run else ''}\n")

    ok = fail = 0
    for code, pub_id in sorted(cases.items()):
        success = process_case(
            code, pub_id, transcripts_dir, projects_dir,
            client, args.model, args.dry_run,
        )
        if success:
            ok += 1
        else:
            fail += 1
        # Small delay to avoid rate-limit bursts
        time.sleep(0.3)

    print(f"\nDone — {ok} updated, {fail} skipped/failed.")


if __name__ == "__main__":
    main()
