#!/usr/bin/env python3
"""
Analyzes a corpus to create a minimized, corpus-specific relation mapping file.

This script performs two main functions:
1. It scans a directory of .rs3 files to find all unique, actively used relations
(by looking at `relname` attributes) and their frequencies.
2. It generates a new JSON mapping file that only includes the relations found
in the corpus. It uses a base mapping file for known relations and applies
pre-defined rules for new relations.
"""

import os
import re
import json
import argparse
from collections import Counter

# --- Pre-defined rules for new relations found in the PCC corpus ---
# Based on our analysis, we decided on these mappings.
# This can be extended for future corpora.
NEW_RELATION_RULES = {
    "attribution": "attribution",  # Map to its own new class
    "sameunit": "sameunit",        # Map to its own new class
    "solutionhood-N": "solutionhood" # Merge with existing class
}

def get_corpus_relations(corpus_dir):
    """Scans the corpus and returns a Counter of relation frequencies."""
    relation_pattern = re.compile(r'relname=\"([^\"]+)\"')
    all_relations = []
    for filename in os.listdir(corpus_dir):
        if not filename.endswith('.rs3'):
            continue
        try:
            with open(os.path.join(corpus_dir, filename), 'r', encoding='utf-8') as f:
                content = f.read()
                relations_in_file = relation_pattern.findall(content)
                all_relations.extend(relations_in_file)
        except Exception as e:
            print(f"Warning: Could not process {filename}: {e}")
    return Counter(all_relations)

def generate_map(base_map_path, corpus_dir, output_path):
    """Generates the new, minimized relation map."""
    print(f"Loading base relation map from {base_map_path}")
    with open(base_map_path, 'r') as f:
        base_map = json.load(f)

    print(f"Analyzing relations in {corpus_dir}...")
    corpus_counts = get_corpus_relations(corpus_dir)
    if not corpus_counts:
        print("Error: No relations found in the corpus. Aborting.")
        return

    print("Found the following relation frequencies:")
    for rel, count in corpus_counts.most_common():
        print(f"{count:>5} {rel}")

    new_map = {}
    for rel in corpus_counts.keys():
        if rel in base_map:
            new_map[rel] = base_map[rel]
        elif rel in NEW_RELATION_RULES:
            new_map[rel] = NEW_RELATION_RULES[rel]
        else:
            print(f"\n---\nWarning: Relation '{rel}' is not in the base map or pre-defined rules!" \
                  f"Defaulting to map to itself: '{rel}' -> '{rel}'\n---")
            new_map[rel] = rel

    print(f"\nGenerated new map with {len(new_map)} relations.")
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(new_map, f, indent=4)
    
    print(f"Successfully saved new relation map to {output_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate a corpus-specific relation map.")
    parser.add_argument('corpus_dir', type=str,
                        help="Directory containing the .rs3 corpus files (e.g., 'data/pcc/training').")
    parser.add_argument('output_path', type=str,
                        help="Path to save the new JSON mapping file (e.g., 'data/pcc/pcc_rel_mapping.json').")
    parser.add_argument('--base_map', type=str, default='parsing_eval_metrics/rel_mapping.json',
                        help="Path to the base relation mapping file.")

    args = parser.parse_args()

    # We should scan the entire corpus, so we point to the parent of the training dir
    full_corpus_dir = os.path.join(os.path.dirname(args.corpus_dir), 'rs3')
    if not os.path.exists(full_corpus_dir):
        print(f"Warning: Full corpus directory not found at {full_corpus_dir}." \
              f"Falling back to scanning only the provided directory: {args.corpus_dir}")
        full_corpus_dir = args.corpus_dir

generate_map(args.base_map, full_corpus_dir, args.output_path)
