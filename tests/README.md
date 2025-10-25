# Testing Hub

**Purpose:** Centralized testing infrastructure and strategy  
**Last Updated:** 2025-01-24  
**Status:** 🟡 In Development

---

## 🎯 Testing Strategy

### Test Coverage Goals
- **Backend**: >80% code coverage
- **Frontend**: >70% code coverage (when implemented)
- **Integration**: Critical user workflows
- **End-to-End**: Complete user journeys

### Testing Pyramid
1. **Unit Tests** - Individual components and functions
2. **Integration Tests** - Component interactions
3. **End-to-End Tests** - Complete user workflows

---

## 📁 Test Structure

### Backend Tests
- **[VDF Parser Tests](backend/test_vdf_parser.py)** - VDF file parsing
- **[Game Resolver Tests](backend/test_game_resolver.py)** - Game name resolution
- **[Config Manager Tests](backend/test_config_manager.py)** - Configuration management
- **[Backup Manager Tests](backend/test_backup_manager.py)** - Backup operations
- **[Fixtures](backend/fixtures/)** - Test data and mock files

### Frontend Tests (Future)
- **UI Component Tests** - Individual interface components
- **User Interaction Tests** - Button clicks, form submissions
- **Visual Regression Tests** - Screenshot comparisons

### Integration Tests
- **CLI Workflow Tests** - Complete command-line workflows
- **File System Tests** - VDF file operations
- **Steam Integration Tests** - Steam process detection

### End-to-End Tests
- **Complete User Journeys** - Extract → Edit → Update workflow
- **Error Recovery** - Backup and restore scenarios
- **Cross-Platform** - Linux/Steam Deck compatibility

---

## 🧪 Running Tests

### Prerequisites
```bash
# Install test dependencies
cd backend
pip install pytest pytest-cov pytest-mock
```

### Test Commands
```bash
# Run all tests
pytest tests/

# Run backend tests only
pytest tests/backend/

# Run with coverage
pytest --cov=backend/src tests/backend/

# Run specific test file
pytest tests/backend/test_vdf_parser.py

# Run with verbose output
pytest -v tests/backend/
```

### Test Data
- **Fixtures**: Sanitized VDF files and JSON samples
- **Mock Data**: Simulated Steam configurations
- **Test Cases**: Edge cases and error scenarios

---

## 📊 Test Metrics

### Coverage Targets
- **Core Logic**: >90% coverage
- **CLI Interface**: >80% coverage
- **Error Handling**: >85% coverage
- **File Operations**: >90% coverage

### Quality Gates
- All tests must pass before merge
- Coverage must not decrease
- No critical security vulnerabilities
- Performance tests within acceptable limits

---

## 🔧 Test Development

### Writing Tests
1. **Test Structure**: Arrange → Act → Assert
2. **Naming**: Descriptive test names
3. **Isolation**: Tests should not depend on each other
4. **Mocking**: Use mocks for external dependencies

### Test Data Management
- **Fixtures**: Reusable test data
- **Factories**: Generate test data dynamically
- **Cleanup**: Ensure tests don't leave artifacts

### Continuous Integration
- **Automated Testing**: Run on every push
- **Coverage Reporting**: Track coverage trends
- **Performance Monitoring**: Detect regressions

---

## 📚 Test Documentation

### Test Cases
- **[VDF Parser Test Cases](backend/test_vdf_parser.py)** - Parsing scenarios
- **[Game Resolution Test Cases](backend/test_game_resolver.py)** - Name resolution
- **[Configuration Test Cases](backend/test_config_manager.py)** - Config management
- **[Backup Test Cases](backend/test_backup_manager.py)** - Backup operations

### Test Utilities
- **Mock VDF Files** - Test data for parsing
- **Mock Steam Processes** - Process detection testing
- **Test Configuration** - Isolated test environment

---

## 🚨 Troubleshooting Tests

### Common Issues
- **File Permissions**: Ensure test files are readable
- **Path Issues**: Use relative paths in tests
- **Mock Failures**: Verify mock setup and teardown
- **Coverage Gaps**: Identify untested code paths

### Debug Mode
```bash
# Run tests with debug output
pytest -s tests/backend/

# Run single test with debug
pytest -s tests/backend/test_vdf_parser.py::test_parse_localconfig
```

---

## 📞 Support

- [Backend Documentation](../backend/README.md)
- [Development Guide](../docs/technical/)
- [Issues](https://github.com/grimm00/steam-config-analyzer/issues)

---

**Last Updated:** 2025-01-24  
**Status:** 🟡 In Development  
**Next:** Create comprehensive test suite for backend components
