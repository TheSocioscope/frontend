#!/usr/bin/env python3
"""
Script to merge duplicate project files while preserving unique information.
Generates a report for manual confirmation before executing merges.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple

# Define obvious duplicate groups to merge (based on the analysis)
# Each group lists files where the FIRST file will be kept and others merged into it

MERGE_GROUPS = [
    # Group 3: Caresà Agricultural Cooperative Society
    {
        "keep": "431252.json",
        "merge": ["430552.json"],
        "reason": "Same organization, 89.66% name similarity, same location"
    },
    
    # Group 4: Sensitive agriculture by Marck Pépin
    {
        "keep": "443552.json",
        "merge": ["431152.json"],
        "reason": "Same author, 87.39% name similarity - different aspects of same project"
    },
    
    # Group 10: Flenexa (3 entries for same company)
    {
        "keep": "439452.json",
        "merge": ["439852.json", "430052.json"],
        "reason": "Same company, 100% name match, same location"
    },
    
    # Group 13: Mulino Terrevive (6 identical entries)
    {
        "keep": "431352.json",
        "merge": ["432052.json", "432352.json", "430952.json", "430452.json", "432252.json"],
        "reason": "Same company, 100% name match, same contact, same location"
    },
    
    # Group 14: Mother Earth Farm (2 entries)
    {
        "keep": "437452.json",
        "merge": ["430252.json"],
        "reason": "Same farm, 100% name match, same location"
    },
    
    # Group 19: Aquaponia (2 entries)
    {
        "keep": "439352.json",
        "merge": ["439952.json"],
        "reason": "Same company, 100% name match, same location"
    },
    
    # Group 21: Riz-banane (2 identical entries)
    {
        "keep": "432652.json",
        "merge": ["431952.json"],
        "reason": "Same project, 100% name match, same contact"
    },
    
    # Group 23: Villa Rabelais (2 entries)
    {
        "keep": "439652.json",
        "merge": ["439252.json"],
        "reason": "Same venue, 100% name match, same contact"
    },
    
    # Group 26: Avana Vetiver (2 entries)
    {
        "keep": "431852.json",
        "merge": ["432752.json"],
        "reason": "Same company, 100% name match, same contact"
    }
]

def load_project(filepath: Path) -> Dict:
    """Load a project JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_project(filepath: Path, data: Dict):
    """Save a project JSON file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def merge_lists(list1: List, list2: List) -> List:
    """Merge two lists, removing duplicates while preserving order."""
    result = list(list1)
    for item in list2:
        if item not in result:
            result.append(item)
    return result

def merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """Merge two dictionaries, combining values for same keys."""
    result = dict(dict1)
    for key, value in dict2.items():
        if key not in result:
            result[key] = value
        elif isinstance(value, str) and value and (not result[key] or len(value) > len(result[key])):
            # Keep longer string if one is empty or shorter
            result[key] = value
    return result

def merge_projects(keep_data: Dict, merge_data: Dict) -> Dict:
    """
    Merge two project objects, keeping data from 'keep' but adding unique info from 'merge'.
    """
    merged = dict(keep_data)
    
    # Merge array fields (continent, country, date, field, thematic, type, etc.)
    for field in ['continent', 'country', 'date', 'field', 'thematic', 'type']:
        if field in merge_data:
            if field not in merged:
                merged[field] = merge_data[field]
            else:
                merged[field] = merge_lists(merged[field], merge_data[field])
    
    # Merge description objects (multiple languages)
    if 'description' in merge_data:
        if 'description' not in merged:
            merged['description'] = merge_data['description']
        elif isinstance(merged['description'], dict) and isinstance(merge_data['description'], dict):
            merged['description'] = merge_dicts(merged['description'], merge_data['description'])
    
    # Merge name objects (multiple languages)
    if 'name' in merge_data:
        if 'name' not in merged:
            merged['name'] = merge_data['name']
        elif isinstance(merged['name'], dict) and isinstance(merge_data['name'], dict):
            merged['name'] = merge_dicts(merged['name'], merge_data['name'])
    
    # Merge team arrays
    if 'team' in merge_data:
        if 'team' not in merged:
            merged['team'] = merge_data['team']
        else:
            # Add team members that aren't already in the list
            existing_members = {
                (m.get('firstname', '').lower(), m.get('lastname', '').lower(), m.get('entity', '').lower())
                for m in merged['team']
            }
            for member in merge_data['team']:
                member_key = (
                    member.get('firstname', '').lower(),
                    member.get('lastname', '').lower(),
                    member.get('entity', '').lower()
                )
                if member_key not in existing_members:
                    merged['team'].append(member)
    
    # Keep the earlier creation date
    if 'createdAt' in merge_data:
        if 'createdAt' not in merged or merge_data['createdAt'] < merged['createdAt']:
            merged['createdAt'] = merge_data['createdAt']
    
    # Use higher score if available
    if 'score' in merge_data:
        if 'score' not in merged or merge_data['score'] > merged['score']:
            merged['score'] = merge_data['score']
    
    # Preserve location and time info if missing
    for field in ['location', 'time']:
        if field in merge_data and (field not in merged or not merged[field]):
            merged[field] = merge_data[field]
    
    return merged

def generate_merge_report(projects_dir: Path, dry_run: bool = True) -> List[Dict]:
    """
    Generate a report of what will be merged.
    If dry_run=False, actually perform the merges.
    """
    report = []
    
    for group in MERGE_GROUPS:
        keep_file = projects_dir / group['keep']
        merge_files = [projects_dir / f for f in group['merge']]
        
        if not keep_file.exists():
            print(f"WARNING: Keep file {keep_file.name} does not exist!")
            continue
        
        keep_data = load_project(keep_file)
        merged_data = dict(keep_data)
        
        merge_info = {
            'keep_file': group['keep'],
            'merge_files': group['merge'],
            'reason': group['reason'],
            'changes': []
        }
        
        for merge_file in merge_files:
            if not merge_file.exists():
                print(f"WARNING: Merge file {merge_file.name} does not exist!")
                continue
            
            merge_data = load_project(merge_file)
            
            # Track what's being added
            before_keys = set(str(merged_data))
            merged_data = merge_projects(merged_data, merge_data)
            after_keys = set(str(merged_data))
            
            if before_keys != after_keys:
                merge_info['changes'].append(f"Added data from {merge_file.name}")
        
        report.append(merge_info)
        
        if not dry_run:
            # Save the merged file
            save_project(keep_file, merged_data)
            
            # Delete the merged files
            for merge_file in merge_files:
                if merge_file.exists():
                    merge_file.unlink()
                    print(f"Deleted {merge_file.name}")
    
    return report

def main():
    import sys
    
    script_dir = Path(__file__).parent
    
    # Check if --execute flag is passed
    execute = '--execute' in sys.argv
    
    if execute:
        print("=" * 80)
        print("EXECUTING MERGE OPERATION")
        print("=" * 80)
        response = input("\nAre you sure you want to merge the duplicates? This will DELETE files. (yes/no): ")
        if response.lower() != 'yes':
            print("Merge cancelled.")
            return
        print()
    else:
        print("=" * 80)
        print("DRY RUN - MERGE PREVIEW")
        print("=" * 80)
        print("Run with --execute flag to actually perform the merge.")
        print()
    
    report = generate_merge_report(script_dir, dry_run=not execute)
    
    print(f"\nMerge plan for {len(report)} groups:\n")
    
    for i, group in enumerate(report, 1):
        print(f"--- Group {i} ---")
        print(f"Keep: {group['keep_file']}")
        print(f"Merge into it: {', '.join(group['merge_files'])}")
        print(f"Reason: {group['reason']}")
        if group['changes']:
            print(f"Changes: {', '.join(group['changes'])}")
        else:
            print("Changes: No unique data to add")
        print()
    
    if execute:
        print(f"\n✓ Successfully merged {len(report)} groups")
        print(f"✓ Deleted {sum(len(g['merge_files']) for g in report)} duplicate files")
    else:
        print("\nTo execute this merge, run: python3 merge_duplicates.py --execute")

if __name__ == "__main__":
    main()
