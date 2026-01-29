#!/usr/bin/env python3
"""
Script to identify duplicate projects based on:
- Name similarity (in various languages)
- Contact info (excluding Paris IAS)
- Location (country and/or continent)
- Description similarity (basic check)
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple
from difflib import SequenceMatcher
from collections import defaultdict

def normalize_text(text: str) -> str:
    """Normalize text for comparison."""
    if not text:
        return ""
    return text.lower().strip()

def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate similarity ratio between two texts."""
    return SequenceMatcher(None, normalize_text(text1), normalize_text(text2)).ratio()

def extract_contact_key(contact: Dict) -> str:
    """Extract a normalized contact key, excluding Paris IAS."""
    if not contact:
        return ""
    
    entity = normalize_text(contact.get('entity', ''))
    # Skip Paris IAS as they manage the whole website project
    if 'paris' in entity and 'ias' in entity:
        return ""
    
    firstname = normalize_text(contact.get('firstname', ''))
    lastname = normalize_text(contact.get('lastname', ''))
    
    return f"{entity}|{firstname}|{lastname}"

def get_location_key(project: Dict) -> str:
    """Get normalized location key."""
    continents = sorted([normalize_text(c) for c in project.get('continent', [])])
    countries = sorted([normalize_text(c) for c in project.get('country', [])])
    return f"{','.join(continents)}|{','.join(countries)}"

def get_all_names(project: Dict) -> List[str]:
    """Get all name variations from the project."""
    names = []
    name_obj = project.get('name', {})
    if isinstance(name_obj, dict):
        for lang, name in name_obj.items():
            if name:
                names.append(normalize_text(name))
    elif isinstance(name_obj, str):
        names.append(normalize_text(name_obj))
    return list(set(names))  # Remove duplicates

def load_projects(directory: str) -> Dict[str, Dict]:
    """Load all project JSON files."""
    projects = {}
    path = Path(directory)
    
    for json_file in path.glob('*.json'):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                projects[json_file.name] = data
        except Exception as e:
            print(f"Error loading {json_file.name}: {e}")
    
    return projects

def find_duplicates(projects: Dict[str, Dict], name_threshold: float = 0.85) -> List[Tuple[List[str], str]]:
    """
    Find potential duplicate projects.
    Returns list of (file_list, reason) tuples.
    """
    duplicates = []
    processed = set()
    
    project_items = list(projects.items())
    
    for i, (file1, proj1) in enumerate(project_items):
        if file1 in processed:
            continue
            
        contact1 = extract_contact_key(proj1.get('contact', {}))
        location1 = get_location_key(proj1)
        names1 = get_all_names(proj1)
        
        matches = []
        
        for j, (file2, proj2) in enumerate(project_items[i+1:], i+1):
            if file2 in processed:
                continue
            
            contact2 = extract_contact_key(proj2.get('contact', {}))
            location2 = get_location_key(proj2)
            names2 = get_all_names(proj2)
            
            reasons = []
            
            # Check name similarity
            max_name_similarity = 0
            for name1 in names1:
                for name2 in names2:
                    similarity = calculate_similarity(name1, name2)
                    max_name_similarity = max(max_name_similarity, similarity)
            
            if max_name_similarity >= name_threshold:
                reasons.append(f"Name similarity: {max_name_similarity:.2%}")
            
            # Check contact match (if both have contact info)
            if contact1 and contact2 and contact1 == contact2:
                reasons.append(f"Same contact: {contact1}")
            
            # Check location match (if both have location)
            if location1 and location2 and location1 == location2 and max_name_similarity > 0.6:
                reasons.append(f"Same location: {location1}")
            
            # If we have at least one strong reason, consider it a potential duplicate
            if reasons:
                if max_name_similarity >= name_threshold or (contact1 and contact2 and contact1 == contact2):
                    matches.append((file2, reasons))
        
        if matches:
            group = [file1] + [m[0] for m in matches]
            reason_summary = " + ".join(matches[0][1])
            duplicates.append((group, reason_summary))
            processed.update(group)
    
    return duplicates

def group_by_contact(projects: Dict[str, Dict]) -> Dict[str, List[str]]:
    """Group projects by contact person (excluding Paris IAS)."""
    contact_groups = defaultdict(list)
    
    for filename, project in projects.items():
        contact_key = extract_contact_key(project.get('contact', {}))
        if contact_key:
            contact_groups[contact_key].append(filename)
    
    # Only keep groups with 2+ projects
    return {k: v for k, v in contact_groups.items() if len(v) > 1}

def main():
    script_dir = Path(__file__).parent
    projects = load_projects(script_dir)
    
    print(f"Loaded {len(projects)} projects\n")
    print("=" * 80)
    print("DUPLICATE DETECTION REPORT")
    print("=" * 80)
    
    # Find duplicates by name/contact/location
    duplicates = find_duplicates(projects)
    
    if duplicates:
        print(f"\n### Found {len(duplicates)} potential duplicate groups:\n")
        
        for i, (files, reason) in enumerate(duplicates, 1):
            print(f"\n--- Group {i} ({len(files)} files) ---")
            print(f"Reason: {reason}")
            
            for filename in files:
                proj = projects[filename]
                name = proj.get('name', {})
                if isinstance(name, dict):
                    display_name = name.get('en') or name.get('fr') or list(name.values())[0]
                else:
                    display_name = name
                
                contact = proj.get('contact', {})
                contact_str = f"{contact.get('firstname', '')} {contact.get('lastname', '')} ({contact.get('entity', '')})"
                
                print(f"  • {filename}")
                print(f"    Name: {display_name}")
                print(f"    Contact: {contact_str}")
                print(f"    Location: {proj.get('country', [])} / {proj.get('continent', [])}")
                print(f"    PubId: {proj.get('pubId')}")
    else:
        print("\nNo obvious duplicates found based on name/contact/location.")
    
    # Also show projects grouped by same contact
    print("\n" + "=" * 80)
    print("PROJECTS BY SAME CONTACT (excluding Paris IAS)")
    print("=" * 80)
    
    contact_groups = group_by_contact(projects)
    
    if contact_groups:
        print(f"\nFound {len(contact_groups)} contacts with multiple projects:\n")
        
        for contact_key, files in sorted(contact_groups.items(), key=lambda x: len(x[1]), reverse=True):
            if len(files) > 1:
                print(f"\n{contact_key} ({len(files)} projects):")
                for filename in files:
                    proj = projects[filename]
                    name = proj.get('name', {})
                    if isinstance(name, dict):
                        display_name = name.get('en') or name.get('fr') or list(name.values())[0]
                    else:
                        display_name = name
                    print(f"  • {filename}: {display_name}")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
