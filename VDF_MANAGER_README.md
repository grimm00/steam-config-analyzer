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

# Extract with different modes
python scripts/vdf_config_manager.py extract-all --mode=sparse      # Only existing fields (default)
python scripts/vdf_config_manager.py extract-all --mode=standard   # All fields with defaults

# Extract with additional options
python scripts/vdf_config_manager.py extract-all --include-system    # Include system apps
python scripts/vdf_config_manager.py extract-all --include-managed   # Include Steam-managed fields

# Combined options
python scripts/vdf_config_manager.py extract-all --mode=sparse --include-managed

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

## Updating Game Configurations

### Complete Update Workflow

The update process allows you to modify game settings by editing the JSON file and applying changes back to Steam's configuration.

**Step-by-Step Process:**

1. **Extract Current Configuration**
   ```bash
   python scripts/vdf_config_manager.py extract-all --mode=sparse
   ```

2. **Edit JSON File**
   - Open `data/all_games_config.json`
   - Modify the fields you want to change
   - Save the file

3. **Validate Changes**
   - Review your modifications carefully
   - Ensure JSON syntax is valid
   - Check that you're only modifying safe fields

4. **Close Steam Completely**
   - Exit Steam application
   - Verify no Steam processes are running
   - The tool will check this automatically

5. **Run Update Command**
   ```bash
   python scripts/vdf_config_manager.py update
   ```

6. **Verify Backup**
   - Check that backup was created in `data/backups/`
   - Note the backup filename for potential rollback

7. **Start Steam and Test**
   - Launch Steam
   - Verify your changes are applied
   - Test the modified games

### JSON Editing Guide

**Field Modification Syntax:**

- **Modify existing field**: Change the value in the JSON
- **Add new field**: Include the field in the JSON with your desired value
- **Delete field**: Set the field to `null` or `""` (empty string)
- **Preserve field**: Don't include the field in the JSON (will remain unchanged)

**Practical Examples:**

**Example 1: Update Launch Options**
```json
{
  "3241660": {
    "appid": "3241660",
    "AppName": "R.E.P.O.",
    "LaunchOptions": "%command% --new-profile \"Friends2\""
  }
}
```

**Example 2: Change Resolution**
```json
{
  "1245620": {
    "appid": "1245620",
    "AppName": "ELDEN RING",
    "ResolutionOverride": "2560x1440"
  }
}
```

**Example 3: Remove Launch Options**
```json
{
  "3241660": {
    "appid": "3241660",
    "AppName": "R.E.P.O.",
    "LaunchOptions": ""
  }
}
```

**Example 4: Bulk Update Multiple Games**
```json
{
  "3241660": {
    "appid": "3241660",
    "AppName": "R.E.P.O.",
    "ResolutionOverride": "1920x1080"
  },
  "1245620": {
    "appid": "1245620",
    "AppName": "ELDEN RING",
    "ResolutionOverride": "2560x1440"
  }
}
```

**Example 5: Remove All Launch Options**
```json
{
  "3241660": {
    "appid": "3241660",
    "AppName": "R.E.P.O.",
    "LaunchOptions": null
  }
}
```

**Example 6: Set Native Resolution**
```json
{
  "1245620": {
    "appid": "1245620",
    "AppName": "ELDEN RING",
    "ResolutionOverride": "Native"
  }
}
```

### Real-World Usage Scenarios

**Scenario 1: Modding a Game**
```bash
# 1. Extract current config
python scripts/vdf_config_manager.py extract-all --mode=sparse

# 2. Edit data/all_games_config.json to add mod launcher
{
  "3241660": {
    "appid": "3241660",
    "AppName": "R.E.P.O.",
    "LaunchOptions": "%command% --doorstop-enable true --doorstop-target \"/home/deck/Mods/BepInEx/core/BepInEx.dll\""
  }
}

# 3. Close Steam and update
python scripts/vdf_config_manager.py update
```

