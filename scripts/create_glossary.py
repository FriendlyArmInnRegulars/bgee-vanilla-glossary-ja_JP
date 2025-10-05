#!/usr/bin/env python3
"""
BG:EE Glossary Generator - Main script

Generates Japanese translation glossary from BG1EE and BG2EE TRA files
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import List

# Add lib directory to path
sys.path.insert(0, str(Path(__file__).parent))

from lib.tra_parser import TRAParser
from lib.glossary_builder import GlossaryBuilder
from lib.models import GlossaryEntry

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_game_tra_files(
    source_dir: Path,
    game: str,
    parser: TRAParser
) -> List[GlossaryEntry]:
    """
    Parse TRA files for a specific game

    Args:
        source_dir: Root source_tra directory
        game: Game identifier (bg1ee or bg2ee)
        parser: TRAParser instance

    Returns:
        List of GlossaryEntry objects
    """
    game_dir = source_dir / game

    # Define file paths
    en_file = game_dir / 'en_US' / 'dialog.tra'
    ja_file = game_dir / 'ja_JP' / 'dialog.tra'

    # Check files exist
    if not en_file.exists():
        logger.error(f"English TRA file not found: {en_file}")
        return []

    if not ja_file.exists():
        logger.error(f"Japanese TRA file not found: {ja_file}")
        return []

    # Parse English entries
    logger.info(f"Parsing {game} English TRA file...")
    en_entries = parser.parse_file(en_file)

    # Parse Japanese translations
    logger.info(f"Parsing {game} Japanese TRA file...")
    ja_translations = parser.parse_japanese_file(ja_file)

    # Build glossary entries
    builder = GlossaryBuilder()
    entries = builder.build_from_entries(en_entries, ja_translations, game)

    return entries


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Generate Japanese translation glossary from BG:EE TRA files'
    )
    parser.add_argument(
        '--games',
        nargs='+',
        choices=['bg1ee', 'bg2ee', 'all'],
        default=['all'],
        help='Games to process (default: all)'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('../glossary.json'),
        help='Output JSON file path (default: ../glossary.json)'
    )
    parser.add_argument(
        '--source-dir',
        type=Path,
        default=Path('../source_tra'),
        help='Source TRA directory (default: ../source_tra)'
    )
    parser.add_argument(
        '--include-stats',
        action='store_true',
        help='Include detailed statistics in output'
    )
    parser.add_argument(
        '--extract-terms',
        action='store_true',
        help='Extract term frequency (Phase 3 feature)'
    )
    parser.add_argument(
        '--indent',
        type=int,
        default=2,
        help='JSON indentation (default: 2)'
    )

    args = parser.parse_args()

    # Determine which games to process
    if 'all' in args.games:
        games = ['bg1ee', 'bg2ee']
    else:
        games = args.games

    # Make paths absolute relative to script location
    script_dir = Path(__file__).parent
    source_dir = (script_dir / args.source_dir).resolve()
    output_file = (script_dir / args.output).resolve()

    logger.info(f"BG:EE Glossary Generator")
    logger.info(f"Source directory: {source_dir}")
    logger.info(f"Output file: {output_file}")
    logger.info(f"Games to process: {games}")

    # Check source directory exists
    if not source_dir.exists():
        logger.error(f"Source directory not found: {source_dir}")
        sys.exit(1)

    # Parse TRA files
    tra_parser = TRAParser()
    all_entries = []

    for game in games:
        logger.info(f"\n{'='*60}")
        logger.info(f"Processing {game.upper()}")
        logger.info(f"{'='*60}")

        entries = parse_game_tra_files(source_dir, game, tra_parser)
        all_entries.extend(entries)

        logger.info(f"✓ {game.upper()}: {len(entries)} entries")

    # Build complete glossary
    logger.info(f"\n{'='*60}")
    logger.info(f"Building final glossary")
    logger.info(f"{'='*60}")

    builder = GlossaryBuilder()
    glossary = builder.build_glossary(
        entries=all_entries,
        source_games=games,
        extract_terms=args.extract_terms
    )

    # Convert to dictionary
    glossary_dict = glossary.to_dict()

    # Remove statistics if not requested
    if not args.include_stats:
        if 'statistics' in glossary_dict['metadata']:
            del glossary_dict['metadata']['statistics']

    # Write JSON output
    logger.info(f"\nWriting glossary to: {output_file}")

    try:
        # Create output directory if needed
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(glossary_dict, f, ensure_ascii=False, indent=args.indent)

        logger.info(f"✓ Successfully wrote {len(all_entries)} entries to {output_file}")

        # Print summary
        print(f"\n{'='*60}")
        print(f"Glossary Generation Complete")
        print(f"{'='*60}")
        print(f"Total entries: {len(all_entries)}")
        print(f"Output file: {output_file}")
        print(f"File size: {output_file.stat().st_size / 1024 / 1024:.2f} MB")
        print(f"{'='*60}\n")

    except Exception as e:
        logger.error(f"Error writing output file: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
