# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Japanese glossary repository for Baldur's Gate: Enhanced Edition (BG1EE and BG2EE) translation modding. The project extracts and manages translation pairs from TRA (translation) files used in the Infinity Engine games.

## Repository Structure

```
source_tra/
├── bg1ee/
│   ├── en_US/          # English TRA files for BG1EE
│   │   └── dialog.tra  # ~50K lines
│   └── ja_JP/          # Japanese TRA files for BG1EE
│       └── dialog.tra  # ~54K lines
└── bg2ee/
    ├── en_US/          # English TRA files for BG2EE
    │   └── dialog.tra  # ~128K lines
    └── ja_JP/          # Japanese TRA files for BG2EE
        └── dialog.tra  # ~129K lines
```

## TRA File Format

TRA files use the Infinity Engine translation format:
- Each entry starts with `@<number>` (e.g., `@0`, `@1`, `@2`)
- Followed by `= ~<text>~`
- Text is enclosed in tildes (`~`)
- The `@<number>` ID matches between English and Japanese files
- Some Japanese translations include gender variants separated by `~` (e.g., `~male version~ ~female version~`)

Example:
```
@1 = ~Why hast thou disturbed me here?~
```

## Key Characteristics

- **Language pairs**: English (en_US) and Japanese (ja_JP) are paired by matching `@ID` numbers
- **Two game versions**: BG1EE (smaller dataset) and BG2EE (larger dataset)
- **Gender-aware translations**: Japanese translations may contain male/female variants
- **No build system**: This is a data repository, no compilation required
- **No scripts yet**: The repository is currently in planning phase (see [memo.md](memo.md) for planned architecture)

## Planned Architecture (from memo.md)

The memo.md outlines a planned structure:
- `glossary.json`: Main output file with structured translation data (English → Japanese mapping with metadata)
- `scripts/`: Python scripts to generate glossary from TRA files
  - `create_glossary.py`: Main script to parse TRA files and create glossary
  - `tra_parser.py`: TRA file parsing library
- `docs/`: Documentation (CONTRIBUTING.md, glossary_format.md)

## Working with TRA Files

When reading TRA files:
- IDs are sequential but may have gaps
- Match entries by `@ID` across language pairs
- Text content is between `~` delimiters
- Handle multi-line entries (though most are single-line)
- Special entry `@0 = ~<NO TEXT>~` represents empty/placeholder text

## Data Scale

- BG1EE: ~50K English lines, ~54K Japanese lines
- BG2EE: ~128K English lines, ~129K Japanese lines
- Total: ~178K translation pairs across both games