**Scenario 2: Performance Optimization**
```bash
# 1. Extract all games
python scripts/vdf_config_manager.py extract-all --mode=standard

# 2. Set consistent resolution for multiple games
{
  "1245620": {"appid": "1245620", "AppName": "ELDEN RING", "ResolutionOverride": "1920x1080"},
  "1174180": {"appid": "1174180", "AppName": "Red Dead Redemption 2", "ResolutionOverride": "1920x1080"},
  "271590": {"appid": "271590", "AppName": "Grand Theft Auto V", "ResolutionOverride": "1920x1080"}
}

# 3. Apply changes
python scripts/vdf_config_manager.py update
```

**Scenario 3: Clean Up Old Settings**
```bash
# 1. Extract current config
python scripts/vdf_config_manager.py extract-all --mode=sparse

# 2. Remove launch options from games that no longer need them
{
  "3241660": {
    "appid": "3241660",
    "AppName": "R.E.P.O.",
    "LaunchOptions": ""  # This will delete the field
  }
}

# 3. Apply cleanup
python scripts/vdf_config_manager.py update
```

### Update Command Details

**Command Syntax:**
```bash
python scripts/vdf_config_manager.py update [--user-id USER_ID]
```

**What the Update Command Does:**

1. **Reads Configuration**: Loads `data/all_games_config.json`
2. **Creates Backup**: Automatically backs up `localconfig.vdf` with timestamp
3. **Validates Changes**: Checks for safe fields and warns about dangerous ones
4. **Applies Modifications**: Updates `localconfig.vdf` with your changes
5. **Shows Detailed Log**: Displays exactly what was changed

**Example Output:**
```
Updating localconfig.vdf with JSON data...
Backup created: data/backups/localconfig_backup_20251023_143022.vdf
Updated LaunchOptions for app 3241660
Updated ResolutionOverride for app 1245620
Removed empty field PlaytimeDisconnected from app 7
Successfully updated localconfig.vdf
Backup available at: data/backups/localconfig_backup_20251023_143022.vdf
```

### Field Reference

**LaunchOptions**
- **Purpose**: Command-line parameters passed to the game
- **Format**: String with parameters
- **Examples**: 
  - `"%command% --fullscreen --width 1920"`
  - `"%command% --doorstop-enable true --doorstop-target \"/path/to/mod.dll\""`
- **Notes**: Always start with `%command%` for non-Steam games

**ResolutionOverride**
- **Purpose**: Force a specific resolution for the game
- **Format**: "WIDTHxHEIGHT" or "Native"
- **Examples**: 
  - `"1920x1080"`
  - `"2560x1440"`
  - `"Native"`
- **Notes**: Use "Native" to let the game choose its own resolution

**ResolutionOverrideInternalDisplay**
- **Purpose**: Internal display override setting
- **Format**: "0" (disabled) or "1" (enabled)
- **Common Value**: Usually "0"
- **Notes**: Rarely needs to be changed

**PlaytimeDisconnected**
- **Purpose**: Track playtime while disconnected from Steam
- **Format**: Number (minutes)
- **Notes**: Usually managed by Steam automatically

### Safety Guidelines

**Before Running Update:**

1. ✓ **Close Steam Completely**
   - Exit the Steam application
   - Check that no Steam processes are running
   - The tool will prevent updates if Steam is running

2. ✓ **Review JSON Changes Carefully**
   - Double-check the app IDs you're modifying
   - Verify the field values are correct
   - Ensure JSON syntax is valid

3. ✓ **Verify Backup Directory**
   - Check that `data/backups/` directory exists
   - The tool creates automatic backups, but verify the location

4. ✓ **Only Modify Safe User Fields**
   - Stick to: LaunchOptions, ResolutionOverride, ResolutionOverrideInternalDisplay
   - Avoid: cloud, autocloud, BadgeData, EULA fields

5. ✓ **Don't Edit Steam-Managed Fields**
   - These are automatically skipped with warnings
   - Modifying them could cause Steam issues

