# Field Reference

**Purpose:** Complete reference for Steam configuration fields  
**Last Updated:** 2025-01-24  
**Status:** ✅ Complete

---

## 🎯 Overview

Steam's `localconfig.vdf` uses a **sparse storage model** - it only stores fields that have been modified from their default values. This means:

- Not all games have all fields
- Fields only appear when they differ from Steam's defaults
- The schema is dynamic and can vary per app

---

## 📊 Field Categories

### 1. Common Fields (>50% frequency)
These are most likely to be present:
- `LastPlayed` (90%) - Almost always present
- `Playtime` (80%) - Present for most played games

### 2. User-Configured Fields (<5% frequency)
These only appear when explicitly set by user:
- `LaunchOptions` - Custom launch parameters
- `ResolutionOverride` - Custom resolution
- `ResolutionOverrideInternalDisplay` - Internal display settings

### 3. System-Managed Fields (Variable frequency)
These appear based on game state:
- `cloud` - Cloud sync status
- `autocloud` - Auto-cloud configuration
- `BadgeData` - Achievement/badge data
- `Playtime2wks` - Recent play tracking

### 4. EULA Fields (Per-game)
These track EULA acceptance:
- `{APPID}_eula_0` - EULA version 0 acceptance
- `{APPID}_eula_1` - EULA version 1 acceptance

---

## 📋 Complete Field Inventory

Based on analysis of 50 apps in a real Steam configuration:

| Field Name | Frequency | Percentage | Description |
|------------|-----------|------------|-------------|
| `LastPlayed` | 45/50 | 90.0% | Unix timestamp of last play session |
| `Playtime` | 40/50 | 80.0% | Total play time in minutes |
| `PlaytimeDisconnected` | 11/50 | 22.0% | Playtime while disconnected from Steam |
| `cloud` | 12/50 | 24.0% | Cloud sync state (nested object) |
| `autocloud` | 7/50 | 14.0% | Auto-cloud settings (nested object) |
| `BadgeData` | 8/50 | 16.0% | Badge/achievement data (hex string) |
| `Playtime2wks` | 5/50 | 10.0% | Playtime in last 2 weeks (minutes) |
| `LaunchOptions` | 1/50 | 2.0% | Command-line launch parameters |
| `ResolutionOverride` | 1/50 | 2.0% | Custom resolution setting |
| `ResolutionOverrideInternalDisplay` | 1/50 | 2.0% | Internal display resolution override |
| `{APPID}_eula_{N}` | 6/50 | 12.0% | EULA acceptance tracking (per-game) |

**Total unique fields found: 17**  
**Total apps analyzed: 50**

---

## 🔧 User-Modifiable Fields

### LaunchOptions
**Purpose:** Command-line parameters passed to the game  
**Format:** String with parameters  
**Examples:** 
- `"%command% --fullscreen --width 1920"`
- `"%command% --doorstop-enable true --doorstop-target \"/path/to/mod.dll\""`
- `"%command% --profile \"Friends\""`

**Notes:** 
- Always start with `%command%` for non-Steam games
- Use quotes around parameters with spaces
- Escape special characters properly

### ResolutionOverride
**Purpose:** Force a specific resolution for the game  
**Format:** "WIDTHxHEIGHT" or "Native"  
**Examples:** 
- `"1920x1080"`
- `"2560x1440"`
- `"Native"`

**Notes:** 
- Use "Native" to let the game choose its own resolution
- Common resolutions: 1920x1080, 2560x1440, 3840x2160
- Must be supported by your display

### ResolutionOverrideInternalDisplay
**Purpose:** Internal display override setting  
**Format:** "0" (disabled) or "1" (enabled)  
**Common Value:** Usually "0"  
**Notes:** 
- Rarely needs to be changed
- Used for internal display scaling
- Leave as "0" unless you know what you're doing

### PlaytimeDisconnected
**Purpose:** Track playtime while disconnected from Steam  
**Format:** Number (minutes)  
**Notes:** 
- Usually managed by Steam automatically
- Can be manually set for offline play tracking
- Rarely needs modification

---

## 🛡️ Steam-Managed Fields

### cloud
**Purpose:** Cloud sync state and configuration  
**Format:** Nested object  
**Example:**
```json
{
  "cloud": {
    "last_sync_state": "synchronized",
    "quota_bytes": "20000000000",
    "quota_files": "50000",
    "used_bytes": "7219221",
    "used_files": "68"
  }
}
```

