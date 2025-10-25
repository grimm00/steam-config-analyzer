# Technical Validation Plan for Node.js Migration

**Status:** 🟡 Pending Validation  
**Created:** 2025-01-24  
**Last Updated:** 2025-01-24  
**Priority:** High

---

## 📋 Overview

Technical validation plan to verify Node.js can handle all Steam file operations before committing to migration.

---

## 🎯 Validation Requirements

### 1. VDF Library Validation

**Objective:** Verify Node.js VDF libraries can parse actual Steam files

**Test Files Available:**
- `/home/deck/.local/share/Steam/userdata/107256425/config/localconfig.vdf` (text VDF)
- `/home/deck/.local/share/Steam/userdata/107256425/config/shortcuts.vdf` (binary VDF)
- Copied to `/tmp/vdf-test/` for testing

**Libraries to Test:**
1. **simple-vdf** - Most popular, supports both text and binary
2. **node-steamvdf** - Steam-specific VDF parser
3. **vdf-parser** - Alternative implementation

**Validation Steps:**
```bash
# Install Node.js (when available)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Test each library
cd /tmp/vdf-test
npm init -y
npm install simple-vdf
npm install node-steamvdf
npm install vdf-parser

# Create test scripts for each library
```

**Success Criteria:**
- ✅ Parse localconfig.vdf (text format)
- ✅ Parse shortcuts.vdf (binary format)
- ✅ Handle malformed files gracefully
- ✅ Performance comparable to Python vdf library
- ✅ Support for both reading and writing VDF files

### 2. Steam Process Detection

**Objective:** Verify Node.js can detect Steam process status

**Test Implementation:**
```javascript
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

async function isSteamRunning() {
  try {
    const { stdout } = await execAsync('pgrep -f steam');
    return stdout.trim().length > 0;
  } catch (error) {
    return false;
  }
}
```

**Success Criteria:**
- ✅ Detect when Steam is running
- ✅ Detect when Steam is not running
- ✅ Handle process detection errors gracefully
- ✅ Performance acceptable (< 100ms)

### 3. File Watching and Steam State Monitoring

**Objective:** Verify Node.js can monitor Steam configuration changes

**Test Implementation:**
```javascript
import { watch } from 'fs';
import { join } from 'path';

function watchSteamConfig(configPath) {
  return new Promise((resolve, reject) => {
    const watcher = watch(configPath, (eventType, filename) => {
      if (eventType === 'change' && filename === 'localconfig.vdf') {
        console.log('Steam config changed');
        resolve({ eventType, filename });
      }
    });
    
    watcher.on('error', reject);
  });
}
```

**Success Criteria:**
- ✅ Detect localconfig.vdf changes
- ✅ Detect shortcuts.vdf changes
- ✅ Handle file system events properly
- ✅ No memory leaks in long-running watchers

### 4. File System Operations

**Objective:** Verify Node.js file operations work with Steam paths

**Test Operations:**
- Read/write Steam configuration files
- Create backup directories
- Handle file permissions
- Cross-platform path handling

**Success Criteria:**
- ✅ Read Steam config files successfully
- ✅ Write backup files successfully
- ✅ Handle file permissions correctly
- ✅ Cross-platform compatibility

---

## 🔧 Validation Environment Setup

### Prerequisites
1. **Node.js Installation** (when available on Steam Deck)
2. **Test Files** (already copied to `/tmp/vdf-test/`)
3. **Steam Process** (for testing process detection)

### Test Script Structure
```
/tmp/vdf-test/
├── localconfig.vdf          # Test file
├── shortcuts.vdf            # Test file
├── package.json             # Node.js project
├── test-simple-vdf.js       # simple-vdf tests
├── test-node-steamvdf.js    # node-steamvdf tests
├── test-vdf-parser.js       # vdf-parser tests
├── test-process-detection.js # Steam process tests
└── test-file-watching.js    # File watching tests
```

---

## 📊 Validation Results

### VDF Library Testing

| Library | Text VDF | Binary VDF | Performance | Reliability | Recommendation |
|---------|----------|------------|-------------|-------------|----------------|
| simple-vdf | ⏳ Pending | ⏳ Pending | ⏳ Pending | ⏳ Pending | ⏳ Pending |
| node-steamvdf | ⏳ Pending | ⏳ Pending | ⏳ Pending | ⏳ Pending | ⏳ Pending |
| vdf-parser | ⏳ Pending | ⏳ Pending | ⏳ Pending | ⏳ Pending | ⏳ Pending |

### Core Functionality Testing

| Feature | Status | Notes |
|---------|--------|-------|
| Steam Process Detection | ⏳ Pending | Requires Node.js installation |
| File Watching | ⏳ Pending | Requires Node.js installation |
| File System Operations | ⏳ Pending | Requires Node.js installation |
| Error Handling | ⏳ Pending | Requires Node.js installation |

---

## 🚨 Validation Risks

### Risk 1: No Suitable VDF Library
**Impact:** High - Would require custom VDF parser
**Mitigation:** Test all available libraries, consider Python subprocess if needed

### Risk 2: Performance Issues
**Impact:** Medium - Could affect user experience
**Mitigation:** Benchmark against Python implementation

### Risk 3: File System Compatibility
**Impact:** Medium - Could break on different systems
**Mitigation:** Test on multiple platforms

---

## 📋 Next Steps

### Immediate Actions Required
1. **Install Node.js** on Steam Deck (when possible)
2. **Test VDF Libraries** with actual Steam files
3. **Validate Core Operations** (process detection, file watching)
4. **Document Results** in this validation report

### Decision Points
- **If VDF libraries work:** Proceed with migration
- **If VDF libraries fail:** Consider hybrid approach or custom parser
- **If performance is poor:** Evaluate optimization options

---

## 📚 Related Documents

- [ADR 002: Python vs Node.js Decision](002-python-vs-nodejs.md)
- [Migration Plan](002-python-vs-nodejs-migration.md)
- [Field Reference](../../docs/technical/field-reference.md)

---

**Last Updated:** 2025-01-24  
**Status:** 🟡 Pending Validation  
**Next:** Install Node.js and begin technical validation
