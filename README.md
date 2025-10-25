# Steam Config Analyzer

**Purpose:** User-friendly tool for managing Steam game configurations with both CLI and GUI interfaces  
**Version:** v2.0.0  
**Last Updated:** 2025-01-24  
**Status:** 🟡 In Development

---

## 🎯 Quick Start

### Prerequisites

- Python 3.13+
- Steam Deck or Linux system with Steam installed
- Steam must be closed when making configuration changes

### Setup

```bash
# Clone and setup
git clone https://github.com/grimm00/steam-config-analyzer.git
cd steam-config-analyzer

# Install dependencies
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start development environment
python src/cli.py --help
```

### First Steps

1. **Extract current configuration**: `python src/cli.py extract-all`
2. **Edit game settings**: Modify `instance/data/all_games_config.json`
3. **Apply changes**: `python src/cli.py update` (Steam must be closed)

---

## 📁 Project Structure

This project follows a **hub-and-spoke documentation pattern**:

- **Hub Files** (README.md) serve as entry points and navigation guides
- **Spoke Directories** contain detailed implementation and specialized documentation
- **Admin Directory** manages project planning, feedback, and decision tracking

### Key Directories

- **`admin/`** - Project management hub ([Admin Guide](admin/README.md))
- **`backend/`** - Python CLI tool and core logic ([Backend Guide](backend/README.md))
- **`frontend/`** - GUI application (planned) ([Frontend Guide](frontend/README.md))
- **`tests/`** - Centralized testing ([Testing Guide](tests/README.md))
- **`scripts/`** - Automation scripts ([Scripts Guide](scripts/README.md))
- **`docs/`** - User documentation ([Documentation Guide](docs/README.md))

---

## 🚀 Development Workflow

### Git Flow

- **`main`** - Production releases only
- **`develop`** - Ongoing development
- **`feat/*`** - Feature branches (require PRs)
- **`fix/*`** - Bug fixes (require PRs)
- **`docs/*`** - Documentation (can push directly)
- **`chore/*`** - Maintenance (can push directly)

### Branch Requirements

- Feature branches: Full testing, linting, external reviews
- Documentation branches: Minimal validation
- Release branches: Full validation + external reviews

---

## 🛠️ Technology Stack

### Backend

- Python 3.13+
- VDF parsing library
- JSON configuration management
- File system operations

### Frontend (Planned)

- GUI framework (TBD - PyQt6, Tkinter, or web-based)
- Steam Deck compatibility focus
- User-friendly interface design

### DevOps

- GitHub Actions CI/CD
- Automated testing
- Code quality checks

---

## 📊 Project Status

### ✅ Completed

- Core VDF parsing and configuration management
- Dual-mode extraction (sparse/standard)
- Comprehensive CLI interface
- Safety features and backup system
- Dynamic game name resolution

### 🟠 In Progress

- Project restructuring with dev-infra template
- Modular code architecture
- Comprehensive testing infrastructure

### 🟡 Planned

- GUI interface for non-technical users
- Steam Deck optimized UI
- Advanced configuration features
- Bulk operations and presets

---

## 📚 Documentation

### Quick References

- [Installation Guide](docs/user-guide/installation.md)
- [CLI Usage Guide](docs/user-guide/cli-usage.md)
- [Field Reference](docs/technical/field-reference.md)
- [Troubleshooting](docs/troubleshooting.md)

### Planning Documents

- [Project Roadmap](admin/planning/roadmap.md)
- [Feature Plans](admin/planning/features/)
- [Architecture Decisions](admin/planning/decisions/)

---

## 🔧 Development Commands

```bash
# Development
cd backend && source venv/bin/activate
python src/cli.py extract-all --mode=sparse

# Testing
./scripts/run-tests.sh

# Building
./scripts/build.sh

# Documentation
./scripts/setup-dev.sh
```

---

## 📈 Key Features

- **Dual-Mode Extraction**: Sparse (accurate) and Standard (frontend-friendly)
- **Safety First**: Automatic backups and Steam process detection
- **Dynamic Resolution**: Automatic game name resolution from multiple sources
- **User-Friendly**: Designed for Steam Deck users without terminal knowledge
- **Comprehensive**: Handles all Steam game configurations, not just shortcuts

---

## 🎊 Key Achievements

1. **Complete VDF Analysis**: Discovered Steam's dual-file configuration system
2. **Robust CLI Tool**: Full-featured command-line interface with safety features
3. **Comprehensive Documentation**: Detailed guides for all user levels
4. **Professional Structure**: Following industry best practices with dev-infra template

---

## 📞 Support

- [Documentation](docs/)
- [Issues](https://github.com/grimm00/steam-config-analyzer/issues)
- [Discussions](https://github.com/grimm00/steam-config-analyzer/discussions)

---

**Last Updated:** 2025-01-24  
**Status:** 🟡 In Development  
**Next:** Complete project restructuring and begin GUI development