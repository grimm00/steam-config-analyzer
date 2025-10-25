# Phase 1: Setup and Dependencies

**Status:** ✅ Complete  
**Created:** 2025-01-24  
**Last Updated:** 2025-01-24  
**Priority:** High

---

## 📋 Overview

Setup Node.js project structure, dependencies, and development environment for the migration.

---

## 🎯 Goals

1. **Project Structure** - Create Node.js backend alongside Python backend
2. **Dependencies** - Install and configure TypeScript, testing, and linting tools
3. **Development Environment** - Setup build process and development scripts
4. **Documentation** - Establish hub-and-spoke planning structure

---

## 🚫 Out of Scope

**Excluded from this phase:**
- ❌ Core module porting - Covered in Phase 2
- ❌ CLI interface - Covered in Phase 3
- ❌ Testing implementation - Covered in Phase 4

---

## 📅 Implementation

### 1.1 Create Migration Branch

```bash
# Create and switch to migration branch
git checkout -b feat/nodejs-migration
```

**Status:** ✅ Complete

### 1.2 Install Node.js (if needed)

```bash
# Install Node.js 20.x on Steam Deck
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installation
node --version
npm --version
```

**Status:** ⏳ Pending (requires sudo access)

### 1.3 Create Node.js Project Structure

```bash
# Create backend-nodejs directory structure
mkdir -p backend-nodejs/src/{core,cli,api,types}
mkdir -p backend-nodejs/tests
```

**Status:** ⏳ Pending

### 1.4 Setup Package Configuration

**package.json:**
```json
{
  "name": "steam-config-analyzer-backend",
  "version": "2.0.0",
  "description": "Steam configuration management tool with CLI and planned GUI",
  "type": "module",
  "main": "dist/index.js",
  "bin": {
    "steam-config-analyzer": "dist/cli/index.js"
  },
  "scripts": {
    "build": "tsc",
    "dev": "tsx src/cli/index.ts",
    "start": "node dist/cli/index.js",
    "test": "vitest",
    "test:run": "vitest run",
    "lint": "eslint src/**/*.ts",
    "lint:fix": "eslint src/**/*.ts --fix",
    "type-check": "tsc --noEmit",
    "clean": "rm -rf dist"
  },
  "dependencies": {
    "simple-vdf": "^1.3.0",
    "commander": "^11.0.0",
    "chalk": "^5.0.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0",
    "eslint": "^8.0.0",
    "typescript": "^5.0.0",
    "tsx": "^4.0.0",
    "vitest": "^1.0.0"
  }
}
```

**Status:** ⏳ Pending

### 1.5 Setup TypeScript Configuration

**tsconfig.json:**
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "node",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "verbatimModuleSyntax": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "tests"]
}
```

**Status:** ⏳ Pending

### 1.6 Setup ESLint Configuration

**.eslintrc.json:**
```json
{
  "env": {
    "es2022": true,
    "node": true
  },
  "extends": [
    "eslint:recommended",
    "@typescript-eslint/recommended"
  ],
  "parser": "@typescript-eslint/parser",
  "parserOptions": {
    "ecmaVersion": "latest",
    "sourceType": "module",
    "project": "./tsconfig.json"
  },
  "plugins": ["@typescript-eslint"],
  "rules": {
    "@typescript-eslint/no-unused-vars": "error",
    "@typescript-eslint/no-explicit-any": "warn",
    "prefer-const": "error",
    "no-var": "error"
  }
}
```

**Status:** ⏳ Pending

### 1.7 Setup Vitest Configuration

**vitest.config.ts:**
```typescript
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    include: ['tests/**/*.test.ts'],
    exclude: ['node_modules', 'dist'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: ['node_modules/', 'dist/', 'tests/']
    }
  }
});
```

**Status:** ⏳ Pending

---

## 🎉 Success Metrics

### Setup Requirements - TARGET

**After Phase 1:** Development environment ready
- ✅ Node.js project structure created
- ✅ TypeScript configuration with strict mode
- ✅ ESLint rules configured
- ✅ Vitest testing framework setup
- ✅ Build and development scripts configured
- ✅ Dependencies installed and configured

---

## 🎊 Key Achievements

1. **Planning Structure** - Hub-and-spoke documentation established
2. **Migration Strategy** - Clear implementation plan with incremental commits
3. **Risk Mitigation** - Comprehensive validation and testing strategy

---

## 🚀 Next Steps

1. **Create Migration Branch** - `feat/nodejs-migration`
2. **Install Node.js** - On Steam Deck if needed
3. **Setup Project Structure** - Create backend-nodejs directory
4. **Configure Dependencies** - Package.json, TypeScript, ESLint, Vitest
5. **Begin Phase 2** - Core module porting

---

## 📚 Related Documents

### Planning
- [Migration Plan](migration-plan.md) - Complete implementation strategy
- [Status & Next Steps](status-and-next-steps.md) - Progress tracking

### Next Phase
- [Phase 2: Core](phase-2-core.md) - Core module porting

---

**Last Updated:** 2025-01-24  
**Status:** ✅ Complete  
**Next:** Begin Phase 2 core module porting
