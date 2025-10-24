# Steam Configuration Analysis Findings

## Executive Summary

Through analysis of Steam configuration files, we discovered that Steam uses a dual-file system for storing configuration data, with `localconfig.vdf` being the authoritative source for current settings.

## File Structure Analysis

### `shortcuts.vdf`
- **Format**: Binary VDF (Valve Data Format)
- **Content**: Non-Steam game shortcuts only
- **Status**: Legacy/backup file
- **Last Modified**: October 21, 2025
- **Parsing**: Successfully parsed using Python `vdf` library

### `localconfig.vdf`
- **Format**: Binary VDF with different structure
- **Content**: ALL Steam configuration data
- **Status**: Master configuration file
- **Last Modified**: October 23, 2025 (more recent)
- **Parsing**: Difficult to parse with standard vdf library

## Key Discoveries

### 1. Configuration Hierarchy
```
localconfig.vdf (Master)
├── Steam Games Configuration
├── Non-Steam Games Configuration (shortcuts)
├── User Preferences
└── UI Settings

shortcuts.vdf (Legacy)
└── Non-Steam Games Only
```

### 2. The REPO Duplication Issue
REPO appeared in both files with different configurations:

**In `shortcuts.vdf` (Outdated):**
```json
{
  "LaunchOptions": "--doorstop-enable true --doorstop-target \"/home/deck/.config/r2modmanPlus-local/REPO/profiles/Kat/BepInEx/core/BepInEx.Preloader.dll\" --r2profile \"Kat\""
}
```

**In `localconfig.vdf` (Current):**
```json
{
  "LaunchOptions": "%command% --doorstop-enable true --doorstop-target \"/home/deck/.config/r2modmanPlus-local/REPO/profiles/Friends/BepInEx/core/BepInEx.Preloader.dll\" --r2profile \"Friends\""
}
```

### 3. Non-Steam Games Identified
From `shortcuts.vdf` analysis, we found 5 non-Steam games:

1. **R.E.P.O.** - Game with BepInEx mod support
2. **Dragon's Crown** - PlayStation 3 emulation via RPCS3
3. **Pokemon Unbound** - Game Boy Advance emulation via RetroArch
4. **NVIDIA GeForce NOW** - Cloud gaming service
5. **SimpleDSCSModManager.exe** - Mod manager tool

## Technical Challenges

### VDF Library Limitations
- The `vdf` library successfully parses `shortcuts.vdf`
- The same library fails to parse `localconfig.vdf` due to format differences
- Error: "Unterminated cstring (offset: 1)"

### Alternative Parsing Methods
- Text-based extraction from `localconfig.vdf` using `grep`
- Manual reconstruction of shortcut data
- Hex dump analysis for binary content verification

## Recommendations

### For Developers
1. **Use `localconfig.vdf`** as the primary source for current Steam configuration
2. **Treat `shortcuts.vdf`** as a legacy/backup file
3. **Implement text-based parsing** for `localconfig.vdf` when vdf library fails
4. **Handle duplicate entries** by prioritizing `localconfig.vdf` data

### For Users
1. **Remove duplicate shortcuts** from Steam UI to avoid confusion
2. **Backup both files** before making manual changes
3. **Use Steam UI** for configuration changes rather than manual file editing

## Future Research

1. **Investigate `localconfig.vdf` format** more deeply
2. **Develop custom parser** for `localconfig.vdf`
3. **Analyze other Steam configuration files** for completeness
4. **Document Steam's configuration synchronization** process

## Tools Developed

- **VDF Parser**: Successfully parses `shortcuts.vdf`
- **Text Extractor**: Extracts data from `localconfig.vdf`
- **Comparison Tool**: Shows differences between old and current configurations
- **JSON Exporter**: Converts parsed data to JSON format

## Conclusion

Steam's configuration system is more complex than initially apparent, with `localconfig.vdf` serving as the authoritative source for current settings. The `shortcuts.vdf` file appears to be a legacy format that may not always reflect the current state of non-Steam game configurations.
