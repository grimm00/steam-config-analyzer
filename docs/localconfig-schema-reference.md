# localconfig.vdf Schema Reference

## Overview

Steam's `localconfig.vdf` uses a **sparse storage model** - it only stores fields that have been modified from their default values. This means:

- Not all games have all fields
- Fields only appear when they differ from Steam's defaults
- The schema is dynamic and can vary per app

## Complete Field Inventory

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

## Field Categories

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
- `PlaytimeDisconnected` - Offline play tracking

### 4. Dynamic Fields (Per-game)
These vary by app ID:
- `{APPID}_eula_{N}` - EULA acceptance tracking

## Nested Object Structures

### `cloud` Object
```json
{
  "last_sync_state": "synchronized"  // Can be: synchronized, pending, conflict, etc.
}
```

### `autocloud` Object
```json
{
  "lastlaunch": "1761006928",  // Unix timestamp of last launch
  "lastexit": "1761018554"     // Unix timestamp of last exit
}
```

## Example Complete Entry

The most "complete" entry found (R.E.P.O. with 9 fields):

```json
{
  "LastPlayed": "1761018554",
  "cloud": {
    "last_sync_state": "synchronized"
  },
  "autocloud": {
    "lastlaunch": "1761006928",
    "lastexit": "1761018554"
  },
  "BadgeData": "02000000080a",
  "Playtime2wks": "2086",
  "Playtime": "9520",
  "LaunchOptions": "%command% --doorstop-enable true --doorstop-target \"/path/to/mod.dll\" --r2profile \"Friends\"",
  "ResolutionOverride": "1920x1080",
  "ResolutionOverrideInternalDisplay": "0"
}
```

## Example Minimal Entry

A minimal entry (only last played):

```json
{
  "LastPlayed": "1716275847"
}
```

## Implications for Tool Design

### Current Approach (Standardization)
The current tool standardizes all entries with the same fields, filling missing values with empty strings or "0":

```json
{
  "appid": "1245620",
  "AppName": "ELDEN RING",
  "LaunchOptions": "",  // Empty - not in source
  "Playtime": "3127",
  "LastPlayed": "1760929573",
  "ResolutionOverride": "",  // Empty - not in source
  "ResolutionOverrideInternalDisplay": "0"  // Default - not in source
}
```

**Pros:**
- Consistent schema for frontend
- Easy to work with in UI forms
- All fields always present

**Cons:**
- Doesn't reflect actual storage model
- Hard to distinguish between "unset" and "set to empty"
- Larger JSON output

### Alternative Approach (Sparse/Actual)
Only include fields that actually exist in localconfig.vdf:

```json
{
  "appid": "1245620",
  "AppName": "ELDEN RING",
  "Playtime": "3127",
  "LastPlayed": "1760929573",
  "cloud": {
    "last_sync_state": "synchronized"
  },
  "autocloud": {
    "lastlaunch": "1760929430",
    "lastexit": "1760929638"
  },
  "BadgeData": "02000000080a",
  "Playtime2wks": "2"
}
```

**Pros:**
- Accurate representation of actual data
- Smaller JSON output
- Clear distinction between unset and empty values

**Cons:**
- Inconsistent schema (different fields per game)
- Frontend needs to handle optional fields
- More complex validation logic

## Recommendations

### For Read/Extract Operations

**Option 1: Dual Output Mode**
- `extract-all --mode=standard` - Current standardized approach
- `extract-all --mode=sparse` - Sparse/actual approach

**Option 2: Separate Commands**
- `extract-all` - Sparse (actual data only)
- `extract-all-normalized` - Standardized with all fields

### For Write/Update Operations

**Critical:** When writing back:
1. **Only write fields that exist in the JSON**
2. **Don't write empty strings as values** (they're different from absent fields)
3. **Preserve fields we don't extract** (cloud, autocloud, BadgeData, etc.)
4. **Allow field deletion** (set to `null` in JSON to remove from VDF)

### Recommended Field Set for Frontend

**Essential Fields (always extract if present):**
- `appid` (added by tool)
- `AppName` (resolved by tool)
- `LastPlayed`
- `Playtime`
- `LaunchOptions`

**Optional Fields (extract if present):**
- `ResolutionOverride`
- `ResolutionOverrideInternalDisplay`
- `Playtime2wks`
- `PlaytimeDisconnected`

**Preserve But Don't Extract (for safety):**
- `cloud` - Steam manages this
- `autocloud` - Steam manages this
- `BadgeData` - Achievement data
- `{APPID}_eula_{N}` - EULA tracking

## Next Steps

1. **Decide on extraction mode**: Sparse vs Standardized vs Both
2. **Update extraction logic** to handle optional fields
3. **Update write logic** to handle sparse writes correctly
4. **Add field documentation** to help frontend developers
5. **Add validation** to ensure we don't corrupt Steam-managed fields
