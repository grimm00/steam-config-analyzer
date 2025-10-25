# CLI Usage Guide

**Purpose:** Complete command-line interface documentation  
**Last Updated:** 2025-01-24  
**Status:** ✅ Complete

---

## 🎯 Quick Start

### Basic Commands

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment
source venv/bin/activate

# Get help
python src/cli.py --help

# Extract all games (safe operation)
python src/cli.py extract-all --mode=sparse
```

---

## 📋 Available Commands

### extract-all
Extract all game configurations from localconfig.vdf.

```bash
python src/cli.py extract-all [options]
```

**Options:**
- `--mode {sparse,standard}` - Extraction mode (default: sparse)
- `--include-system` - Include system apps (Proton, Steam Runtime)
- `--include-managed` - Include Steam-managed fields
- `--user-id USER_ID` - Steam user ID (default: 107256425)

**Examples:**
```bash
# Extract with sparse mode (recommended)
python src/cli.py extract-all --mode=sparse

# Extract with standard mode (frontend-friendly)
python src/cli.py extract-all --mode=standard

# Include system apps
python src/cli.py extract-all --include-system

# Include managed fields
python src/cli.py extract-all --include-managed
```

### extract
Extract only games with launch options (legacy compatibility).

```bash
python src/cli.py extract [options]
```

**Note:** This is equivalent to `extract-all` filtered for games with launch options.

### update
Update localconfig.vdf with modified JSON data.

```bash
python src/cli.py update [options]
```

**Options:**
- `--user-id USER_ID` - Steam user ID (default: 107256425)

**⚠️ Important:** Steam must be closed before running this command.

### backup
Create a manual backup of localconfig.vdf.

```bash
python src/cli.py backup [options]
```

**Options:**
- `--user-id USER_ID` - Steam user ID (default: 107256425)

### restore
Restore localconfig.vdf from a backup file.

```bash
python src/cli.py restore --backup-path PATH [options]
```

**Options:**
- `--backup-path PATH` - Path to backup file (required)
- `--user-id USER_ID` - Steam user ID (default: 107256425)

**⚠️ Important:** Steam must be closed before running this command.

### refresh-cache
Refresh the app name cache.

```bash
python src/cli.py refresh-cache [options]
```

**Options:**
- `--user-id USER_ID` - Steam user ID (default: 107256425)

---

## 🔄 Complete Workflow

### Step 1: Extract Current Configuration

```bash
# Extract all games in sparse mode (recommended)
python src/cli.py extract-all --mode=sparse
```

This creates `backend/instance/data/all_games_config.json` with your current game configurations.

### Step 2: Edit Configuration

Open `backend/instance/data/all_games_config.json` and modify the fields you want to change.

**Example modifications:**
```json
{
  "3241660": {
    "appid": "3241660",
    "AppName": "R.E.P.O.",
    "LaunchOptions": "%command% --new-profile \"Friends2\""
  }
}
```

### Step 3: Close Steam

**Important:** Steam must be completely closed before updating configuration.

```bash
# Check if Steam is running
pgrep -f steam

# If Steam is running, close it completely
# The tool will also check and prevent updates if Steam is running
```

### Step 4: Apply Changes

```bash
# Update configuration (Steam must be closed)
python src/cli.py update
```

### Step 5: Start Steam and Test

Launch Steam and verify your changes are applied correctly.

---

## 📝 JSON Editing Guide

### Field Modification Syntax

- **Modify existing field**: Change the value in the JSON
- **Add new field**: Include the field in the JSON with your desired value
- **Delete field**: Set the field to `null` or `""` (empty string)
- **Preserve field**: Don't include the field in the JSON (will remain unchanged)

### Practical Examples

**Update Launch Options:**
```json
{
  "3241660": {
    "appid": "3241660",
    "AppName": "R.E.P.O.",
    "LaunchOptions": "%command% --new-profile \"Friends2\""
  }
}
```

**Change Resolution:**
```json
{
  "1245620": {
    "appid": "1245620",
    "AppName": "ELDEN RING",
    "ResolutionOverride": "2560x1440"
  }
}
```

**Remove Launch Options:**
```json
{
  "3241660": {
    "appid": "3241660",
    "AppName": "R.E.P.O.",
    "LaunchOptions": ""
  }
}
```

**Bulk Update Multiple Games:**
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

---

## 🎮 Real-World Scenarios

### Scenario 1: Modding a Game

```bash
# 1. Extract current config
python src/cli.py extract-all --mode=sparse

