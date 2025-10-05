#!/usr/bin/env python3
"""
Deduplicate nouns_glossary.json by merging entries with identical English-Japanese pairs.

Entries with the same English text and Japanese translation are merged into a single entry,
preserving all source IDs and metadata.
"""

import json
from typing import Dict, List, Set
from collections import defaultdict


class NounDeduplicator:
    """Deduplicate noun glossary entries."""

    def __init__(self):
        self.stats = {
            'original_count': 0,
            'deduplicated_count': 0,
            'removed_duplicates': 0
        }

    def create_key(self, english: str, japanese: str) -> str:
        """Create a unique key for English-Japanese pair."""
        return f"{english}|||{japanese}"

    def merge_entries(self, entries: List[Dict]) -> Dict:
        """Merge multiple entries with the same English-Japanese pair."""
        if len(entries) == 1:
            return entries[0]

        # Use first entry as base
        merged = entries[0].copy()

        # Collect all IDs and games
        all_ids = []
        all_games = set()
        all_categories = set()

        for entry in entries:
            all_ids.append(entry['id'])
            all_games.add(entry['game'])
            all_categories.update(entry['categories'])

        # Update merged entry
        merged['ids'] = sorted(all_ids)  # All source IDs
        merged['games'] = sorted(list(all_games))  # All games where this term appears
        merged['categories'] = sorted(list(all_categories))  # All applicable categories
        merged['occurrence_count'] = len(entries)  # How many times this term appeared

        # Remove single 'id' field in favor of 'ids'
        if 'id' in merged:
            del merged['id']
        if 'game' in merged:
            del merged['game']

        # Handle gender variants - keep if any entry has them
        if 'japanese_male' not in merged or not merged.get('japanese_male'):
            for entry in entries:
                if entry.get('japanese_male'):
                    merged['japanese_male'] = entry['japanese_male']
                    break

        if 'japanese_female' not in merged or not merged.get('japanese_female'):
            for entry in entries:
                if entry.get('japanese_female'):
                    merged['japanese_female'] = entry['japanese_female']
                    break

        return merged

    def deduplicate_category(self, terms: List[Dict]) -> List[Dict]:
        """Deduplicate terms within a category."""
        # Group by English-Japanese pair
        term_groups = defaultdict(list)

        for term in terms:
            key = self.create_key(term['english'], term['japanese'])
            term_groups[key].append(term)

        # Merge duplicates
        deduplicated = []
        for key, entries in term_groups.items():
            merged = self.merge_entries(entries)
            deduplicated.append(merged)

        # Sort by English text
        deduplicated.sort(key=lambda x: x['english'].lower())

        return deduplicated

    def deduplicate_glossary(self, input_path: str) -> Dict:
        """Deduplicate entire noun glossary."""
        print(f"Loading noun glossary from {input_path}...")

        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        original_total = sum(cat['count'] for cat in data['categories'].values())
        self.stats['original_count'] = original_total

        print(f"Original total: {original_total:,} noun terms")
        print(f"Processing {len(data['categories'])} categories...\n")

        # Process each category
        deduplicated_categories = {}

        for category, cat_data in sorted(data['categories'].items()):
            original_count = cat_data['count']
            terms = cat_data['terms']

            deduplicated = self.deduplicate_category(terms)
            removed = original_count - len(deduplicated)

            deduplicated_categories[category] = {
                'count': len(deduplicated),
                'terms': deduplicated
            }

            print(f"  {category}:")
            print(f"    Original: {original_count:,} terms")
            print(f"    After deduplication: {len(deduplicated):,} terms")
            print(f"    Removed: {removed:,} duplicates")

        deduplicated_total = sum(cat['count'] for cat in deduplicated_categories.values())
        self.stats['deduplicated_count'] = deduplicated_total
        self.stats['removed_duplicates'] = original_total - deduplicated_total

        print(f"\n{'='*60}")
        print(f"Total original entries: {original_total:,}")
        print(f"Total after deduplication: {deduplicated_total:,}")
        print(f"Total duplicates removed: {self.stats['removed_duplicates']:,}")
        print(f"Deduplication rate: {(self.stats['removed_duplicates']/original_total*100):.1f}%")

        # Build result
        result = {
            'metadata': {
                'source_file': data['metadata']['source_file'],
                'total_entries_processed': data['metadata']['total_entries_processed'],
                'extraction_date': data['metadata']['extraction_date'],
                'deduplication_stats': {
                    'original_term_count': original_total,
                    'deduplicated_term_count': deduplicated_total,
                    'duplicates_removed': self.stats['removed_duplicates'],
                    'deduplication_rate': f"{(self.stats['removed_duplicates']/original_total*100):.1f}%"
                },
                'categories': list(deduplicated_categories.keys())
            },
            'categories': deduplicated_categories
        }

        return result

    def save_results(self, results: Dict, output_path: str) -> None:
        """Save deduplicated results."""
        print(f"\nSaving deduplicated glossary to {output_path}...")

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print(f"✓ Saved successfully!")


def main():
    """Main execution."""
    import sys

    input_path = 'nouns_glossary.json'
    output_path = 'nouns_glossary.json'  # Overwrite by default

    if len(sys.argv) > 1:
        input_path = sys.argv[1]
    if len(sys.argv) > 2:
        output_path = sys.argv[2]

    deduplicator = NounDeduplicator()
    results = deduplicator.deduplicate_glossary(input_path)
    deduplicator.save_results(results, output_path)

    print("\n✓ Deduplication complete!")


if __name__ == '__main__':
    main()
