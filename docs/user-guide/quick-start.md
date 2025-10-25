# Quick Start Guide

**Purpose:** Get up and running with Steam Config Analyzer in minutes  
**Last Updated:** 2025-01-24  
**Status:** ✅ Complete

---

## 🚀 5-Minute Setup

### Step 1: Install (2 minutes)

```bash
# Clone the repository
git clone https://github.com/grimm00/steam-config-analyzer.git
cd steam-config-analyzer

# Setup backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Extract Your Games (1 minute)

```bash
# Extract all your Steam games
python src/cli.py extract-all --mode=sparse
```

This creates `backend/instance/data/all_games_config.json` with all your game configurations.

### Step 3: Make a Change (1 minute)

Edit `backend/instance/data/all_games_config.json` to modify a game:

```json
{
  "1245620": {
    "appid": "1245620",
    "AppName": "ELDEN RING",
    "ResolutionOverride": "1920x1080"
  }
}
```

### Step 4: Apply Changes (1 minute)

```bash
# Close Steam first, then:
python src/cli.py update
```

### Step 5: Test (30 seconds)

Start Steam and launch your modified game to see the changes!

---

## 🎯 Common Use Cases

### Change Game Resolution

**Problem:** Game runs at wrong resolution  
**Solution:** Set ResolutionOverride

```json
{
  "1245620": {
    "appid": "1245620",
    "AppName": "ELDEN RING",
    "ResolutionOverride": "1920x1080"
  }
}
```

### Add Mod Launcher

**Problem:** Want to use mods with a game  
**Solution:** Add LaunchOptions

```json
{
  "3241660": {
    "appid": "3241660",
    "AppName": "R.E.P.O.",
    "LaunchOptions": "%command% --doorstop-enable true --doorstop-target \"/path/to/mod.dll\""
  }
}
```

### Remove Launch Options

**Problem:** Game has old launch options you don't want  
**Solution:** Set LaunchOptions to empty string

```json
{
  "3241660": {
    "appid": "3241660",
    "AppName": "R.E.P.O.",
    "LaunchOptions": ""
  }
}
```

---

## 🔧 Essential Commands

### Extract Games
```bash
# Get all your games (recommended)
python src/cli.py extract-all --mode=sparse

# Get all games with standard format
python src/cli.py extract-all --mode=standard
```

### Update Configuration
```bash
# Apply your changes (Steam must be closed)
python src/cli.py update
```

### Create Backup
```bash
# Manual backup
python src/cli.py backup
```

### Restore Backup
```bash
# Restore from backup
python src/cli.py restore --backup-path backend/instance/data/backups/backup_file.vdf
```

---

## 📁 Key Files

### Configuration Files
- `backend/instance/data/all_games_config.json` - Your game configurations
- `backend/instance/data/app_name_cache.json` - Game name cache

### Backup Files
- `backend/instance/data/backups/` - Automatic backups

### Archive Files
- `backend/instance/archive/` - Legacy files

---

## ⚠️ Important Safety Notes

### Steam Must Be Closed
- **Always close Steam** before running `update` command
- **The tool will check** and prevent updates if Steam is running
- **Steam can be restarted** after changes are applied

### Automatic Backups
- **Backups are created automatically** before any changes
- **Backup files** are stored in `backend/instance/data/backups/`
- **You can restore** from any backup if needed

### Safe Fields Only
- **Only user-modifiable fields** are updated
- **Steam-managed fields** are skipped for safety
- **EULA fields** are never modified

---

## 🎮 Steam Deck Users

### Desktop Mode Setup
1. **Switch to Desktop Mode** on your Steam Deck
2. **Open Konsole** (terminal application)
3. **Follow the 5-minute setup** above
4. **Test with a simple change** to verify everything works

### Gaming Mode
- **Gaming Mode works normally** after setup
- **Changes persist** between Desktop and Gaming Mode
- **No special configuration** needed for Gaming Mode

---

## 🔍 Troubleshooting

### Steam is Running Error
```bash
# Close Steam completely and try again
pgrep -f steam  # Check if Steam is still running
```

### File Not Found
```bash
# Check if Steam is installed
ls ~/.local/share/Steam/userdata/
```

### Permission Denied
```bash
# Check file permissions
ls -la ~/.local/share/Steam/userdata/[USER_ID]/config/
```

---

## 📚 Next Steps

### Learn More
- **[CLI Usage Guide](cli-usage.md)** - Complete command reference
- **[Field Reference](../technical/field-reference.md)** - All configuration options
- **[Troubleshooting Guide](../troubleshooting.md)** - Common issues and solutions

### Advanced Usage
- **[Installation Guide](installation.md)** - Detailed setup instructions
- **[Technical Documentation](../technical/)** - Implementation details
- **[API Documentation](../api/)** - Backend API reference

### Get Help
- **[FAQ](../faq.md)** - Frequently asked questions
- **[Issues](https://github.com/grimm00/steam-config-analyzer/issues)** - Report problems
- **[Discussions](https://github.com/grimm00/steam-config-analyzer/discussions)** - Community help

---

## 🎊 You're Ready!

You now have a powerful tool for managing your Steam game configurations. The tool is designed to be safe, with automatic backups and validation, so you can experiment with confidence.

**Happy gaming!** 🎮

---

**Last Updated:** 2025-01-24  
**Status:** ✅ Complete  
**Next:** [CLI Usage Guide](cli-usage.md)
