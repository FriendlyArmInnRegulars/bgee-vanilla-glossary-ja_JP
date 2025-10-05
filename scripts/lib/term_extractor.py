"""
Term extraction for building frequency index
"""

import re
import logging
from typing import Dict, List, Set
from collections import Counter, defaultdict
from .models import GlossaryEntry, TermInfo

logger = logging.getLogger(__name__)


class TermExtractor:
    """Extract proper nouns and frequent phrases from glossary entries"""

    # English stopwords to exclude
    STOPWORDS = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
        'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
        'would', 'should', 'could', 'may', 'might', 'must', 'can', 'shall',
        'I', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her',
        'us', 'them', 'my', 'your', 'his', 'its', 'our', 'their', 'this',
        'that', 'these', 'those', 'what', 'which', 'who', 'when', 'where',
        'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most',
        'some', 'such', 'no', 'not', 'only', 'own', 'same', 'so', 'than',
        'too', 'very', 'just', 'now', 'if'
    }

    # Variable tags to ignore
    VARIABLE_PATTERN = re.compile(r'<[A-Z_]+>')

    # Sound reference pattern
    SOUND_PATTERN = re.compile(r'\[[A-Z0-9]+\]')

    def __init__(self, min_proper_noun_freq: int = 2, min_phrase_freq: int = 5):
        """
        Initialize term extractor

        Args:
            min_proper_noun_freq: Minimum frequency for proper nouns
            min_phrase_freq: Minimum frequency for phrases
        """
        self.min_proper_noun_freq = min_proper_noun_freq
        self.min_phrase_freq = min_phrase_freq

    def extract_proper_nouns(self, entries: List[GlossaryEntry]) -> Dict[str, TermInfo]:
        """
        Extract proper nouns (capitalized words) from entries

        Args:
            entries: List of glossary entries

        Returns:
            Dictionary of proper noun -> TermInfo
        """
        logger.info("Extracting proper nouns...")

        # Track all proper nouns and their translations
        proper_noun_data = defaultdict(lambda: {
            'count': 0,
            'translations': set(),
            'entries': []
        })

        for entry in entries:
            # Extract capitalized words from English text
            proper_nouns = self._extract_capitalized_words(entry.english)

            for noun in proper_nouns:
                # Skip if it's a stopword (capitalized at start of sentence)
                if noun.lower() in self.STOPWORDS:
                    continue

                # Find corresponding Japanese translation
                ja_translation = self._get_japanese_translation(entry, noun)

                if ja_translation:
                    proper_noun_data[noun]['count'] += 1
                    proper_noun_data[noun]['translations'].add(ja_translation)
                    proper_noun_data[noun]['entries'].append(entry.id)

        # Filter by minimum frequency and convert to TermInfo
        result = {}
        for noun, data in proper_noun_data.items():
            if data['count'] >= self.min_proper_noun_freq:
                result[noun] = TermInfo(
                    count=data['count'],
                    translations=sorted(list(data['translations'])),
                    entries=data['entries'][:10]  # Limit to first 10 examples
                )

        logger.info(f"Extracted {len(result)} proper nouns")
        return result

    def extract_frequent_phrases(self, entries: List[GlossaryEntry]) -> Dict[str, TermInfo]:
        """
        Extract frequently occurring short phrases

        Args:
            entries: List of glossary entries

        Returns:
            Dictionary of phrase -> TermInfo
        """
        logger.info("Extracting frequent phrases...")

        # Count all exact English phrases
        phrase_data = defaultdict(lambda: {
            'count': 0,
            'translations': set(),
            'entries': []
        })

        for entry in entries:
            # Clean text
            text = self._clean_text(entry.english)

            # Only consider short phrases (1-5 words, 3-50 characters)
            if 3 <= len(text) <= 50 and len(text.split()) <= 5:
                # Get Japanese translation
                ja_text = self._get_full_japanese(entry)

                if ja_text:
                    phrase_data[text]['count'] += 1
                    phrase_data[text]['translations'].add(ja_text)
                    phrase_data[text]['entries'].append(entry.id)

        # Filter by minimum frequency
        result = {}
        for phrase, data in phrase_data.items():
            if data['count'] >= self.min_phrase_freq:
                result[phrase] = TermInfo(
                    count=data['count'],
                    translations=sorted(list(data['translations'])),
                    entries=data['entries'][:10]
                )

        logger.info(f"Extracted {len(result)} frequent phrases")
        return result

    def build_term_frequency_index(
        self,
        entries: List[GlossaryEntry],
        extract_proper_nouns: bool = True,
        extract_phrases: bool = True
    ) -> Dict[str, TermInfo]:
        """
        Build complete term frequency index

        Args:
            entries: List of glossary entries
            extract_proper_nouns: Whether to extract proper nouns
            extract_phrases: Whether to extract frequent phrases

        Returns:
            Complete term frequency dictionary
        """
        logger.info(f"Building term frequency index for {len(entries)} entries...")

        term_frequency = {}

        if extract_proper_nouns:
            proper_nouns = self.extract_proper_nouns(entries)
            term_frequency.update(proper_nouns)

        if extract_phrases:
            phrases = self.extract_frequent_phrases(entries)
            term_frequency.update(phrases)

        logger.info(f"Total terms in index: {len(term_frequency)}")
        return term_frequency

    def _extract_capitalized_words(self, text: str) -> Set[str]:
        """
        Extract capitalized words from text

        Args:
            text: English text

        Returns:
            Set of capitalized words
        """
        # Remove variable tags and sound references
        text = self.VARIABLE_PATTERN.sub('', text)
        text = self.SOUND_PATTERN.sub('', text)

        # Find all capitalized words (at least 2 characters)
        # Match: "Word", "Word's", "O'Brien", etc.
        pattern = r'\b[A-Z][a-z\']+(?:[\s\-][A-Z][a-z\']+)*'
        matches = re.findall(pattern, text)

        # Clean up matches
        result = set()
        for match in matches:
            # Remove trailing punctuation
            match = match.rstrip(".,;:!?")
            if len(match) >= 2:
                result.add(match)

        return result

    def _get_japanese_translation(self, entry: GlossaryEntry, term: str) -> str:
        """
        Get Japanese translation for a specific English term in entry

        This is a simple heuristic - finds the term in English and
        returns the full Japanese translation.

        Args:
            entry: Glossary entry
            term: English term to find translation for

        Returns:
            Japanese translation or None
        """
        # Check if term appears in English text
        if term not in entry.english:
            return None

        # Return Japanese translation
        return self._get_full_japanese(entry)

    def _get_full_japanese(self, entry: GlossaryEntry) -> str:
        """
        Get full Japanese text from entry (handling gender variants)

        Args:
            entry: Glossary entry

        Returns:
            Japanese text
        """
        if entry.japanese.default:
            return entry.japanese.default
        elif entry.japanese.male:
            return entry.japanese.male
        elif entry.japanese.female:
            return entry.japanese.female
        return None

    def _clean_text(self, text: str) -> str:
        """
        Clean text by removing variable tags, sound references, etc.

        Args:
            text: Text to clean

        Returns:
            Cleaned text
        """
        # Remove variable tags
        text = self.VARIABLE_PATTERN.sub('', text)

        # Remove sound references
        text = self.SOUND_PATTERN.sub('', text)

        # Remove extra whitespace
        text = ' '.join(text.split())

        # Strip leading/trailing whitespace
        text = text.strip()

        return text

    def analyze_translation_consistency(
        self,
        term_frequency: Dict[str, TermInfo]
    ) -> List[Dict[str, any]]:
        """
        Analyze translation consistency - find terms with multiple translations

        Args:
            term_frequency: Term frequency dictionary

        Returns:
            List of inconsistencies
        """
        logger.info("Analyzing translation consistency...")

        inconsistencies = []

        for term, info in term_frequency.items():
            if len(info.translations) > 1:
                inconsistencies.append({
                    'term': term,
                    'count': info.count,
                    'translations': info.translations,
                    'num_translations': len(info.translations)
                })

        # Sort by count (most frequent first)
        inconsistencies.sort(key=lambda x: x['count'], reverse=True)

        logger.info(f"Found {len(inconsistencies)} terms with multiple translations")

        return inconsistencies
