"""
TRA file parser for Infinity Engine translation files
"""

import re
import logging
from pathlib import Path
from typing import Dict, Tuple, Optional
from .models import TRAEntry, JapaneseTranslation

logger = logging.getLogger(__name__)


class TRAParser:
    """Parser for TRA (translation) files"""

    # Regex patterns
    ENTRY_PATTERN = re.compile(r'^@(\d+)\s*=\s*~(.*)~\s*$')
    GENDER_VARIANT_PATTERN = re.compile(r'^@(\d+)\s*=\s*~([^~]*)~\s*~([^~]*)~\s*$')

    def __init__(self):
        self.entries_parsed = 0
        self.errors = 0

    def parse_file(self, filepath: Path) -> Dict[int, TRAEntry]:
        """
        Parse a TRA file and return dictionary of entries

        Args:
            filepath: Path to TRA file

        Returns:
            Dictionary mapping tra_id to TRAEntry
        """
        entries = {}
        self.entries_parsed = 0
        self.errors = 0

        logger.info(f"Parsing TRA file: {filepath}")

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.rstrip('\n')

                    # Skip empty lines
                    if not line.strip():
                        continue

                    # Try to parse entry
                    entry = self._parse_line(line, line_num)
                    if entry:
                        entries[entry.tra_id] = entry
                        self.entries_parsed += 1

        except Exception as e:
            logger.error(f"Error reading file {filepath}: {e}")
            raise

        logger.info(f"Parsed {self.entries_parsed} entries, {self.errors} errors")
        return entries

    def _parse_line(self, line: str, line_num: int) -> Optional[TRAEntry]:
        """
        Parse a single line from TRA file

        Args:
            line: Line text
            line_num: Line number (for error reporting)

        Returns:
            TRAEntry if parsed successfully, None otherwise
        """
        # Try to match entry pattern
        match = self.ENTRY_PATTERN.match(line)
        if match:
            tra_id = int(match.group(1))
            text = match.group(2)
            return TRAEntry(tra_id=tra_id, text=text)

        # If line starts with @ but doesn't match, it's an error
        if line.startswith('@'):
            logger.warning(f"Line {line_num}: Malformed entry: {line[:100]}")
            self.errors += 1

        return None

    def parse_japanese_variants(self, text: str) -> JapaneseTranslation:
        """
        Parse Japanese text with potential gender variants

        Japanese TRA files may contain gender variants in format:
        ~male version~ ~female version~

        Args:
            text: Japanese text (may contain gender variants)

        Returns:
            JapaneseTranslation object
        """
        # Check if text contains multiple tilde-separated parts
        parts = text.split('~')

        # Filter out empty parts
        parts = [p.strip() for p in parts if p.strip()]

        if len(parts) == 0:
            # Empty text
            return JapaneseTranslation(default=None, male=None, female=None)
        elif len(parts) == 1:
            # Single translation (no gender variant)
            return JapaneseTranslation(default=parts[0], male=None, female=None)
        elif len(parts) == 2:
            # Gender variants: first is male, second is female
            return JapaneseTranslation(default=None, male=parts[0], female=parts[1])
        else:
            # More than 2 parts - log warning and use first two
            logger.warning(f"Text has {len(parts)} parts, expected 1 or 2: {text[:100]}")
            return JapaneseTranslation(default=None, male=parts[0], female=parts[1])

    def parse_japanese_file(self, filepath: Path) -> Dict[int, JapaneseTranslation]:
        """
        Parse Japanese TRA file and extract gender variants

        Args:
            filepath: Path to Japanese TRA file

        Returns:
            Dictionary mapping tra_id to JapaneseTranslation
        """
        translations = {}
        self.entries_parsed = 0
        self.errors = 0

        logger.info(f"Parsing Japanese TRA file: {filepath}")

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.rstrip('\n')

                    # Skip empty lines
                    if not line.strip():
                        continue

                    # First try gender variant pattern
                    gender_match = self.GENDER_VARIANT_PATTERN.match(line)
                    if gender_match:
                        tra_id = int(gender_match.group(1))
                        male_text = gender_match.group(2).strip()
                        female_text = gender_match.group(3).strip()
                        translations[tra_id] = JapaneseTranslation(
                            default=None,
                            male=male_text if male_text else None,
                            female=female_text if female_text else None
                        )
                        self.entries_parsed += 1
                        continue

                    # Try standard entry pattern
                    match = self.ENTRY_PATTERN.match(line)
                    if match:
                        tra_id = int(match.group(1))
                        text = match.group(2)

                        # Parse for potential inline gender variants
                        translation = self.parse_japanese_variants(text)
                        translations[tra_id] = translation
                        self.entries_parsed += 1
                        continue

                    # If line starts with @ but doesn't match, it's an error
                    if line.startswith('@'):
                        logger.warning(f"Line {line_num}: Malformed entry: {line[:100]}")
                        self.errors += 1

        except Exception as e:
            logger.error(f"Error reading file {filepath}: {e}")
            raise

        logger.info(f"Parsed {self.entries_parsed} Japanese entries, {self.errors} errors")
        return translations

    @staticmethod
    def should_skip_entry(english_text: str, japanese_translation: JapaneseTranslation) -> bool:
        """
        Determine if entry should be skipped

        Args:
            english_text: English text
            japanese_translation: Japanese translation

        Returns:
            True if entry should be skipped
        """
        # Skip <NO TEXT> entries
        if english_text == '<NO TEXT>':
            return True

        # Skip placeholder entries
        if english_text.lower() == 'placeholder':
            return True

        # Skip if English is empty
        if not english_text.strip():
            return True

        # Skip if Japanese has no translation at all
        if not japanese_translation.has_any():
            return True

        # Skip test entries (single character or digit)
        if len(english_text.strip()) == 1 and english_text.strip().isdigit():
            return True

        return False
