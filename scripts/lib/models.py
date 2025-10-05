"""
Data models for BG:EE Glossary Generator
"""

from dataclasses import dataclass, asdict
from typing import Optional, Dict, List
import re


@dataclass
class TRAEntry:
    """Single TRA file entry"""
    tra_id: int
    text: str

    def __str__(self) -> str:
        return f"@{self.tra_id} = ~{self.text}~"


@dataclass
class JapaneseTranslation:
    """Japanese translation with gender variants"""
    default: Optional[str] = None
    male: Optional[str] = None
    female: Optional[str] = None

    def has_any(self) -> bool:
        """Check if any translation exists"""
        return any([self.default, self.male, self.female])

    def to_dict(self) -> Dict[str, Optional[str]]:
        return asdict(self)


@dataclass
class EntryMetadata:
    """Metadata for glossary entry"""
    game: str
    tra_id: int
    has_variables: bool
    has_sound_ref: bool
    char_count_en: int
    char_count_ja: int

    def to_dict(self) -> Dict:
        return asdict(self)

    @staticmethod
    def create(game: str, tra_id: int, english: str, japanese: JapaneseTranslation) -> 'EntryMetadata':
        """Create metadata from entry data"""
        # Detect variables like <CHARNAME>, <SIRMAAM>
        has_variables = bool(re.search(r'<[A-Z_]+>', english))

        # Detect sound references like [ZOMBI01]
        has_sound_ref = bool(re.search(r'\[[A-Z0-9]+\]', english))

        # Count characters
        char_count_en = len(english)

        # For Japanese, use the longest variant
        ja_texts = [japanese.default, japanese.male, japanese.female]
        ja_texts = [t for t in ja_texts if t]
        char_count_ja = max([len(t) for t in ja_texts]) if ja_texts else 0

        return EntryMetadata(
            game=game,
            tra_id=tra_id,
            has_variables=has_variables,
            has_sound_ref=has_sound_ref,
            char_count_en=char_count_en,
            char_count_ja=char_count_ja
        )


@dataclass
class GlossaryEntry:
    """Single glossary entry with English-Japanese pair"""
    id: str
    english: str
    japanese: JapaneseTranslation
    metadata: EntryMetadata

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'english': self.english,
            'japanese': self.japanese.to_dict(),
            'metadata': self.metadata.to_dict()
        }


@dataclass
class TermInfo:
    """Term frequency information"""
    count: int
    translations: List[str]
    entries: List[str]

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class GlossaryMetadata:
    """Metadata for entire glossary"""
    version: str
    generated_at: str
    source_games: List[str]
    total_entries: int
    statistics: Dict[str, Dict[str, int]]

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class Glossary:
    """Complete glossary structure"""
    metadata: GlossaryMetadata
    entries: List[GlossaryEntry]
    term_frequency: Dict[str, TermInfo]

    def to_dict(self) -> Dict:
        return {
            'metadata': self.metadata.to_dict(),
            'entries': [e.to_dict() for e in self.entries],
            'term_frequency': {k: v.to_dict() for k, v in self.term_frequency.items()}
        }
