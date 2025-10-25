# Sourcery Security Analysis - PR #1

**PR:** [#1 - Phase 1 & 2: Node.js Migration Core Modules](https://github.com/grimm00/steam-config-analyzer/pull/1)  
**Review Date:** 2025-01-24  
**Reviewer:** Sourcery AI

---

## 🚨 Security Issues Detailed Analysis

### 1. Path Traversal Vulnerabilities (9 issues)

#### Risk Assessment
**Severity:** High  
**CVSS Score:** 7.5 (High)  
**Impact:** Directory traversal attacks, unauthorized file access

#### Root Cause
User-controlled input is being passed directly to `path.join()` and `path.resolve()` without validation, allowing potential directory traversal attacks using `../` sequences.

#### Affected Code Locations

**`backend-nodejs/src/core/backup-manager.ts`**
```typescript
// Line 120 - Path traversal risk
const backupPath = join(this.backupDir, `localconfig_backup_${timestamp}.vdf`);
```

**`backend-nodejs/src/core/config-manager.ts`**
```typescript
// Lines 44-45 - Path traversal risk
this.steamConfigPath = join(homedir(), '.local', 'share', 'Steam', 'userdata', steamUserId, 'config');
this.localconfigPath = join(this.steamConfigPath, 'localconfig.vdf');
```

**`backend-nodejs/src/core/game-resolver.ts`**
```typescript
// Lines 45-46 - Path traversal risk
this.steamPath = join(homedir(), '.local', 'share', 'Steam');
this.steamappsPath = join(this.steamPath, 'steamapps');

// Line 102 - Path traversal risk
const manifestPath = join(this.steamappsPath, `appmanifest_${appId}.acf`);

// Line 136 - Path traversal risk
const cacheFilePath = join(this.libraryCachePath, `${appId}.json`);
```

**`backend-nodejs/src/core/vdf-parser.ts`**
```typescript
// Lines 28-29 - Path traversal risk
this.localconfigPath = join(steamConfigPath, 'localconfig.vdf');
this.shortcutsPath = join(steamConfigPath, 'shortcuts.vdf');
```

#### Attack Scenarios
1. **Steam User ID Manipulation**: If `steamUserId` contains `../`, attacker could access files outside Steam directory
2. **App ID Manipulation**: If `appId` contains `../`, attacker could access arbitrary files
3. **Config Path Manipulation**: If `steamConfigPath` contains `../`, attacker could access system files

### 2. Non-Literal File System Operations (11 issues)

#### Risk Assessment
**Severity:** Medium  
**CVSS Score:** 5.3 (Medium)  
**Impact:** Unauthorized file access, potential data exposure

#### Root Cause
Function arguments containing user-controlled data are passed directly to file system operations without validation or sanitization.

#### Affected Code Locations

**`backend-nodejs/src/core/backup-manager.ts`**
```typescript
// Lines 95, 100 - backupPath parameter
async restoreBackup(backupPath: string): Promise<void> {
  if (!existsSync(backupPath)) { // Line 95 - Unvalidated path
    throw new BackupError(`Backup file not found: ${backupPath}`, backupPath);
  }
  await copyFile(backupPath, this.localconfigPath); // Line 100 - Unvalidated path
}

// Line 125 - file parameter in listBackups
const backupFiles = files.filter(file => file.startsWith('localconfig_backup_') && file.endsWith('.vdf'));

// Line 152 - keepCount parameter
async cleanupOldBackups(keepCount: number = 10): Promise<void> {

// Lines 170, 190, 194 - backupPath parameter
async getBackupInfo(backupPath: string): Promise<BackupInfo> {
  const stats = await stat(backupPath); // Line 170 - Unvalidated path
}

async validateBackup(backupPath: string): Promise<boolean> {
  if (!existsSync(backupPath)) { // Line 190 - Unvalidated path
    return false;
  }
  const stats = await stat(backupPath); // Line 194 - Unvalidated path
}
```

**`backend-nodejs/src/core/game-resolver.ts`**
```typescript
// Lines 104, 109 - appId parameter
private async getNameFromAppManifest(appId: string): Promise<string | null> {
  const manifestPath = join(this.steamappsPath, `appmanifest_${appId}.acf`);
  if (!existsSync(manifestPath)) { // Line 104 - Unvalidated path
    return null;
  }
  const content = await readFile(manifestPath, 'utf-8'); // Line 109 - Unvalidated path
}

// Lines 138, 143 - appId parameter
private async getNameFromLibraryCache(appId: string): Promise<string | null> {
  const cacheFilePath = join(this.libraryCachePath, `${appId}.json`);
  if (!existsSync(cacheFilePath)) { // Line 138 - Unvalidated path
    return null;
  }
  const content = await readFile(cacheFilePath, 'utf-8'); // Line 143 - Unvalidated path
}
```

#### Attack Scenarios
1. **Backup Path Manipulation**: Attacker could specify backup paths outside allowed directory
2. **App ID Injection**: Attacker could use app IDs to access arbitrary files
3. **File System Enumeration**: Attacker could probe file system for sensitive files

## 🛡️ Recommended Security Fixes

### 1. Path Validation Utility

Create a centralized path validation utility:

```typescript
import { normalize, resolve, isAbsolute } from 'path';

export class SecurityError extends Error {
  constructor(message: string, public readonly code: string = 'SECURITY_ERROR') {
    super(message);
    this.name = 'SecurityError';
  }
}

export function validatePath(userPath: string, allowedBasePath: string): string {
  // Normalize the path
  const normalized = normalize(userPath);
  
  // Prevent directory traversal
  if (normalized.includes('..')) {
    throw new SecurityError('Path traversal detected: contains ".."');
  }
  
  // Ensure path is absolute and within allowed base
  const resolved = resolve(normalized);
  const baseResolved = resolve(allowedBasePath);
  
  if (!resolved.startsWith(baseResolved)) {
    throw new SecurityError(`Path outside allowed directory: ${resolved}`);
  }
  
  return resolved;
}

export function validateAppId(appId: string): string {
  // App IDs should only contain digits
  if (!/^\d+$/.test(appId)) {
    throw new SecurityError(`Invalid app ID format: ${appId}`);
  }
  
  // Prevent extremely long app IDs (potential DoS)
  if (appId.length > 20) {
    throw new SecurityError(`App ID too long: ${appId}`);
  }
  
  return appId;
}

export function validateBackupPath(backupPath: string, backupDir: string): string {
  return validatePath(backupPath, backupDir);
}
```

### 2. Input Sanitization

Add input validation to all public methods:

```typescript
// In BackupManager
async restoreBackup(backupPath: string): Promise<void> {
  const validatedPath = validateBackupPath(backupPath, this.backupDir);
  // ... rest of method
}

// In GameNameResolver
private async getNameFromAppManifest(appId: string): Promise<string | null> {
  const validatedAppId = validateAppId(appId);
  const manifestPath = join(this.steamappsPath, `appmanifest_${validatedAppId}.acf`);
  // ... rest of method
}
```

### 3. Configuration Validation

Add validation for constructor parameters:

```typescript
// In VDFConfigManager constructor
constructor(steamUserId: string = '107256425') {
  // Validate Steam user ID
  if (!/^\d+$/.test(steamUserId)) {
    throw new SecurityError(`Invalid Steam user ID format: ${steamUserId}`);
  }
  
  // Validate Steam user ID length
  if (steamUserId.length > 20) {
    throw new SecurityError(`Steam user ID too long: ${steamUserId}`);
  }
  
  this.steamUserId = steamUserId;
  // ... rest of constructor
}
```

## 🧪 Testing Security Fixes

### Unit Tests for Path Validation

```typescript
import { validatePath, validateAppId, SecurityError } from '../src/utils/security';

describe('Path Validation', () => {
  test('should reject paths with directory traversal', () => {
    expect(() => validatePath('../../../etc/passwd', '/safe/dir')).toThrow(SecurityError);
  });
  
  test('should reject paths outside allowed directory', () => {
    expect(() => validatePath('/etc/passwd', '/safe/dir')).toThrow(SecurityError);
  });
  
  test('should accept valid paths within allowed directory', () => {
    const result = validatePath('subdir/file.txt', '/safe/dir');
    expect(result).toBe('/safe/dir/subdir/file.txt');
  });
});

describe('App ID Validation', () => {
  test('should reject non-numeric app IDs', () => {
    expect(() => validateAppId('abc123')).toThrow(SecurityError);
  });
  
  test('should reject extremely long app IDs', () => {
    expect(() => validateAppId('1'.repeat(25))).toThrow(SecurityError);
  });
  
  test('should accept valid app IDs', () => {
    const result = validateAppId('123456');
    expect(result).toBe('123456');
  });
});
```

## 📋 Implementation Priority

1. **High Priority** - Path traversal fixes (9 issues)
2. **Medium Priority** - File system operation validation (11 issues)
3. **Low Priority** - Additional input validation and sanitization

## 🔗 References

- [OWASP Path Traversal](https://owasp.org/www-community/attacks/Path_Traversal)
- [Node.js Security Best Practices](https://nodejs.org/en/docs/guides/security/)
- [Sourcery Security Guidelines](https://docs.sourcery.ai/security/)

---

**Next Steps:** See [Action Plan](pr01-action-plan.md) for implementation details.
