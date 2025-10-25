# Backend Hub

**Purpose:** Python CLI tool and core logic for Steam configuration management  
**Last Updated:** 2025-01-24  
**Status:** 🟡 In Development

---

## 🎯 Quick Navigation

### Core Components
- **[CLI Interface](src/cli.py)** - Command-line interface and argument parsing
- **[VDF Parser](src/core/vdf_parser.py)** - Steam VDF file parsing logic
- **[Game Resolver](src/core/game_resolver.py)** - Dynamic game name resolution
- **[Config Manager](src/core/config_manager.py)** - Configuration management
- **[Backup Manager](src/core/backup_manager.py)** - Backup and restore operations

### API Layer
- **[API Module](src/api/)** - Future API for frontend integration

### Utilities
- **[Utils Module](src/utils/)** - Shared utility functions

---

## 🚀 Quick Start

### Setup
```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run CLI
python src/cli.py --help
```

### Basic Usage
```bash
# Extract all games (sparse mode)
python src/cli.py extract-all --mode=sparse

# Extract with standard mode
python src/cli.py extract-all --mode=standard

# Update configuration (Steam must be closed)
python src/cli.py update

# Create backup
python src/cli.py backup
```

---

## 📁 Architecture

### Modular Design
The backend is structured as a modular Python package:

```
src/
├── cli.py              # CLI interface and argument parsing
├── core/               # Core functionality
│   ├── vdf_parser.py   # VDF file parsing
│   ├── game_resolver.py # Game name resolution
│   ├── config_manager.py # Configuration management
│   └── backup_manager.py # Backup operations
├── api/                # API layer (future)
└── utils/              # Utility functions
```

### Data Flow
1. **Extract**: VDF Parser → Game Resolver → Config Manager → JSON output
2. **Update**: JSON input → Config Manager → Backup Manager → VDF Parser → File write
3. **Backup**: Backup Manager → File operations

---

## 🔧 Core Features

### Dual-Mode Extraction
- **Sparse Mode**: Only includes fields that exist in localconfig.vdf
- **Standard Mode**: All games have same fields with defaults for missing values

### Safety Features
- **Steam Process Detection**: Prevents writes while Steam is running
- **Automatic Backups**: Creates timestamped backups before changes
- **Field Validation**: Only allows safe user-modifiable fields
- **Error Recovery**: Comprehensive error handling and rollback

### Dynamic Game Resolution
- **App Manifests**: Reads Steam app manifest files
- **Library Cache**: Parses Steam library cache
- **Shortcuts VDF**: Fallback to shortcuts.vdf
- **Manual Mappings**: Custom app ID to name mappings

---

## 📊 Configuration Management

### Supported Fields
- **LaunchOptions**: Command-line parameters for games
- **ResolutionOverride**: Force specific resolution
- **ResolutionOverrideInternalDisplay**: Internal display setting
- **PlaytimeDisconnected**: Offline playtime tracking

### Field Safety
- **Safe Fields**: User-modifiable configuration options
- **Managed Fields**: Steam-managed (cloud, autocloud, BadgeData)
- **Tool Fields**: Automatically managed (appid, AppName)

---

## 🧪 Testing

### Test Structure
```
tests/backend/
├── test_vdf_parser.py      # VDF parsing tests
├── test_game_resolver.py   # Game resolution tests
├── test_config_manager.py  # Configuration tests
├── test_backup_manager.py  # Backup tests
└── fixtures/               # Test data
```

### Running Tests
```bash
# Run all backend tests
pytest tests/backend/

# Run specific test file
pytest tests/backend/test_vdf_parser.py

# Run with coverage
pytest --cov=src tests/backend/
```

---

## 📚 API Reference

### CLI Commands
- `extract-all` - Extract all game configurations
- `extract-shortcuts` - Extract only games with launch options
- `update` - Update configuration from JSON
- `backup` - Create manual backup
- `restore` - Restore from backup

### Core Classes
- `VDFConfigManager` - Main configuration management
- `GameNameResolver` - Game name resolution
- `BackupManager` - Backup and restore operations

---

## 🔧 Development

### Adding New Features
1. **Core Logic**: Add to appropriate module in `src/core/`
2. **CLI Interface**: Update `src/cli.py` with new commands
3. **Tests**: Add comprehensive tests in `tests/backend/`
4. **Documentation**: Update this README and user docs

### Code Standards
- **Type Hints**: Use Python type annotations
- **Docstrings**: Document all public methods
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Logging**: Use appropriate logging levels

---

## 📈 Performance

### Optimization Areas
- **VDF Parsing**: Large localconfig.vdf files
- **Game Resolution**: Caching resolved names
- **File I/O**: Efficient backup operations
- **Memory Usage**: Large configuration datasets

### Monitoring
- **Parse Time**: VDF file parsing performance
- **Memory Usage**: Configuration data handling
- **File Operations**: Backup and restore speed

---

## 🚨 Troubleshooting

### Common Issues
- **Steam Running**: Tool prevents writes while Steam is active
- **Permission Errors**: Check file permissions for Steam directory
- **VDF Corruption**: Use backup restore functionality
- **Game Resolution**: Check app manifest and cache files

### Debug Mode
```bash
# Enable debug logging
python src/cli.py --debug extract-all
```

---

## 📞 Support

- [User Documentation](../docs/user-guide/cli-usage.md)
- [Technical Documentation](../docs/technical/)
- [Troubleshooting Guide](../docs/troubleshooting.md)
- [Issues](https://github.com/grimm00/steam-config-analyzer/issues)

---

**Last Updated:** 2025-01-24  
**Status:** 🟡 In Development  
**Next:** Complete modular refactoring and comprehensive testing
