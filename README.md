# Steam Config Analyzer

A Python tool for analyzing and parsing Steam configuration files, specifically focused on understanding the relationship between `shortcuts.vdf` and `localconfig.vdf` files.

## Overview

This project was created to investigate and document how Steam stores configuration data, particularly for non-Steam game shortcuts. Through analysis, we discovered that Steam uses a dual-file system:

- **`shortcuts.vdf`** - Contains only non-Steam game shortcuts (binary format)
- **`localconfig.vdf`** - Contains ALL Steam configuration data, including shortcuts for both Steam and non-Steam games

## Key Findings

### Steam Configuration Architecture

1. **`localconfig.vdf`** is the master configuration file containing:
   - Settings for all Steam games
   - Settings for non-Steam games (shortcuts)
   - User preferences and UI settings
   - Launch options for everything

2. **`shortcuts.vdf`** is a legacy/backup file containing:
   - Only non-Steam game shortcuts
   - May not always reflect current state
   - Used primarily for non-Steam game management

### The REPO Case Study

During our investigation, we discovered that REPO appeared in both files with different configurations:

- **`shortcuts.vdf`**: Old "Kat" profile (outdated)
- **`localconfig.vdf`**: Current "Friends" profile (up-to-date)

This revealed that `localconfig.vdf` is the source of truth for current configurations.

## Project Structure

```
steam-config-analyzer/
├── scripts/           # Python analysis scripts
├── data/             # Sample data and outputs
├── docs/             # Documentation
├── venv/             # Python virtual environment
└── README.md         # This file
```

## Scripts

- **`parse_shortcuts.py`** - Parses `shortcuts.vdf` using the vdf library
- **`parse_localconfig.py`** - Attempts to parse `localconfig.vdf` (has parsing issues)
- **`parse_current_shortcuts.py`** - Extracts shortcuts from `localconfig.vdf`
- **`extract_shortcuts_from_text.py`** - Manual extraction of current shortcuts data

## Requirements

- Python 3.13+
- vdf library (`pip install vdf`)

## Usage

1. Clone or download this project
2. Set up the virtual environment:
   ```bash
   cd steam-config-analyzer
   source venv/bin/activate
   ```
3. Run the analysis scripts:
   ```bash
   cd scripts
   python3 parse_shortcuts.py
   ```

## Data Files

- **`shortcuts_parsed.json`** - Parsed output from `shortcuts.vdf`
- **`current_shortcuts_updated.json`** - Current shortcuts data with "Friends" profile

## Documentation

See the `docs/` directory for detailed findings and analysis.

## Notes

- The `localconfig.vdf` file uses a different format that the vdf library struggles to parse
- Current shortcuts data can be extracted using text-based methods
- Steam appears to prioritize `localconfig.vdf` over `shortcuts.vdf` for current configurations
