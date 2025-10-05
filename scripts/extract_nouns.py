#!/usr/bin/env python3
"""
Extract noun terms from glossary.json

This script identifies and extracts noun terms from the glossary including:
- Person names
- Place names
- Organization names
- Deity/religion names
- Classes/professions
- Race/creature/animal names
- Weapon/armor/item names
- Spell names
- Military ranks/armies
"""

import json
import re
from typing import Dict, List, Set
from collections import defaultdict


class NounExtractor:
    """Extract noun terms from glossary entries."""

    def __init__(self):
        # Pattern definitions for identifying nouns
        self.patterns = {
            'proper_noun': [
                # Capitalized words (English proper nouns)
                r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',
                # Common fantasy/D&D name patterns
                r'\b[A-Z][a-z]+\'[a-z]+\b',  # e.g., Drizzt'Do
            ],
            'title': [
                # Titles and honorifics
                r'\b(?:Lord|Lady|Sir|Duke|Duchess|King|Queen|Prince|Princess|Baron|Count|Master|Mistress)\s+[A-Z][a-z]+',
            ],
            'location': [
                # Common location indicators
                r'\b(?:the\s+)?[A-Z][a-z]+\s+(?:Gate|Keep|Castle|Tower|Forest|Mountains?|Hills?|River|Lake|Sea|Coast|Valley|Plains?)',
            ],
            'organization': [
                # Organization patterns
                r'\b(?:the\s+)?[A-Z][a-z]+\s+(?:Throne|Order|Guild|Company|Legion|Army|Guard|Watch)',
            ],
            'deity': [
                # Deity/religious patterns
                r'\b(?:the\s+)?(?:Temple|Church|Shrine)\s+of\s+[A-Z][a-z]+',
            ],
            'class_race': [
                # D&D classes and races
                r'\b(?:Fighter|Mage|Wizard|Cleric|Thief|Ranger|Paladin|Druid|Bard|Monk|Sorcerer|Barbarian)\b',
                r'\b(?:Human|Elf|Dwarf|Halfling|Gnome|Half-Elf|Half-Orc|Drow)\b',
            ],
            'creature': [
                # Fantasy creatures
                r'\b(?:Dragon|Wyvern|Basilisk|Beholder|Mind Flayer|Lich|Vampire|Werewolf|Zombie|Skeleton|Ghost|Demon|Devil|Elemental|Giant|Troll|Ogre|Goblin|Kobold|Orc)\b',
            ],
            'spell': [
                # Spell patterns (often start with verb/adjective)
                r'\b[A-Z][a-z]+(?:\'s)?\s+[A-Z][a-z]+\b',  # e.g., "Melf's Acid Arrow"
            ]
        }

        # Known game-specific terms (from BG series)
        self.known_terms = {
            'location': {
                "Sword Coast", "Baldur's Gate", "Candlekeep", "Nashkel", "Beregost",
                "Friendly Arm Inn", "High Hedge", "Underdark", "Athkatla", "Amn",
                "Waterdeep", "Neverwinter", "Calimshan", "Cormyr", "Sembia"
            },
            'organization': {
                "Iron Throne", "Flaming Fist", "Shadow Thieves", "Harpers",
                "Zhentarim", "Red Wizards", "Cowled Wizards"
            },
            'deity': {
                "Bhaal", "Mystra", "Helm", "Tyr", "Lathander", "Tempus",
                "Talos", "Bane", "Cyric", "Shar", "Selûne", "Ilmater"
            },
            'class': {
                "Fighter", "Mage", "Wizard", "Cleric", "Thief", "Ranger",
                "Paladin", "Druid", "Bard", "Monk", "Sorcerer", "Barbarian",
                "Assassin", "Berserker", "Shapeshifter", "Bounty Hunter"
            },
            'race': {
                "Human", "Elf", "Dwarf", "Halfling", "Gnome", "Half-Elf",
                "Half-Orc", "Drow"
            }
        }

        # Track extracted terms
        self.extracted_terms: Dict[str, Dict[str, List[Dict]]] = defaultdict(lambda: defaultdict(list))
        self.term_translations: Dict[str, Set[str]] = defaultdict(set)

    def is_likely_noun(self, english: str, japanese: str) -> bool:
        """Check if a term pair is likely to be a noun."""
        # Skip very long texts (likely sentences/dialogue)
        if len(english) > 100 or english.count(' ') > 8:
            return False

        # Skip common sentence patterns
        if any(english.lower().startswith(x) for x in ['you ', 'i ', 'we ', 'they ', 'he ', 'she ']):
            return False

        # Check for capitalization (proper nouns)
        words = english.split()
        if len(words) <= 4 and any(w[0].isupper() for w in words if w):
            return True

        return False

    def categorize_term(self, english: str) -> List[str]:
        """Categorize a term based on patterns."""
        categories = []

        # Check against known terms
        for category, terms in self.known_terms.items():
            if english in terms or any(term in english for term in terms):
                categories.append(category)

        # Pattern matching
        for category, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, english):
                    categories.append(category)
                    break

        return list(set(categories)) if categories else ['other']

    def extract_terms_from_entry(self, entry: Dict) -> None:
        """Extract noun terms from a single glossary entry."""
        english = entry['english']
        japanese_default = entry['japanese']['default']

        if not self.is_likely_noun(english, japanese_default):
            return

        categories = self.categorize_term(english)

        term_data = {
            'id': entry['id'],
            'english': english,
            'japanese': japanese_default,
            'game': entry['metadata']['game'],
            'categories': categories
        }

        # Add gender variants if present
        if entry['japanese']['male']:
            term_data['japanese_male'] = entry['japanese']['male']
        if entry['japanese']['female']:
            term_data['japanese_female'] = entry['japanese']['female']

        # Store in all applicable categories
        for category in categories:
            self.extracted_terms[category]['terms'].append(term_data)

        # Track translation mapping
        self.term_translations[english].add(japanese_default)

    def extract_from_glossary(self, glossary_path: str) -> Dict:
        """Extract all noun terms from glossary."""
        print(f"Loading glossary from {glossary_path}...")

        with open(glossary_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        total_entries = len(data['entries'])
        print(f"Processing {total_entries:,} entries...")

        # Process all entries
        for i, entry in enumerate(data['entries']):
            if i % 10000 == 0:
                print(f"  Processed {i:,} / {total_entries:,} entries...")
            self.extract_terms_from_entry(entry)

        print(f"Extraction complete!")

        # Compile results
        results = {
            'metadata': {
                'source_file': 'glossary.json',
                'total_entries_processed': total_entries,
                'extraction_date': data['metadata']['generated_at'],
                'categories': list(self.extracted_terms.keys())
            },
            'categories': {}
        }

        # Organize by category
        for category in sorted(self.extracted_terms.keys()):
            terms = self.extracted_terms[category]['terms']
            results['categories'][category] = {
                'count': len(terms),
                'terms': sorted(terms, key=lambda x: x['english'])
            }
            print(f"  {category}: {len(terms):,} terms")

        return results

    def save_results(self, results: Dict, output_path: str) -> None:
        """Save extracted nouns to JSON file."""
        print(f"\nSaving results to {output_path}...")

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print(f"Saved {sum(cat['count'] for cat in results['categories'].values()):,} noun terms")


def main():
    """Main execution."""
    import sys

    glossary_path = 'glossary.json'
    output_path = 'nouns_glossary.json'

    if len(sys.argv) > 1:
        glossary_path = sys.argv[1]
    if len(sys.argv) > 2:
        output_path = sys.argv[2]

    extractor = NounExtractor()
    results = extractor.extract_from_glossary(glossary_path)
    extractor.save_results(results, output_path)

    print("\n✓ Noun extraction complete!")


if __name__ == '__main__':
    main()
