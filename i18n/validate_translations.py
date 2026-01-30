#!/usr/bin/env python3
"""
Validation script to check that all $t() calls in Vue files have corresponding translation keys.
"""
import json
import re
from pathlib import Path

# Load the English translation file
with open('/home/bob/Projects/frontend/i18n/locales/en.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

def get_all_translation_keys(data, prefix=''):
    """Recursively get all translation keys from nested dict."""
    keys = []
    for key, value in data.items():
        current_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            keys.extend(get_all_translation_keys(value, current_key))
        else:
            keys.append(current_key)
    return set(keys)

def extract_t_calls_from_file(file_path):
    """Extract all $t() calls from a Vue file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Match $t('key') or $t("key")
        pattern = r'\$t\([\'"]([^\'"]+)[\'"]\)'
        matches = re.findall(pattern, content)
        return matches
    except Exception as e:
        print(f"⚠️  Error reading {file_path}: {e}")
        return []

# Get all available translation keys
available_keys = get_all_translation_keys(translations)
print(f"📊 Found {len(available_keys)} translation keys in en.json")

# Find all Vue files
app_dir = Path('/home/bob/Projects/frontend/app')
vue_files = list(app_dir.rglob('*.vue'))
print(f"📁 Scanning {len(vue_files)} Vue files...")

# Extract all used translation keys
used_keys = set()
file_keys = {}

for vue_file in vue_files:
    keys = extract_t_calls_from_file(vue_file)
    if keys:
        relative_path = vue_file.relative_to(Path('/home/bob/Projects/frontend'))
        file_keys[str(relative_path)] = keys
        used_keys.update(keys)

print(f"🔍 Found {len(used_keys)} unique translation keys used in Vue files")

# Find missing keys (used but not defined)
missing_keys = used_keys - available_keys
if missing_keys:
    print(f"\n❌ MISSING TRANSLATIONS ({len(missing_keys)} keys):")
    for key in sorted(missing_keys):
        # Find which files use this key
        files_using = [f for f, keys in file_keys.items() if key in keys]
        print(f"  • {key}")
        for file in files_using[:3]:  # Show first 3 files
            print(f"    └─ {file}")
else:
    print("\n✅ All used translation keys are defined!")

# Find unused keys (defined but not used)
unused_keys = available_keys - used_keys
if unused_keys:
    print(f"\n⚠️  UNUSED TRANSLATIONS ({len(unused_keys)} keys):")
    for key in sorted(unused_keys)[:20]:  # Show first 20
        print(f"  • {key}")
    if len(unused_keys) > 20:
        print(f"  ... and {len(unused_keys) - 20} more")
else:
    print("\n✅ All translation keys are used!")

# Summary
print(f"\n📈 SUMMARY:")
print(f"  • Total keys defined: {len(available_keys)}")
print(f"  • Total keys used: {len(used_keys)}")
print(f"  • Missing keys: {len(missing_keys)}")
print(f"  • Unused keys: {len(unused_keys)}")
print(f"  • Coverage: {(len(used_keys - missing_keys) / len(used_keys) * 100):.1f}%")

if len(missing_keys) == 0:
    print("\n✅ SUCCESS: All translation keys are properly bound to the UI!")
    exit(0)
else:
    print("\n⚠️  WARNING: Some translation keys are missing and need to be added.")
    exit(1)
