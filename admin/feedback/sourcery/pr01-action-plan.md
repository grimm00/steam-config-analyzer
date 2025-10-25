# Sourcery Security Action Plan - PR #1

**PR:** [#1 - Phase 1 & 2: Node.js Migration Core Modules](https://github.com/grimm00/steam-config-analyzer/pull/1)  
**Created:** 2025-01-24  
**Priority:** High

---

## 🎯 Overview

This action plan addresses the 20 security issues identified by Sourcery in the Node.js migration core modules. The plan prioritizes fixes by severity and provides a structured approach to implementing security improvements.

## 📊 Issue Summary

| Priority | Issue Type | Count | Files | Estimated Time |
|----------|------------|-------|-------|----------------|
| **High** | Path Traversal | 9 | 4 | 45 minutes |
| **Medium** | Non-Literal FS Filename | 11 | 2 | 30 minutes |
| **Total** | | **20** | **4** | **75 minutes** |

## 🚀 Implementation Strategy

### Option A: Address Security Before Phase 3 (Recommended)
**Timeline:** 1-2 hours  
**Approach:** Fix all security issues before continuing with CLI development

**Benefits:**
- Clean security foundation for Phase 3
- Single security review cycle
- No security debt accumulation

### Option B: Address Security in Parallel with Phase 3
**Timeline:** 2-3 hours (parallel work)  
**Approach:** Create separate security branch while continuing CLI work

**Benefits:**
- Faster overall migration progress
- Parallel development streams
- Independent review cycles

## 📋 Detailed Action Items

### Phase 1: Security Infrastructure (15 minutes)

#### 1.1 Create Security Utility Module
**File:** `backend-nodejs/src/utils/security.ts`

```typescript
import { normalize, resolve } from 'path';

export class SecurityError extends Error {
  constructor(message: string, public readonly code: string = 'SECURITY_ERROR') {
    super(message);
    this.name = 'SecurityError';
  }
}

export function validatePath(userPath: string, allowedBasePath: string): string {
  const normalized = normalize(userPath);
  
  if (normalized.includes('..')) {
    throw new SecurityError('Path traversal detected: contains ".."');
  }
  
  const resolved = resolve(normalized);
  const baseResolved = resolve(allowedBasePath);
  
  if (!resolved.startsWith(baseResolved)) {
    throw new SecurityError(`Path outside allowed directory: ${resolved}`);
  }
  
  return resolved;
}

export function validateAppId(appId: string): string {
  if (!/^\d+$/.test(appId)) {
    throw new SecurityError(`Invalid app ID format: ${appId}`);
  }
  
  if (appId.length > 20) {
    throw new SecurityError(`App ID too long: ${appId}`);
  }
  
  return appId;
}

export function validateSteamUserId(userId: string): string {
  if (!/^\d+$/.test(userId)) {
    throw new SecurityError(`Invalid Steam user ID format: ${userId}`);
  }
  
  if (userId.length > 20) {
    throw new SecurityError(`Steam user ID too long: ${userId}`);
  }
  
  return userId;
}
```

#### 1.2 Update Type Definitions
**File:** `backend-nodejs/src/types/index.ts`

Add SecurityError to error types:

```typescript
export interface SecurityError extends Error {
  code: string;
}
```

### Phase 2: Path Traversal Fixes (45 minutes)

#### 2.1 Fix VDF Parser (5 minutes)
**File:** `backend-nodejs/src/core/vdf-parser.ts`

```typescript
import { validatePath } from '../utils/security.js';

constructor(steamConfigPath: string) {
  // Validate steam config path
  const validatedPath = validatePath(steamConfigPath, process.cwd());
  this.steamConfigPath = validatedPath;
  this.localconfigPath = join(validatedPath, 'localconfig.vdf');
  this.shortcutsPath = join(validatedPath, 'shortcuts.vdf');
}
```

#### 2.2 Fix Config Manager (10 minutes)
**File:** `backend-nodejs/src/core/config-manager.ts`

```typescript
import { validateSteamUserId } from '../utils/security.js';

constructor(steamUserId: string = '107256425') {
  this.steamUserId = validateSteamUserId(steamUserId);
  
  // Validate Steam paths
  const steamBasePath = join(homedir(), '.local', 'share', 'Steam');
  this.steamConfigPath = validatePath(
    join(steamBasePath, 'userdata', this.steamUserId, 'config'),
    steamBasePath
  );
  this.localconfigPath = join(this.steamConfigPath, 'localconfig.vdf');
  // ... rest of constructor
}
```

#### 2.3 Fix Game Resolver (15 minutes)
**File:** `backend-nodejs/src/core/game-resolver.ts`

```typescript
import { validateSteamUserId, validateAppId, validatePath } from '../utils/security.js';

constructor(steamUserId: string = '107256425') {
  this.steamUserId = validateSteamUserId(steamUserId);
  
  // Validate Steam paths
  const steamBasePath = join(homedir(), '.local', 'share', 'Steam');
  this.steamPath = validatePath(steamBasePath, homedir());
  this.steamappsPath = join(this.steamPath, 'steamapps');
  // ... rest of constructor
}

private async getNameFromAppManifest(appId: string): Promise<string | null> {
  const validatedAppId = validateAppId(appId);
  const manifestPath = join(this.steamappsPath, `appmanifest_${validatedAppId}.acf`);
  // ... rest of method
}

private async getNameFromLibraryCache(appId: string): Promise<string | null> {
  const validatedAppId = validateAppId(appId);
  const cacheFilePath = join(this.libraryCachePath, `${validatedAppId}.json`);
  // ... rest of method
}
```

#### 2.4 Fix Backup Manager (15 minutes)
**File:** `backend-nodejs/src/core/backup-manager.ts`

```typescript
import { validatePath } from '../utils/security.js';

constructor(localconfigPath: string, backupDir: string) {
  this.localconfigPath = validatePath(localconfigPath, process.cwd());
  this.backupDir = validatePath(backupDir, process.cwd());
}

async createBackup(): Promise<string> {
  await this.ensureBackupDir();
  
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
  const backupPath = validatePath(
    join(this.backupDir, `localconfig_backup_${timestamp}.vdf`),
    this.backupDir
  );
  
  await copyFile(this.localconfigPath, backupPath);
  return backupPath;
}
```

### Phase 3: File System Operation Validation (30 minutes)

#### 3.1 Backup Manager Validation (20 minutes)
**File:** `backend-nodejs/src/core/backup-manager.ts`

```typescript
async restoreBackup(backupPath: string): Promise<void> {
  const validatedPath = validatePath(backupPath, this.backupDir);
  
  if (await this.isSteamRunning()) {
    throw new BackupError('Steam is currently running. Please close Steam before restoring configuration.', validatedPath);
  }
  
  if (!existsSync(validatedPath)) {
    throw new BackupError(`Backup file not found: ${validatedPath}`, validatedPath);
  }
  
  await copyFile(validatedPath, this.localconfigPath);
}

async getBackupInfo(backupPath: string): Promise<BackupInfo> {
  const validatedPath = validatePath(backupPath, this.backupDir);
  
  try {
    const stats = await stat(validatedPath);
    return {
      path: validatedPath,
      size: stats.size,
      created: stats.birthtime,
      modified: stats.mtime
    };
  } catch (error) {
    throw new BackupError(`Failed to get backup info: ${error}`, validatedPath);
  }
}

async validateBackup(backupPath: string): Promise<boolean> {
  try {
    const validatedPath = validatePath(backupPath, this.backupDir);
    
    if (!existsSync(validatedPath)) {
      return false;
    }
    
    const stats = await stat(validatedPath);
    return stats.size > 0;
  } catch (error) {
    return false;
  }
}
```

#### 3.2 Game Resolver Validation (10 minutes)
**File:** `backend-nodejs/src/core/game-resolver.ts`

```typescript
private async getNameFromAppManifest(appId: string): Promise<string | null> {
  const validatedAppId = validateAppId(appId);
  const manifestPath = join(this.steamappsPath, `appmanifest_${validatedAppId}.acf`);
  
  // Additional validation: ensure path is within steamapps
  const validatedPath = validatePath(manifestPath, this.steamappsPath);
  
  if (!existsSync(validatedPath)) {
    return null;
  }
  
  try {
    const content = await readFile(validatedPath, 'utf-8');
    // ... rest of method
  } catch (error) {
    console.warn(`Warning: Could not parse app manifest for ${validatedAppId}: ${error}`);
    return null;
  }
}

private async getNameFromLibraryCache(appId: string): Promise<string | null> {
  const validatedAppId = validateAppId(appId);
  const cacheFilePath = join(this.libraryCachePath, `${validatedAppId}.json`);
  
  // Additional validation: ensure path is within library cache
  const validatedPath = validatePath(cacheFilePath, this.libraryCachePath);
  
  if (!existsSync(validatedPath)) {
    return null;
  }
  
  try {
    const content = await readFile(validatedPath, 'utf-8');
    // ... rest of method
  } catch (error) {
    console.warn(`Warning: Could not parse library cache for ${validatedAppId}: ${error}`);
    return null;
  }
}
```

### Phase 4: Testing and Validation (15 minutes)

#### 4.1 Create Security Tests
**File:** `backend-nodejs/tests/security.test.ts`

```typescript
import { describe, test, expect } from 'vitest';
import { validatePath, validateAppId, validateSteamUserId, SecurityError } from '../src/utils/security.js';

describe('Security Validation', () => {
  describe('validatePath', () => {
    test('should reject directory traversal', () => {
      expect(() => validatePath('../../../etc/passwd', '/safe/dir')).toThrow(SecurityError);
    });
    
    test('should reject paths outside allowed directory', () => {
      expect(() => validatePath('/etc/passwd', '/safe/dir')).toThrow(SecurityError);
    });
    
    test('should accept valid paths', () => {
      const result = validatePath('subdir/file.txt', '/safe/dir');
      expect(result).toContain('/safe/dir/subdir/file.txt');
    });
  });
  
  describe('validateAppId', () => {
    test('should reject non-numeric app IDs', () => {
      expect(() => validateAppId('abc123')).toThrow(SecurityError);
    });
    
    test('should reject long app IDs', () => {
      expect(() => validateAppId('1'.repeat(25))).toThrow(SecurityError);
    });
    
    test('should accept valid app IDs', () => {
      expect(validateAppId('123456')).toBe('123456');
    });
  });
  
  describe('validateSteamUserId', () => {
    test('should reject non-numeric user IDs', () => {
      expect(() => validateSteamUserId('user123')).toThrow(SecurityError);
    });
    
    test('should accept valid user IDs', () => {
      expect(validateSteamUserId('107256425')).toBe('107256425');
    });
  });
});
```

#### 4.2 Integration Tests
**File:** `backend-nodejs/tests/integration/security.test.ts`

```typescript
import { describe, test, expect } from 'vitest';
import { VDFConfigManager } from '../../src/core/config-manager.js';
import { SecurityError } from '../../src/utils/security.js';

describe('Security Integration Tests', () => {
  test('should reject invalid Steam user ID', () => {
    expect(() => new VDFConfigManager('invalid-user-id')).toThrow(SecurityError);
  });
  
  test('should accept valid Steam user ID', () => {
    const manager = new VDFConfigManager('107256425');
    expect(manager.getSteamUserId()).toBe('107256425');
  });
});
```

## 🎯 Success Criteria

- ✅ All 20 security issues addressed
- ✅ Path traversal vulnerabilities eliminated
- ✅ File system operations validated
- ✅ Security tests passing
- ✅ Sourcery re-review approved
- ✅ No regression in functionality

## 📅 Timeline

| Phase | Duration | Dependencies |
|-------|----------|--------------|
| Phase 1: Security Infrastructure | 15 minutes | None |
| Phase 2: Path Traversal Fixes | 45 minutes | Phase 1 |
| Phase 3: FS Operation Validation | 30 minutes | Phase 1 |
| Phase 4: Testing and Validation | 15 minutes | Phases 2-3 |
| **Total** | **105 minutes** | |

## 🔄 Implementation Options

### Option A: Single Security Branch
1. Create `fix/security-validation` branch
2. Implement all security fixes
3. Update PR #1 with security fixes
4. Get Sourcery re-review
5. Merge to develop
6. Continue with Phase 3

### Option B: Parallel Development
1. Create `fix/security-validation` branch
2. Continue Phase 3 on `feat/nodejs-migration`
3. Implement security fixes in parallel
4. Create separate security PR
5. Merge both PRs to develop

## 🚨 Risk Mitigation

- **Backup Strategy**: All changes in feature branch
- **Testing**: Comprehensive security test suite
- **Review**: Sourcery re-review after fixes
- **Rollback**: Easy rollback to pre-security state

## 📋 Checklist

- [ ] Create security utility module
- [ ] Fix VDF parser path validation
- [ ] Fix config manager path validation
- [ ] Fix game resolver path validation
- [ ] Fix backup manager path validation
- [ ] Add file system operation validation
- [ ] Create security test suite
- [ ] Run all tests
- [ ] Update PR #1 with security fixes
- [ ] Request Sourcery re-review
- [ ] Address any remaining feedback

---

**Next Steps:** Choose implementation option and begin Phase 1 security infrastructure.