**What Gets Updated:**

- ✓ **LaunchOptions** - Safe to modify
- ✓ **ResolutionOverride** - Safe to modify  
- ✓ **ResolutionOverrideInternalDisplay** - Safe to modify
- ✓ **PlaytimeDisconnected** - Safe to modify
- ✗ **cloud, autocloud, BadgeData** - Skipped for safety
- ✗ **EULA fields** - Skipped for safety
- ✗ **appid, AppName** - Tool-managed, skipped

### Troubleshooting

**Common Issues and Solutions:**

**"Steam is currently running" Error**
- **Problem**: Steam is still running
- **Solution**: Close Steam completely and try again
- **Check**: Run `pgrep -f steam` to verify no processes

**"App ID not found" Warning**
- **Problem**: The app ID in JSON doesn't exist in localconfig.vdf
- **Solution**: Check the app ID is correct, or the game was uninstalled
- **Check**: Verify with `extract-all` command

**"Field skipped for safety" Warning**
- **Problem**: You tried to modify a Steam-managed field
- **Solution**: Remove the field from JSON or use `--include-managed` flag
- **Note**: This is normal behavior for cloud, autocloud, BadgeData fields

**JSON Parse Errors**
- **Problem**: Invalid JSON syntax in the file
- **Solution**: Validate JSON syntax using an online validator
- **Check**: Look for missing commas, quotes, or brackets

**"Backup creation failed" Error**
- **Problem**: Cannot create backup file
- **Solution**: Check write permissions in `data/backups/` directory
- **Check**: Ensure directory exists and is writable

**Changes Not Applied**
- **Problem**: Updates didn't take effect in Steam
- **Solution**: Restart Steam completely, verify backup was created
- **Check**: Use backup to restore if needed

**Field Deletion Not Working**
- **Problem**: Empty string `""` not removing field
- **Solution**: Use `null` instead of `""` for explicit deletion
- **Note**: Empty strings remove fields, `null` explicitly deletes them

### Logic Review and Important Notes

