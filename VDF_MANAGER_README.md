# VDF Configuration Manager

A Python tool for reading and writing Steam shortcut configurations from `localconfig.vdf` with JSON as the intermediate format for frontend integration.

## Overview

This tool allows you to:
- Extract Steam shortcut configurations to JSON format
- Modify shortcut settings (especially launch options) via JSON
- Write changes back to Steam's configuration files
- Create automatic backups before any modifications
- Restore from backups if needed

## Key Features

- **Safe Operations**: Automatically creates backups before any write operations
- **Steam Safety**: Prevents modifications while Steam is running
- **JSON Interface**: Clean JSON format for easy frontend integration
- **Essential Fields**: Focuses on the most important shortcut properties:
  - `appid` - Steam app ID for identification
  - `AppName` - Display name of the game/application
  - `LaunchOptions` - Launch parameters and command-line options
  - `Playtime` - Time played in minutes
  - `LastPlayed` - Timestamp of last play
  - `ResolutionOverride` - Custom resolution settings

## Installation

1. Ensure you have the required dependencies:
   ```bash
   pip install vdf
   ```

2. The tool is ready to use - no additional installation required.

## Usage

### Basic Commands

```bash
# Extract current shortcuts to JSON
python scripts/vdf_config_manager.py extract

# Create a manual backup
python scripts/vdf_config_manager.py backup

# Update configuration from JSON (Steam must be closed)
python scripts/vdf_config_manager.py update

# Restore from backup (Steam must be closed)
python scripts/vdf_config_manager.py restore --backup-path data/backups/localconfig_backup_YYYYMMDD_HHMMSS.vdf
```

### Workflow Example

1. **Extract current configuration:**
   ```bash
   python scripts/vdf_config_manager.py extract
   ```
   This creates `data/shortcuts_config.json` with your current shortcuts.

2. **Modify the JSON file:**
   Edit `data/shortcuts_config.json` to change launch options, resolution, etc.

3. **Close Steam:**
   Make sure Steam is completely closed before proceeding.

4. **Update configuration:**
   ```bash
   python scripts/vdf_config_manager.py update
   ```
   This will automatically create a backup and apply your changes.

5. **Start Steam:**
   Launch Steam to see your changes take effect.

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
    "ResolutionOverride": "1920x1080"
  }
}
```

### Field Descriptions

- **appid**: Steam's internal app ID (string format)
- **AppName**: Display name of the game/application
- **LaunchOptions**: Command-line parameters passed to the game
- **Playtime**: Total play time in minutes
- **LastPlayed**: Unix timestamp of last play session
- **ResolutionOverride**: Custom resolution (e.g., "1920x1080", "Native")

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

### App ID Mappings
The tool includes a mapping system for app IDs to human-readable names:

```python
self.app_id_mappings = {
    "3241660": "R.E.P.O.",
    # Add more mappings as needed
}
```

You can extend this mapping in the `VDFConfigManager` class to include more games.

### Steam User ID
By default, the tool uses Steam user ID `107256425`. To use a different user:

```bash
python scripts/vdf_config_manager.py extract --user-id YOUR_USER_ID
```

## File Locations

- **Source**: `~/.local/share/Steam/userdata/{USER_ID}/config/localconfig.vdf`
- **Output**: `data/shortcuts_config.json`
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