# 2. Edit backend/instance/data/all_games_config.json
# Add mod launcher to launch options:
{
  "3241660": {
    "appid": "3241660",
    "AppName": "R.E.P.O.",
    "LaunchOptions": "%command% --doorstop-enable true --doorstop-target \"/home/deck/Mods/BepInEx/core/BepInEx.dll\""
  }
}

# 3. Close Steam and update
python src/cli.py update
```

### Scenario 2: Performance Optimization

```bash
# 1. Extract all games
python src/cli.py extract-all --mode=standard

# 2. Set consistent resolution for multiple games
{
  "1245620": {"appid": "1245620", "AppName": "ELDEN RING", "ResolutionOverride": "1920x1080"},
  "1174180": {"appid": "1174180", "AppName": "Red Dead Redemption 2", "ResolutionOverride": "1920x1080"},
  "271590": {"appid": "271590", "AppName": "Grand Theft Auto V", "ResolutionOverride": "1920x1080"}
}

# 3. Apply changes
python src/cli.py update
```

### Scenario 3: Clean Up Old Settings

```bash
# 1. Extract current config
python src/cli.py extract-all --mode=sparse

# 2. Remove launch options from games that no longer need them
{
  "3241660": {
    "appid": "3241660",
    "AppName": "R.E.P.O.",
    "LaunchOptions": ""  # This will delete the field
  }
}

# 3. Apply cleanup
python src/cli.py update
```

---

## 🔧 Command Options

### Global Options

- `--user-id USER_ID` - Steam user ID (default: 107256425)
- `--help` - Show help message

### Extraction Options

- `--mode {sparse,standard}` - Extraction mode
  - **sparse**: Only include fields that exist (recommended)
  - **standard**: Include all fields with defaults (frontend-friendly)
- `--include-system` - Include system apps (Proton, Steam Runtime)
- `--include-managed` - Include Steam-managed fields (cloud, autocloud, BadgeData)

### Update Options

- `--backup-path PATH` - Path to backup file (for restore command)

---

## 📊 Output Files

### Configuration Files

- `backend/instance/data/all_games_config.json` - Main configuration file
- `backend/instance/data/app_name_cache.json` - Game name resolution cache

### Backup Files

- `backend/instance/data/backups/localconfig_backup_YYYYMMDD_HHMMSS.vdf` - Automatic backups

### Archive Files

- `backend/instance/archive/` - Legacy scripts and old data files

---

## 🚨 Safety Features

### Steam Process Detection

The tool automatically checks if Steam is running and prevents dangerous operations:

```bash
# This will fail if Steam is running
python src/cli.py update
# Error: Steam is currently running. Please close Steam before updating configuration.
```

### Automatic Backups

Every update operation creates an automatic backup:

```
Updating localconfig.vdf with JSON data...
Backup created: backend/instance/data/backups/localconfig_backup_20251023_143022.vdf
Updated LaunchOptions for app 3241660
Successfully updated localconfig.vdf
Backup available at: backend/instance/data/backups/localconfig_backup_20251023_143022.vdf
```

### Field Validation

Only safe user-modifiable fields are updated:

- ✅ **Safe Fields**: LaunchOptions, ResolutionOverride, ResolutionOverrideInternalDisplay
- ⚠️ **Managed Fields**: cloud, autocloud, BadgeData (skipped with warning)
- ❌ **Dangerous Fields**: EULA fields (skipped for safety)

---

## 🔍 Troubleshooting

### Common Issues

**Steam is running error:**
```bash
# Close Steam completely and try again
pgrep -f steam  # Check if Steam is still running
```

**File not found error:**
```bash
# Check if Steam is installed and configured
ls ~/.local/share/Steam/userdata/
```

**Permission denied:**
```bash
# Check file permissions
ls -la ~/.local/share/Steam/userdata/[USER_ID]/config/
```

### Getting Help

- **[Troubleshooting Guide](../troubleshooting.md)** - Common issues and solutions
- **[Field Reference](../technical/field-reference.md)** - Configuration field details
- **[Issues](https://github.com/grimm00/steam-config-analyzer/issues)** - Report problems

---

**Last Updated:** 2025-01-24  
**Status:** ✅ Complete  
**Next:** [GUI Usage Guide](gui-usage.md) (when available)