**Field Deletion Behavior:**
The tool handles field deletion in two ways:
- **`null` values**: Explicitly delete the field from localconfig.vdf
- **Empty strings `""`**: Also delete the field (same as null)
- **Missing fields**: Preserve existing values (don't modify)

**Sparse vs Standard Mode Compatibility:**
- **Sparse mode**: Only includes fields that exist in localconfig.vdf
- **Standard mode**: Includes all fields with defaults for missing ones
- **Update behavior**: Only modifies fields present in JSON, regardless of extraction mode
- **Missing fields**: Always preserved during updates

**Tool-Added Fields:**
- **`appid` and `AppName`**: Automatically skipped during updates
- **Validation**: No validation that appid matches the JSON key
- **Safety**: Changing appid in JSON won't affect the actual app being updated

**Shortcut Fields (Exe, StartDir):**
- **Source**: These come from shortcuts.vdf, not localconfig.vdf
- **Current behavior**: Read-only, not written back during updates
- **Reason**: They're managed by Steam's shortcut system, not per-app config

**Steam-Managed Fields:**
- **cloud, autocloud, BadgeData**: Automatically skipped with warnings
- **Safety**: These are complex nested objects that could break Steam if modified
- **Override**: Use `--include-managed` flag to include them in extraction (but still not in updates)

**Nested Object Handling:**
- **Current limitation**: Only flat fields are supported for updates
- **cloud/autocloud**: Complex nested objects are skipped entirely
- **Future enhancement**: Could add support for nested object updates with proper validation

**Edge Cases and Limitations:**

**1. App ID Validation:**
- **Issue**: No validation that JSON appid matches the dictionary key
- **Example**: JSON key "3241660" but appid field "1234567" - updates wrong app
- **Workaround**: Always ensure appid field matches the JSON key
- **Future fix**: Add validation to prevent mismatched app IDs

**2. Field Type Consistency:**
- **Issue**: No validation of field value types
- **Example**: ResolutionOverride expects string but receives number
- **Current behavior**: Updates anyway, may cause Steam issues
- **Recommendation**: Always use correct data types in JSON

**3. Custom Input File Support:**
- **Current limitation**: Update always reads from `data/all_games_config.json`
- **Use case**: Want to update from a different JSON file
- **Workaround**: Copy your file to `data/all_games_config.json`
- **Future enhancement**: Add `--input-file` parameter

**4. Partial Updates:**
- **Current behavior**: Only updates fields present in JSON
- **Benefit**: Safe, preserves other fields
- **Limitation**: Can't easily set fields to empty without explicit null/""
- **Example**: Standard mode with empty defaults won't clear existing values

**5. Backup Management:**
- **Current behavior**: Creates timestamped backups automatically
- **Issue**: No automatic cleanup of old backups
- **Recommendation**: Periodically clean up old backup files
- **Future enhancement**: Add backup retention policy

## Dual-Mode Extraction System

The tool supports two extraction modes to handle Steam's sparse storage model:

### Sparse Mode (Default)
- **Purpose**: Accurate representation of actual data
- **Behavior**: Only includes fields that exist in localconfig.vdf
- **Use Case**: Data analysis, understanding actual Steam configuration
- **Output**: Variable fields per game (2-8 fields typically)

### Standard Mode
- **Purpose**: Frontend-friendly consistent schema
- **Behavior**: All games have same fields with defaults for missing values
- **Use Case**: UI forms, consistent data processing
- **Output**: All games have same fields (9 fields typically)

### Mode Comparison

**Sparse Mode Example:**
```json
{
  "7": {
    "appid": "7",
    "AppName": "App 7"
  },
  "3241660": {
    "appid": "3241660",
    "AppName": "R.E.P.O.",
    "LastPlayed": "1761018554",
    "Playtime": "9520",
    "LaunchOptions": "%command% --doorstop...",
    "ResolutionOverride": "1920x1080"
  }
}
```

**Standard Mode Example:**
```json
{
  "7": {
    "appid": "7",
    "AppName": "App 7",
    "LaunchOptions": "",
    "Playtime": "",
    "LastPlayed": "",
    "ResolutionOverride": "",
    "ResolutionOverrideInternalDisplay": ""
  },
  "3241660": {
    "appid": "3241660",
    "AppName": "R.E.P.O.",
    "LaunchOptions": "%command% --doorstop...",
    "Playtime": "9520",
    "LastPlayed": "1761018554",
    "ResolutionOverride": "1920x1080",
    "ResolutionOverrideInternalDisplay": "0"
  }
}
```

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

## Field Categories and Safety

### Essential Fields (Always Safe to Modify)
- `LaunchOptions` - Command-line parameters
- `ResolutionOverride` - Custom resolution settings
- `ResolutionOverrideInternalDisplay` - Internal display settings
- `Playtime2wks` - Recent play time tracking
- `PlaytimeDisconnected` - Offline play time

### Steam-Managed Fields (Preserve, Don't Modify)
- `cloud` - Cloud sync state (nested object)
- `autocloud` - Auto-cloud settings (nested object)
- `BadgeData` - Achievement/badge data
- `{APPID}_eula_{N}` - EULA acceptance tracking

### Tool-Added Fields (Read-Only)
- `appid` - Steam app ID (added by tool)
- `AppName` - Game name (resolved by tool)

### Write Operation Safety

The tool implements several safety measures when writing back to localconfig.vdf:

1. **Field Validation**: Only safe user fields are modified
2. **Steam-Managed Protection**: Managed fields are skipped with warnings
3. **EULA Protection**: EULA fields are skipped for safety
4. **Field Deletion Support**: 
   - `null` values → delete field from VDF
   - Empty strings `""` → remove field if exists
5. **Backup Creation**: Automatic backup before any write operation
6. **Steam Process Check**: Prevents writes while Steam is running

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
