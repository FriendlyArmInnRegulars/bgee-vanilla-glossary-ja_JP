"""
Glossary builder - creates glossary from parsed TRA entries
"""

import logging
from typing import Dict, List
from datetime import datetime
from .models import (
    TRAEntry, JapaneseTranslation, GlossaryEntry,
    EntryMetadata, GlossaryMetadata, Glossary, TermInfo
)
from .tra_parser import TRAParser

logger = logging.getLogger(__name__)


class GlossaryBuilder:
    """Builds glossary from English and Japanese TRA entries"""

    def __init__(self):
        self.parser = TRAParser()

    def build_from_entries(
        self,
        en_entries: Dict[int, TRAEntry],
        ja_translations: Dict[int, JapaneseTranslation],
        game: str
    ) -> List[GlossaryEntry]:
        """
        Build glossary entries from English and Japanese TRA data

        Args:
            en_entries: English TRA entries (tra_id -> TRAEntry)
            ja_translations: Japanese translations (tra_id -> JapaneseTranslation)
            game: Game identifier (bg1ee or bg2ee)

        Returns:
            List of GlossaryEntry objects
        """
        glossary_entries = []
        skipped = 0

        logger.info(f"Building glossary for {game}")
        logger.info(f"English entries: {len(en_entries)}")
        logger.info(f"Japanese entries: {len(ja_translations)}")

        # Iterate through all English entries
        for tra_id, en_entry in en_entries.items():
            # Find matching Japanese translation
            ja_translation = ja_translations.get(tra_id)

            # If no Japanese translation found, create empty one
            if ja_translation is None:
                ja_translation = JapaneseTranslation(default=None, male=None, female=None)

            # Check if entry should be skipped
            if self.parser.should_skip_entry(en_entry.text, ja_translation):
                skipped += 1
                continue

            # Create entry ID
            entry_id = f"{game}:{tra_id}"

            # Create metadata
            metadata = EntryMetadata.create(
                game=game,
                tra_id=tra_id,
                english=en_entry.text,
                japanese=ja_translation
            )

            # Create glossary entry
            entry = GlossaryEntry(
                id=entry_id,
                english=en_entry.text,
                japanese=ja_translation,
                metadata=metadata
            )

            glossary_entries.append(entry)

        logger.info(f"Created {len(glossary_entries)} glossary entries, skipped {skipped}")
        return glossary_entries

    def build_metadata(
        self,
        entries: List[GlossaryEntry],
        source_games: List[str]
    ) -> GlossaryMetadata:
        """
        Build metadata for glossary

        Args:
            entries: List of glossary entries
            source_games: List of source games

        Returns:
            GlossaryMetadata object
        """
        # Calculate statistics per game
        statistics = {}
        for game in source_games:
            game_entries = [e for e in entries if e.metadata.game == game]

            # Count entries with translation
            with_translation = sum(
                1 for e in game_entries
                if e.japanese.has_any()
            )

            # Count entries with gender variant
            with_gender_variant = sum(
                1 for e in game_entries
                if e.japanese.male is not None or e.japanese.female is not None
            )

            statistics[game] = {
                'total': len(game_entries),
                'with_translation': with_translation,
                'with_gender_variant': with_gender_variant
            }

        # Create metadata
        metadata = GlossaryMetadata(
            version="1.0",
            generated_at=datetime.utcnow().isoformat() + 'Z',
            source_games=source_games,
            total_entries=len(entries),
            statistics=statistics
        )

        return metadata

    def build_glossary(
        self,
        entries: List[GlossaryEntry],
        source_games: List[str],
        extract_terms: bool = False
    ) -> Glossary:
        """
        Build complete glossary

        Args:
            entries: List of glossary entries
            source_games: List of source games
            extract_terms: Whether to extract term frequency (Phase 3)

        Returns:
            Complete Glossary object
        """
        # Build metadata
        metadata = self.build_metadata(entries, source_games)

        # Term frequency (placeholder for now)
        term_frequency = {}

        if extract_terms:
            # TODO: Implement term extraction (Phase 3)
            logger.info("Term extraction not yet implemented")

        return Glossary(
            metadata=metadata,
            entries=entries,
            term_frequency=term_frequency
        )
