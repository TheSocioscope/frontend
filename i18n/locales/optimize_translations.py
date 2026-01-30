#!/usr/bin/env python3
"""
Script to optimize translation files based on the optimized English structure.
Preserves existing translations from FR, ES, DE files.
"""
import json
from pathlib import Path

# Load the optimized English file as the template
with open('en.json', 'r', encoding='utf-8') as f:
    en_template = json.load(f)

# Load existing translations
with open('fr.json.backup', 'r', encoding='utf-8') as f:
    fr_old = json.load(f)

with open('es.json.backup', 'r', encoding='utf-8') as f:
    es_old = json.load(f)

with open('de.json.backup', 'r', encoding='utf-8') as f:
    de_old = json.load(f)

def get_nested_value(data, path):
    """Get value from nested dict using dot notation path."""
    keys = path.split('.')
    value = data
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return None
    return value

def set_nested_value(data, path, value):
    """Set value in nested dict using dot notation path."""
    keys = path.split('.')
    current = data
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    current[keys[-1]] = value

def get_all_paths(data, prefix=''):
    """Get all paths from a nested dict."""
    paths = []
    for key, value in data.items():
        current_path = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            paths.extend(get_all_paths(value, current_path))
        else:
            paths.append(current_path)
    return paths

def build_translation(template, old_data):
    """Build new translation dict preserving old translations where they exist."""
    new_data = {}
    paths = get_all_paths(template)
    
    for path in paths:
        old_value = get_nested_value(old_data, path)
        if old_value is not None:
            set_nested_value(new_data, path, old_value)
        else:
            # Use English as fallback
            en_value = get_nested_value(template, path)
            set_nested_value(new_data, path, en_value)
    
    return new_data

# Build optimized translations
fr_optimized = build_translation(en_template, fr_old)
es_optimized = build_translation(en_template, es_old)
de_optimized = build_translation(en_template, de_old)

# Save optimized files
with open('fr.json', 'w', encoding='utf-8') as f:
    json.dump(fr_optimized, f, ensure_ascii=False, indent=2)

with open('es.json', 'w', encoding='utf-8') as f:
    json.dump(es_optimized, f, ensure_ascii=False, indent=2)

with open('de.json', 'w', encoding='utf-8') as f:
    json.dump(de_optimized, f, ensure_ascii=False, indent=2)

print("✅ Successfully optimized all translation files!")
print("📋 French, Spanish, and German translations have been updated to match the English structure.")
print("🔄 Existing translations were preserved where possible.")