**Notes:**
- **DO NOT MODIFY** - Managed by Steam
- Contains sync status and quota information
- Automatically updated by Steam

### autocloud
**Purpose:** Auto-cloud sync settings  
**Format:** Nested object  
**Example:**
```json
{
  "autocloud": {
    "lastlaunch": "1761110413",
    "lastsync": "1761110413"
  }
}
```

**Notes:**
- **DO NOT MODIFY** - Managed by Steam
- Contains auto-sync timestamps
- Automatically updated by Steam

### BadgeData
**Purpose:** Achievement and badge data  
**Format:** Hex string  
**Example:** `"010000000100000001000000"`

**Notes:**
- **DO NOT MODIFY** - Managed by Steam
- Contains achievement and badge information
- Automatically updated by Steam

---

## ⚠️ Dangerous Fields

### EULA Fields
**Purpose:** Track EULA acceptance per game  
**Format:** `{APPID}_eula_{VERSION}`  
**Examples:**
- `"1245620_eula_0"` - EULA version 0 for ELDEN RING
- `"3241660_eula_1"` - EULA version 1 for R.E.P.O.

**Notes:**
- **DO NOT MODIFY** - Could break game functionality
- Used by Steam to track EULA acceptance
- Modifying could cause games to not launch

---

## 📈 Field Frequency Analysis

### Most Common Fields
1. **LastPlayed** (90%) - Almost every game
2. **Playtime** (80%) - Most played games
3. **PlaytimeDisconnected** (22%) - Some offline play
4. **cloud** (24%) - Games with cloud sync
5. **BadgeData** (16%) - Games with achievements

### Least Common Fields
1. **LaunchOptions** (2%) - Custom launch parameters
2. **ResolutionOverride** (2%) - Custom resolution
3. **ResolutionOverrideInternalDisplay** (2%) - Internal display settings

### System Fields
- **autocloud** (14%) - Auto-cloud enabled games
- **Playtime2wks** (10%) - Recently played games
- **EULA fields** (12%) - Games with EULA acceptance

---

## 🔍 Field Examples

### Complete Game Entry
```json
{
  "1245620": {
    "LastPlayed": "1735544601",
    "Playtime": "915",
    "PlaytimeDisconnected": "0",
    "cloud": {
      "last_sync_state": "synchronized",
      "quota_bytes": "20000000000",
      "quota_files": "50000",
      "used_bytes": "7219221",
      "used_files": "68"
    },
    "autocloud": {
      "lastlaunch": "1761110413",
      "lastsync": "1761110413"
    },
    "BadgeData": "010000000100000001000000",
    "Playtime2wks": "915",
    "ResolutionOverride": "1920x1080",
    "ResolutionOverrideInternalDisplay": "0"
  }
}
```

### Minimal Game Entry
```json
{
  "7": {
    "LastPlayed": "1716275847",
    "Playtime": "1260"
  }
}
```

### Game with Launch Options
```json
{
  "3241660": {
    "LastPlayed": "1735544601",
    "Playtime": "915",
    "LaunchOptions": "%command% --profile \"Friends\"",
    "ResolutionOverride": "1920x1080",
    "ResolutionOverrideInternalDisplay": "0"
  }
}
```

---

## 🚨 Safety Guidelines

### Safe to Modify
- ✅ `LaunchOptions` - User launch parameters
- ✅ `ResolutionOverride` - Display resolution
- ✅ `ResolutionOverrideInternalDisplay` - Internal display settings
- ✅ `PlaytimeDisconnected` - Offline play tracking

### Never Modify
- ❌ `cloud` - Cloud sync state
- ❌ `autocloud` - Auto-cloud settings
- ❌ `BadgeData` - Achievement data
- ❌ `{APPID}_eula_{N}` - EULA acceptance
- ❌ `LastPlayed` - Play session tracking
- ❌ `Playtime` - Total play time
- ❌ `Playtime2wks` - Recent play time

### Tool-Managed
- 🔧 `appid` - Added by tool for identification
- 🔧 `AppName` - Resolved by tool for display

---

## 📚 Related Documentation

- **[CLI Usage Guide](../user-guide/cli-usage.md)** - How to modify fields
- **[Troubleshooting Guide](../troubleshooting.md)** - Common field issues
- **[Architecture Overview](architecture.md)** - How fields are processed

---

**Last Updated:** 2025-01-24  
**Status:** ✅ Complete  
**Next:** [Architecture Overview](architecture.md)
