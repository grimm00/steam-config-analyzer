# Scripts Hub

**Purpose:** Automation scripts for development and deployment  
**Last Updated:** 2025-01-24  
**Status:** 🟡 In Development

---

## 🎯 Available Scripts

### Development Scripts
- **[setup-dev.sh](setup-dev.sh)** - Development environment setup
- **[run-tests.sh](run-tests.sh)** - Test suite runner
- **[build.sh](build.sh)** - Build and package distribution

### Utility Scripts
- **[validate-config.sh](validate-config.sh)** - Validate configuration files
- **[backup-data.sh](backup-data.sh)** - Backup user data
- **[cleanup.sh](cleanup.sh)** - Clean temporary files

---

## 🚀 Quick Start

### Setup Development Environment
```bash
# Make scripts executable
chmod +x scripts/*.sh

# Setup development environment
./scripts/setup-dev.sh

# Run tests
./scripts/run-tests.sh

# Build project
./scripts/build.sh
```

---

## 📁 Script Details

### setup-dev.sh
**Purpose**: Set up complete development environment

**Features**:
- Clone repository and dependencies
- Create Python virtual environment
- Install all required packages
- Setup pre-commit hooks
- Validate installation

**Usage**:
```bash
./scripts/setup-dev.sh
```

### run-tests.sh
**Purpose**: Run comprehensive test suite

**Features**:
- Run all test categories (unit, integration, e2e)
- Generate coverage reports
- Run linting and code quality checks
- Performance testing

**Usage**:
```bash
# Run all tests
./scripts/run-tests.sh

# Run specific test category
./scripts/run-tests.sh --unit
./scripts/run-tests.sh --integration
./scripts/run-tests.sh --e2e
```

### build.sh
**Purpose**: Build and package for distribution

**Features**:
- Build backend package
- Create distribution archives
- Generate documentation
- Validate build artifacts

**Usage**:
```bash
# Build all components
./scripts/build.sh

# Build specific component
./scripts/build.sh --backend
./scripts/build.sh --frontend
```

---

## 🔧 Script Development

### Script Standards
- **Bash**: Use bash for cross-platform compatibility
- **Error Handling**: Proper error checking and reporting
- **Logging**: Clear output and progress indication
- **Documentation**: Inline comments and help text

### Adding New Scripts
1. **Create Script**: Add new `.sh` file in `scripts/`
2. **Make Executable**: `chmod +x scripts/new-script.sh`
3. **Add Documentation**: Update this README
4. **Test**: Verify script works in different environments

---

## 📊 Script Metrics

### Performance
- **Execution Time**: Track script performance
- **Resource Usage**: Monitor memory and CPU usage
- **Success Rate**: Track script success/failure rates

### Quality
- **Error Handling**: Comprehensive error checking
- **User Experience**: Clear output and progress indication
- **Maintainability**: Well-documented and modular code

---

## 🚨 Troubleshooting

### Common Issues
- **Permission Denied**: Ensure scripts are executable
- **Path Issues**: Use absolute paths in scripts
- **Dependency Missing**: Check all required tools are installed
- **Environment Variables**: Verify required environment setup

### Debug Mode
```bash
# Run script with debug output
bash -x scripts/setup-dev.sh

# Check script syntax
bash -n scripts/setup-dev.sh
```

---

## 📚 Script Documentation

### Inline Documentation
- **Header Comments**: Purpose and usage
- **Function Comments**: Parameter and return descriptions
- **Inline Comments**: Complex logic explanations

### External Documentation
- **README Updates**: Document new scripts here
- **Usage Examples**: Provide working examples
- **Troubleshooting**: Common issues and solutions

---

## 🔗 Integration

### CI/CD Integration
- **GitHub Actions**: Use scripts in workflows
- **Pre-commit Hooks**: Validate before commits
- **Automated Testing**: Run tests automatically

### Development Workflow
- **Local Development**: Use scripts for daily tasks
- **Code Review**: Validate changes with scripts
- **Release Process**: Automated build and deployment

---

## 📞 Support

- [Backend Documentation](../backend/README.md)
- [Testing Guide](../tests/README.md)
- [Issues](https://github.com/grimm00/steam-config-analyzer/issues)

---

**Last Updated:** 2025-01-24  
**Status:** 🟡 In Development  
**Next:** Create automation scripts for development workflow
