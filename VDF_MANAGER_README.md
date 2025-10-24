# Enhanced VDF Configuration Manager

A comprehensive Python tool for reading and writing **all** Steam game configurations from `localconfig.vdf` with dynamic game name resolution and JSON as the intermediate format for frontend integration.

## Overview

This enhanced tool allows you to:
- Extract **all** Steam game configurations (not just shortcuts) to JSON format
- **Dynamic game name resolution** using multiple fallback methods
- Modify game settings (launch options, resolution, etc.) via JSON
- Write changes back to Steam's configuration files
- Create automatic backups before any modifications
- Restore from backups if needed
- **Caching system** for improved performance
- **System app filtering** (Proton, Steam Runtime, etc.)

## Key Features

- **Dynamic Game Name Resolution**: Automatically discovers game names using multiple fallback methods
- **Comprehensive Extraction**: Extracts ALL games, not just those with launch options
- **Safe Operations**: Automatically creates backups before any write operations
- **Steam Safety**: Prevents modifications while Steam is running
- **JSON Interface**: Clean JSON format for easy frontend integration
- **Caching System**: Improves performance with app ID → name mapping cache
- **System App Filtering**: Optionally exclude Proton, Steam Runtime, etc.
- **Essential Fields**: Extracts the most important game properties:
  - `appid` - Steam app ID for identification
  - `AppName` - Display name of the game/application (dynamically resolved)
  - `LaunchOptions` - Launch parameters and command-line options
  - `Playtime` - Time played in minutes
  - `LastPlayed` - Timestamp of last play
  - `ResolutionOverride` - Custom resolution settings
  - `Exe`, `StartDir` - Executable path and start directory (for non-Steam games)

## Installation

1. Ensure you have the required dependencies:
   ```bash
   pip install vdf
   ```

2. The tool is ready to use - no additional installation required.

## Usage

### Basic Commands

```bash
# Extract shortcuts (games with launch options) to JSON
python scripts/vdf_config_manager.py extract

# Extract ALL games to JSON (recommended)
python scripts/vdf_config_manager.py extract-all

# Extract all games including system apps (Proton, Steam Runtime, etc.)
python scripts/vdf_config_manager.py extract-all --include-system

# Refresh app name cache
python scripts/vdf_config_manager.py refresh-cache

# Create a manual backup
python scripts/vdf_config_manager.py backup

# Update configuration from JSON (Steam must be closed)
python scripts/vdf_config_manager.py update

# Restore from backup (Steam must be closed)
python scripts/vdf_config_manager.py restore --backup-path data/backups/localconfig_backup_YYYYMMDD_HHMMSS.vdf
```

### Workflow Example

1. **Extract all games:**
   ```bash
   python scripts/vdf_config_manager.py extract-all
   ```
   This creates `data/all_games_config.json` with all your games and their configurations.

2. **Modify the JSON file:**
   Edit `data/all_games_config.json` to change launch options, resolution, etc.

3. **Close Steam:**
   Make sure Steam is completely closed before proceeding.

4. **Update configuration:**
   ```bash
   python scripts/vdf_config_manager.py update
   ```
   This will automatically create a backup and apply your changes.

5. **Start Steam:**
   Launch Steam to see your changes take effect.

## Dynamic Game Name Resolution

The tool uses a sophisticated multi-fallback system to resolve app IDs to human-readable game names:

### Fallback Methods (in order):

1. **App Manifests** (Primary) - Fast, clean data for installed Steam games
   - Parses `.acf` files in `/steamapps/appmanifest_*.acf`
   - Extracts `"name"` field for each app ID
   - Works for all installed Steam games

2. **Library Cache** (Fallback 1) - Works for both Steam and non-Steam games
   - Parses JSON files in `/config/librarycache/*.json`
   - Extracts game metadata and descriptions
   - Available for games with cached data

3. **shortcuts.vdf** (Fallback 2) - Legacy data source
   - Parses binary VDF for non-Steam game names
   - Matches by launch options and other criteria
   - Used for non-Steam games

4. **Manual Mappings** (Fallback 3) - Configurable custom mappings
   - Hardcoded dictionary for games not found in other sources
   - Easily extensible for custom games
   - Final fallback before generic naming

5. **Generic Naming** (Final Fallback)
   - Uses format `"App {APP_ID}"` for unknown games
   - Ensures every game has a name

### Caching System

- App ID → name mappings are cached in `data/app_name_cache.json`
- Improves performance on subsequent runs
- Automatically refreshed when new games are discovered
- Use `refresh-cache` command to force refresh

## JSON Format

The extracted JSON has the following structure:

```json
{
  "3241660": {
    "appid": "3241660",
    "AppName": "R.E.P.O.",
    "LaunchOptions": "%command% --doorstop-enable true --doorstop-target \"/path/to/mod.dll\" --r2profile \"ProfileName\"",
    "Playtime": "9520",
    "LastPlayed": "1761018554",
    "ResolutionOverride": "1920x1080",
    "ResolutionOverrideInternalDisplay": "0",
    "Exe": "/path/to/game.exe",
    "StartDir": "/path/to/game/directory"
  },
  "1245620": {
    "appid": "1245620",
    "AppName": "ELDEN RING",
    "LaunchOptions": "",
    "Playtime": "3146",
    "LastPlayed": "1716275847",
    "ResolutionOverride": "",
    "ResolutionOverrideInternalDisplay": "0"
  }
}
```

### Field Descriptions

- **appid**: Steam's internal app ID (string format)
- **AppName**: Display name of the game/application (dynamically resolved)
- **LaunchOptions**: Command-line parameters passed to the game
- **Playtime**: Total play time in minutes
- **LastPlayed**: Unix timestamp of last play session
- **ResolutionOverride**: Custom resolution (e.g., "1920x1080", "Native")
- **ResolutionOverrideInternalDisplay**: Internal display resolution override
- **Exe**: Executable path (for non-Steam games)
- **StartDir**: Start directory (for non-Steam games)

## Safety Features

### Automatic Backups
- Every write operation creates a timestamped backup
- Backups are stored in `data/backups/`
- Format: `localconfig_backup_YYYYMMDD_HHMMSS.vdf`

### Steam Process Detection
- Tool checks if Steam is running before any write operations
- Prevents corruption by blocking updates while Steam is active
- Clear error messages guide you to close Steam first

### Validation
- JSON structure validation before applying changes
- Preserves all non-shortcut data in VDF files
- Graceful error handling with rollback instructions

## Configuration

### Manual App ID Mappings
The tool includes a mapping system for app IDs to human-readable names in the `GameNameResolver` class:

```python
self.manual_mappings = {
    "3241660": "R.E.P.O.",
    # Add more mappings as needed
}
```

You can extend this mapping in the `GameNameResolver` class to include more games that aren't found through other methods.

### System App Filtering
The tool can filter out system applications:

```python
self.system_apps = {
    "steam linux runtime", "proton", "steamworks", "steam client"
}
```

Use the `--include-system` flag to include these in extraction.

### Steam User ID
By default, the tool uses Steam user ID `107256425`. To use a different user:

```bash
python scripts/vdf_config_manager.py extract --user-id YOUR_USER_ID
```

## File Locations

- **Source**: `~/.local/share/Steam/userdata/{USER_ID}/config/localconfig.vdf`
- **App Manifests**: `~/.local/share/Steam/steamapps/appmanifest_*.acf`
- **Library Cache**: `~/.local/share/Steam/userdata/{USER_ID}/config/librarycache/*.json`
- **Output**: `data/all_games_config.json`
- **Cache**: `data/app_name_cache.json`
- **Backups**: `data/backups/localconfig_backup_*.vdf`

## Troubleshooting

### Common Issues

1. **"Steam is currently running" error:**
   - Close Steam completely before running update/restore commands
   - Use `pgrep -f steam` to verify no Steam processes are running

2. **"localconfig.vdf not found" error:**
   - Verify your Steam user ID is correct
   - Check that Steam is installed in the default location

3. **"Could not read shortcuts.vdf" warning:**
   - This is normal for some configurations
   - The tool will use app ID mappings as fallback

4. **JSON parsing errors:**
   - Validate your JSON syntax before running update
   - Use a JSON validator to check your modifications

### Recovery

If something goes wrong:

1. **Restore from backup:**
   ```bash
   python scripts/vdf_config_manager.py restore --backup-path data/backups/localconfig_backup_YYYYMMDD_HHMMSS.vdf
   ```

2. **Steam Cloud restore:**
   - Steam may automatically restore from cloud backup
   - Check Steam settings for cloud synchronization

3. **Manual restore:**
   - Copy a backup file over `localconfig.vdf`
   - Restart Steam

## Technical Details

### VDF Format
- `localconfig.vdf` is a plain text VDF (Valve Data Format) file
- Contains all Steam configuration data in a nested structure
- Shortcuts are stored under `UserLocalConfigStore.Software.Valve.Steam.apps`

### App ID System
- Steam converts non-Steam games to regular app entries
- Each app gets a unique positive integer ID
- Launch options are stored in the main apps section

### Parsing Strategy
1. Parse `localconfig.vdf` as text VDF
2. Navigate to the apps section
3. Find apps with `LaunchOptions` (likely non-Steam games)
4. Cross-reference with `shortcuts.vdf` for additional metadata
5. Use app ID mappings for human-readable names

## Contributing

To extend the tool:

1. **Add new app mappings** in the `app_id_mappings` dictionary
2. **Extend field extraction** in the `extract_shortcuts` method
3. **Add new CLI commands** in the `main` function
4. **Improve error handling** throughout the codebase

## License

This tool is part of the Steam Config Analyzer project. Use at your own risk and always backup your Steam configuration before making changes.
