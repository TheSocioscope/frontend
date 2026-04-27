"""
Renames content/projects/*.json from pubId-based names (e.g. 479752.json)
to slugified initiative names (e.g. steakarar-restaurant.json).

Source of truth: Global tracker - Mapping.csv  (Initiative Name column)
Collision guard: if two names produce the same slug, the pubId is appended
                 to the second one (e.g. some-name-479752.json).
"""

import csv
import json
import os
import re
import unicodedata
from pathlib import Path


def slugify(text: str) -> str:
    """Convert an initiative name to a safe, human-readable filename slug."""
    # Normalise Unicode: decompose accented characters
    text = unicodedata.normalize('NFD', text)
    # Drop combining marks (accents, etc.)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    text = text.lower()
    # Replace anything that isn't alphanumeric or hyphen with a hyphen
    text = re.sub(r'[^a-z0-9]+', '-', text)
    # Collapse and strip leading/trailing hyphens
    text = text.strip('-')
    # Limit length to keep filenames sane
    return text[:80].rstrip('-')


def read_mapping(csv_path: Path) -> dict[int, str]:
    """Returns {pubId: initiative_name} for rows that have both fields."""
    mapping: dict[int, str] = {}
    with open(csv_path, encoding='utf-8-sig', newline='') as f:
        for row in csv.DictReader(f):
            raw_id = row.get('website id', '').strip()
            name = row.get('Initiative Name', '').strip()
            if raw_id and name:
                try:
                    mapping[int(float(raw_id))] = name
                except ValueError:
                    pass
    return mapping


def main():
    base = Path(__file__).parent.parent
    projects_dir = base / 'content' / 'projects'
    csv_path = base / 'Global tracker - Mapping.csv'

    mapping = read_mapping(csv_path)

    # First pass: build the desired slug for every file
    plan: list[tuple[Path, int, str, str]] = []  # (path, pubId, name, desired_slug)

    for json_file in sorted(projects_dir.glob('*.json')):
        try:
            data = json.loads(json_file.read_text(encoding='utf-8'))
        except Exception as e:
            print(f'SKIP (parse error) {json_file.name}: {e}')
            continue

        pub_id = data.get('pubId')
        if pub_id not in mapping:
            print(f'SKIP (not in mapping) {json_file.name}')
            continue

        name = mapping[pub_id]
        slug = slugify(name)
        if not slug:
            print(f'SKIP (empty slug) {json_file.name} -> "{name}"')
            continue

        plan.append((json_file, pub_id, name, slug))

    # Second pass: detect slug collisions and add pubId suffix where needed
    slug_counts: dict[str, int] = {}
    for _, _, _, slug in plan:
        slug_counts[slug] = slug_counts.get(slug, 0) + 1

    collisions = {s for s, n in slug_counts.items() if n > 1}
    if collisions:
        print(f'\nCollisions detected ({len(collisions)}): {sorted(collisions)}\n')

    # Track slugs already assigned in this run to disambiguate
    assigned: set[str] = set()

    renamed = skipped_same = errors = 0

    for json_file, pub_id, name, slug in plan:
        if slug in collisions or slug in assigned:
            final_slug = f'{slug}-{pub_id}'
        else:
            final_slug = slug

        assigned.add(final_slug)
        target = projects_dir / f'{final_slug}.json'

        if json_file == target:
            skipped_same += 1
            continue

        if target.exists():
            print(f'ERROR: target exists {target.name} (for {json_file.name})')
            errors += 1
            continue

        try:
            os.rename(json_file, target)
            print(f'  {json_file.name}  ->  {target.name}')
            renamed += 1
        except Exception as e:
            print(f'ERROR renaming {json_file.name}: {e}')
            errors += 1

    print(f'\nRenamed : {renamed}')
    print(f'Already correct: {skipped_same}')
    print(f'Errors  : {errors}')


if __name__ == '__main__':
    main()
