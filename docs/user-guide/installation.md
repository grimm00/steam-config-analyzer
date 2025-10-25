# Installation Guide

**Purpose:** Complete setup instructions for Steam Config Analyzer  
**Last Updated:** 2025-01-24  
**Status:** ✅ Complete

---

## 🎯 Quick Installation

### Prerequisites

- **Python 3.13+** - Required for the backend
- **Steam Deck or Linux** - Primary target platform
- **Steam Installed** - Must have Steam installed and configured
- **Git** - For cloning the repository

### System Requirements

- **Operating System**: Linux (Steam Deck, Ubuntu, Arch, etc.)
- **Memory**: 512MB RAM minimum
- **Storage**: 100MB for application + space for backups
- **Permissions**: Read/write access to Steam configuration files

---

## 📥 Installation Methods

### Method 1: Clone from GitHub (Recommended)

```bash
# Clone the repository
git clone https://github.com/grimm00/steam-config-analyzer.git
cd steam-config-analyzer

# Setup backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Test installation
python src/cli.py --help
```

### Method 2: Download Release (Future)

```bash
# Download and extract release (when available)
wget https://github.com/grimm00/steam-config-analyzer/releases/latest/download/steam-config-analyzer.tar.gz
tar -xzf steam-config-analyzer.tar.gz
cd steam-config-analyzer

# Follow setup instructions
```

---

## 🔧 Backend Setup

### Virtual Environment

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Verify Installation

```bash
# Test CLI help
python src/cli.py --help

# Test extraction (safe operation)
python src/cli.py extract-all --mode=sparse
```

---

## 🎮 Steam Deck Specific Setup

### Desktop Mode

1. **Switch to Desktop Mode** on your Steam Deck
2. **Open Konsole** (terminal application)
3. **Follow standard installation** steps above
4. **Test with a simple extraction** to verify everything works

### Steam Deck Considerations

- **Steam must be closed** before making configuration changes
- **Use Desktop Mode** for installation and configuration
- **Gaming Mode** will work normally after setup
- **Backups are automatic** - don't worry about losing settings

---

## 🚨 Important Notes

### Steam Process Management

- **Always close Steam** before running update commands
- **The tool will check** if Steam is running and prevent dangerous operations
- **Steam can be restarted** after configuration changes are applied

### File Permissions

- **Steam config files** are in `~/.local/share/Steam/userdata/[USER_ID]/config/`
- **Default user ID** is `107256425` (can be changed with `--user-id` flag)
- **Backup files** are stored in `backend/instance/data/backups/`

### Safety Features

- **Automatic backups** are created before any changes
- **Steam process detection** prevents writes while Steam is running
- **Field validation** only allows safe user-modifiable fields
- **Rollback capability** using backup files

---

## 🔍 Troubleshooting Installation

### Common Issues

**Python not found:**
```bash
# Install Python 3.13+ on your system
sudo pacman -S python  # Arch/Steam Deck
sudo apt install python3  # Ubuntu/Debian
```

**Permission denied:**
```bash
# Make sure you have access to Steam directory
ls ~/.local/share/Steam/userdata/
```

**Module not found:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

**Steam config not found:**
```bash
# Check if Steam is installed and configured
ls ~/.local/share/Steam/userdata/
# Look for your user ID directory
```

### Getting Help

- **[Troubleshooting Guide](../troubleshooting.md)** - Common issues and solutions
- **[FAQ](../faq.md)** - Frequently asked questions
- **[Issues](https://github.com/grimm00/steam-config-analyzer/issues)** - Report problems
- **[Discussions](https://github.com/grimm00/steam-config-analyzer/discussions)** - Community help

---

## ✅ Installation Complete

Once installation is complete, you can:

1. **[Quick Start Guide](quick-start.md)** - Get started with basic usage
2. **[CLI Usage Guide](cli-usage.md)** - Learn command-line interface
3. **[GUI Usage Guide](gui-usage.md)** - Use graphical interface (when available)

---

**Last Updated:** 2025-01-24  
**Status:** ✅ Complete  
**Next:** [Quick Start Guide](quick-start.md)
